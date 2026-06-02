"""Campaigns API trigger error response model."""

from pydantic import BaseModel, Field

__all__ = ["NxtCampaignTriggerErrorResponse"]


class NxtCampaignTriggerErrorResponse(BaseModel):
    """Error details returned by the Campaigns API."""

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
