"""Workflows API v1 execution request model."""
# ruff: noqa: N815 - Field names follow the official Workflows API schema.

from typing import Self

from pydantic import BaseModel, Field, model_validator

__all__ = ["NxtWorkflowExecutionRequest"]

UUID_PATTERN = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
SID_PATTERN = r"^S(-\d+){2,10}$|^0$"


class NxtWorkflowExecutionRequest(BaseModel):
    """Request body used to execute a workflow with collector UUIDs or SIDs."""

    workflowId: str = Field(min_length=1)
    devices: list[str] = Field(default_factory=list, max_length=10000)
    users: list[str] = Field(default_factory=list, max_length=10000)
    params: dict[str, str] | None = None

    @model_validator(mode="after")
    def validate_targets(self) -> Self:
        """Require at least one target despite contradictory docs required fields."""
        if not self.devices and not self.users:
            raise ValueError("At least one device or user target is required")
        return self
