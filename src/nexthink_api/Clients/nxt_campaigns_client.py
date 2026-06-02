"""Internal Campaigns domain client."""

from nexthink_api.Campaigns.nxt_campaign_trigger_request import NxtCampaignTriggerRequest
from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.Clients.nxt_response import CampaignResponseType, NxtResponse
from nexthink_api.Models.nxt_endpoint import NxtEndpoint

__all__ = ["NxtCampaignsClient"]


class NxtCampaignsClient:
    """Internal delegate for Campaigns behavior."""

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal Campaigns client."""
        self._api_client = api_client

    def trigger(self, data: NxtCampaignTriggerRequest) -> CampaignResponseType:
        """Trigger a campaign for a set of user SIDs."""
        endpoint = NxtEndpoint.Engage
        if not self._api_client.check_method(endpoint, "POST"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.post(
            endpoint.value,
            headers=self._api_client.headers,
            json=data.model_dump(exclude_none=True),
        )
        return NxtResponse().from_response(response=response)
