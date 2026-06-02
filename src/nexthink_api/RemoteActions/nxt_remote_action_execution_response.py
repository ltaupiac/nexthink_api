"""Remote Actions API execution response model."""
# ruff: noqa: N815 - Field names follow the official Remote Actions API schema.

from pydantic import BaseModel, Field

__all__ = ["NxtRemoteActionExecutionResponse"]


class NxtRemoteActionExecutionResponse(BaseModel):
    """Response returned when a remote action execution request is accepted."""

    requestId: str = Field(min_length=1)
    expiresInMinutes: int | None = Field(default=None, ge=1, le=10080)
