"""Internal protocol for domain clients that delegate to NxtApiClient."""

from typing import Protocol

from nexthink_api.Clients.nxt_http_transport import NxtHttpTransport
from nexthink_api.Clients.nxt_response import ResponseApiType
from nexthink_api.Models.nxt_endpoint import NxtEndpoint

__all__ = ["NxtClientFacade"]


class NxtClientFacade(Protocol):
    """Minimal internal facade owned by `NxtApiClient` during domain extraction."""

    headers: dict[str, str]
    transport: NxtHttpTransport

    def check_method(self, endpoint: NxtEndpoint, method: str) -> bool:
        """Check whether an HTTP method is supported for an endpoint."""

    def update_header(self, endpoint: NxtEndpoint = None) -> None:
        """Update persistent headers for the provided endpoint."""

    def post(
            self,
            endpoint: NxtEndpoint,
            data: object,
            headers: dict[str, str] | None = None,
    ) -> ResponseApiType:
        """Send a POST request through the public facade."""

    def get(
            self,
            endpoint: NxtEndpoint,
            params: object = None,
    ) -> ResponseApiType:
        """Send a GET request through the public facade."""
