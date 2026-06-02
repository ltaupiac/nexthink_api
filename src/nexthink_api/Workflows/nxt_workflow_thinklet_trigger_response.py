"""Workflows API thinklet trigger response model."""
# ruff: noqa: N815 - Field names follow the official Workflows API schema.

from pydantic import BaseModel, Field

__all__ = ["NxtWorkflowThinkletTriggerResponse"]


class NxtWorkflowThinkletTriggerResponse(BaseModel):
    """Response returned when a waiting workflow execution is triggered."""

    requestUuid: str = Field(min_length=1)
