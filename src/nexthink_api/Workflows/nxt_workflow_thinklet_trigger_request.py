"""Workflows API thinklet trigger request model."""

from pydantic import BaseModel, Field

__all__ = ["NxtWorkflowThinkletTriggerRequest"]


class NxtWorkflowThinkletTriggerRequest(BaseModel):
    """Request body used to trigger a waiting workflow execution."""

    parameters: dict[str, str] | None = Field(default=None)
