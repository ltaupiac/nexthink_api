"""Campaigns API trigger response details model."""
# ruff: noqa: N815 - Field names follow the official Campaigns API schema.

from pydantic import BaseModel

__all__ = ["NxtCampaignTriggerResponseDetails"]


class NxtCampaignTriggerResponseDetails(BaseModel):
    """Per-user result returned by a Campaigns trigger response."""

    userSid: str
    requestId: str | None = None
    message: str | None = None
