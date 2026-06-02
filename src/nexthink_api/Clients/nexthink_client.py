"""Public Nexthink API client entrypoint."""

from nexthink_api.Clients.nxt_api_client import NxtApiClient

__all__ = ["NexthinkClient"]


class NexthinkClient(NxtApiClient):
    """Public root client for the cleaned `0.1.0` API."""
