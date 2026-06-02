"""Remote Actions API trigger information model."""
# ruff: noqa: N815 - Field names follow the official Remote Actions API schema.

from pydantic import BaseModel, Field

__all__ = ["NxtRemoteActionTriggerInfoRequest"]


class NxtRemoteActionTriggerInfoRequest(BaseModel):
    """Optional context describing why a remote action was triggered."""

    externalSource: str | None = None
    reason: str | None = Field(default=None, max_length=500)
    externalReference: str | None = None
