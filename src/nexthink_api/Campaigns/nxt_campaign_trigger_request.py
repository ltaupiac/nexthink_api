"""Campaigns API trigger request model."""
# ruff: noqa: N815 - Field names follow the official Campaigns API schema.

from pydantic import BaseModel, Field

__all__ = ["NxtCampaignTriggerRequest"]


class NxtCampaignTriggerRequest(BaseModel):
    """Request body used to trigger a campaign for user SIDs."""

    campaignNqlId: str = Field(min_length=1)
    userSid: list[str] = Field(min_length=1, max_length=10000)
    expiresInMinutes: int = Field(ge=1, le=525600)
    parameters: dict[str, str] | None = Field(default=None, max_length=30)
