"""Remote Actions API execution request model."""
# ruff: noqa: N815 - Field names follow the official Remote Actions API schema.

from pydantic import BaseModel, Field

from nexthink_api.RemoteActions.nxt_remote_action_trigger_info_request import NxtRemoteActionTriggerInfoRequest

__all__ = ["NxtRemoteActionExecutionRequest"]


class NxtRemoteActionExecutionRequest(BaseModel):
    """Request body used to trigger a remote action."""

    remoteActionId: str = Field(min_length=1)
    devices: list[str] = Field(min_length=1, max_length=10000)
    params: dict[str, str] | None = None
    expiresInMinutes: int | None = Field(default=None, ge=60, le=10080)
    triggerInfo: NxtRemoteActionTriggerInfoRequest | None = None
