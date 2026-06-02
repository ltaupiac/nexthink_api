"""Internal HTTP transport used to isolate low-level request execution."""

import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Mapping, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response

from nexthink_api.Clients.nxt_tls import _nxt_ssl_context

__all__ = ["NxtHttpTransport"]


class NxtTruststoreHttpAdapter(HTTPAdapter):
    """Requests adapter using a dedicated truststore SSL context."""

    def __init__(self, ssl_context: ssl.SSLContext) -> None:
        self._ssl_context = ssl_context
        super().__init__()

    def init_poolmanager(self, connections: int, maxsize: int, block: bool = False, **pool_kwargs: object) -> None:
        """Initialize urllib3 pools with the Nexthink SSL context."""
        pool_kwargs["ssl_context"] = self._ssl_context
        super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

    def proxy_manager_for(self, proxy: str, **proxy_kwargs: object) -> object:
        """Initialize proxy pools with the Nexthink SSL context."""
        proxy_kwargs["ssl_context"] = self._ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)


@dataclass(frozen=True)
class NxtHttpTransport:
    """Execute HTTP requests with the current requests-based transport contract.

    This class is intentionally internal. It centralizes URL construction,
    proxies, timeout defaults, and optional TLS request parameters without
    changing the public client behavior.

    Contract:
    - ``get()`` and ``post()`` receive API paths relative to ``base_url``.
    - ``get_url()`` receives an already absolute URL, used for raw downloads.
    - All methods return the raw ``requests.Response`` object.
    - Base headers and per-call headers are merged into a new dictionary.
    - Caller-owned header mappings are never mutated.
    - Proxies and timeout are applied consistently to every request.
    - Per-call timeout overrides the transport default.
    - ``verify`` and ``cert`` are only forwarded when explicitly configured.
    - Truststore uses a request-local ``requests.Session`` adapter after
      ``enable_truststore()`` has been called; Python SSL is not monkey patched.
    - No retries, session pooling, tracing, response parsing, or exception
      normalization are performed here.
    """

    base_url: str
    proxies: Optional[Mapping[str, str]] = None
    timeout: int = 300
    verify: bool | str | None = None
    cert: str | tuple[str, str] | None = None

    def build_url(self, path: str) -> str:
        """Build an absolute API URL from the configured base URL and a path."""
        return urljoin(self.base_url, path)

    def get(
            self,
            path: str,
            *,
            headers: Optional[Mapping[str, str]] = None,
            extra_headers: Optional[Mapping[str, str]] = None,
            params: Optional[Mapping[str, Any]] = None,
            timeout: Optional[int] = None,
    ) -> Response:
        """Execute a GET request against a path relative to the base URL."""
        with self._session() as session:
            return session.request(
                "GET",
                self.build_url(path),
                **self._request_options(timeout, headers=self._merge_headers(headers, extra_headers), params=params),
            )

    def post(
            self,
            path: str,
            *,
            headers: Optional[Mapping[str, str]] = None,
            extra_headers: Optional[Mapping[str, str]] = None,
            json: Optional[Mapping[str, Any]] = None,
            timeout: Optional[int] = None,
    ) -> Response:
        """Execute a POST request against a path relative to the base URL."""
        with self._session() as session:
            return session.request(
                "POST",
                self.build_url(path),
                headers=self._merge_headers(headers, extra_headers),
                json=json,
                **self._request_options(timeout),
            )

    def post_url(
            self,
            url: str,
            *,
            headers: Optional[Mapping[str, str]] = None,
            extra_headers: Optional[Mapping[str, str]] = None,
            data: Optional[Mapping[str, Any]] = None,
            timeout: Optional[int] = None,
    ) -> Response:
        """Execute a POST request against an already absolute URL."""
        with self._session() as session:
            return session.request(
                "POST",
                url,
                headers=self._merge_headers(headers, extra_headers),
                data=data,
                **self._request_options(timeout),
            )

    def get_url(
            self,
            url: str,
            *,
            headers: Optional[Mapping[str, str]] = None,
            extra_headers: Optional[Mapping[str, str]] = None,
            params: Optional[Mapping[str, Any]] = None,
            timeout: Optional[int] = None,
    ) -> Response:
        """Execute a GET request against an already absolute URL."""
        with self._session() as session:
            return session.request(
                "GET",
                url,
                **self._request_options(timeout, headers=self._merge_headers(headers, extra_headers), params=params),
            )

    @staticmethod
    def _merge_headers(
            headers: Optional[Mapping[str, str]],
            extra_headers: Optional[Mapping[str, str]],
    ) -> Optional[dict[str, str]]:
        """Merge base and per-call headers without mutating either mapping."""
        if headers is None and extra_headers is None:
            return None
        return dict(headers or {}) | dict(extra_headers or {})

    def _request_options(
            self,
            timeout: Optional[int],
            *,
            headers: Optional[Mapping[str, str]] = None,
            params: Optional[Mapping[str, Any]] = None,
    ) -> dict[str, Any]:
        """Return shared requests keyword arguments."""
        options: dict[str, Any] = {
            "proxies": self.proxies,
            "timeout": timeout if timeout is not None else self.timeout,
        }
        if headers is not None:
            options["headers"] = headers
        if params is not None:
            options["params"] = params
        if self.verify is not None:
            options["verify"] = self.verify
        if self.cert is not None:
            options["cert"] = self.cert
        return options

    @contextmanager
    def _session(self) -> Iterator[requests.Session]:
        """Create a short-lived requests session configured for Nexthink TLS."""
        session = requests.Session()
        ssl_context = _nxt_ssl_context()
        if ssl_context is not None:
            adapter = NxtTruststoreHttpAdapter(ssl_context)
            session.mount("https://", adapter)
        try:
            yield session
        finally:
            session.close()
