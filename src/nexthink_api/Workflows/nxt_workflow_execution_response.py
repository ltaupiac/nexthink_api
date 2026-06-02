"""Workflows API execution response model."""
# ruff: noqa: N815 - Field names follow the official Workflows API schema.

from pydantic import BaseModel, Field

__all__ = ["NxtWorkflowExecutionResponse"]


class NxtWorkflowExecutionResponse(BaseModel):
    """Response returned when a workflow execution request is accepted."""

    requestUuid: str = Field(min_length=1)
    executionsUuids: list[str] = Field(min_length=1)
