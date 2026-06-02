"""Campaigns API trigger success response model."""

from pydantic import BaseModel, Field

from nexthink_api.Campaigns.nxt_campaign_trigger_response_details import NxtCampaignTriggerResponseDetails

__all__ = ["NxtCampaignTriggerSuccessResponse"]


class NxtCampaignTriggerSuccessResponse(BaseModel):
    """Response returned when campaign trigger requests are created."""

    requests: list[NxtCampaignTriggerResponseDetails] = Field(min_length=1)
