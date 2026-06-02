"""Internal OAuth token provider."""

import base64
import time
from collections.abc import Callable
from dataclasses import dataclass
from http import HTTPStatus

import requests

from nexthink_api.Clients.nxt_http_transport import NxtHttpTransport
from nexthink_api.Clients.nxt_response import NxtResponse
from nexthink_api.Exceptions.nxt_token_exception import NxtTokenException
from nexthink_api.Models.nxt_settings import NxtSettings
from nexthink_api.Models.nxt_token_request import NxtTokenRequest
from nexthink_api.Models.nxt_token_response import NxtTokenResponse

__all__ = ["NxtTokenProvider"]


@dataclass
class NxtTokenProvider:
    """Retrieve and cache OAuth tokens for Nexthink API calls."""

    settings: NxtSettings
    transport: NxtHttpTransport
    client_id: str
    client_secret: str
    refresh_margin_seconds: int = 60
    now: Callable[[], float] = time.time
    token: NxtTokenResponse | None = None
    expires_at: float | None = None

    def basic_auth_headers(self) -> dict[str, str]:
        """Return headers required by the OAuth token endpoint."""
        credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        return {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

    def get_token(self) -> NxtTokenResponse | None:
        """Return a cached token or request a new one when needed."""
        if self._has_valid_token():
            return self.token
        return self.request_token()

    def request_token(self) -> NxtTokenResponse | None:
        """Request a token from the official OAuth token endpoint."""
        try:
            response = self.transport.post_url(
                str(self.settings.token_url),
                headers=self.basic_auth_headers(),
                data=NxtTokenRequest().get_request_header(),
            )
            if response.status_code != HTTPStatus.OK:
                return None
            token = NxtResponse().build_nxt_token_response(response=response)
            self.token = token
            self.expires_at = self.now() + token.expires_in
            return token
        except requests.exceptions.HTTPError as e:
            raise NxtTokenException(f"Error during token retrieval: {e}") from e

    def authorization_header(self) -> str | None:
        """Return a bearer authorization header value when a token is available."""
        token = self.get_token()
        if token is None:
            return None
        return f"Bearer {token.access_token}"

    def _has_valid_token(self) -> bool:
        """Return True when the cached token is not close to expiration."""
        if self.token is None or self.expires_at is None:
            return False
        return self.now() < self.expires_at - self.refresh_margin_seconds
