"""Internal Remote Actions domain client."""

from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.Clients.nxt_response import NxtResponse, RemoteActionsResponseType
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.RemoteActions.nxt_remote_action_execution_request import NxtRemoteActionExecutionRequest

__all__ = ["NxtRemoteActionsClient"]


class NxtRemoteActionsClient:
    """Internal delegate for Remote Actions behavior."""

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal Remote Actions client."""
        self._api_client = api_client

    def execute(self, data: NxtRemoteActionExecutionRequest) -> RemoteActionsResponseType:
        """Trigger a remote action execution for a set of devices."""
        endpoint = NxtEndpoint.Act
        if not self._api_client.check_method(endpoint, "POST"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.post(
            endpoint.value,
            headers=self._api_client.headers,
            json=data.model_dump(exclude_none=True),
        )
        return NxtResponse().from_response(response=response)

    def list(self) -> RemoteActionsResponseType:
        """Return remote actions configuration metadata."""
        endpoint = NxtEndpoint.RemoteActions
        if not self._api_client.check_method(endpoint, "GET"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.get(endpoint.value, headers=self._api_client.headers)
        return NxtResponse().from_response(response=response)

    def get(self, nql_id: str) -> RemoteActionsResponseType:
        """Return one remote action configuration by NQL ID."""
        endpoint = NxtEndpoint.RemoteActionsDetails
        if not self._api_client.check_method(endpoint, "GET"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.get(
            endpoint.value,
            headers=self._api_client.headers,
            params={"nql-id": nql_id},
        )
        return NxtResponse().from_response(response=response)
