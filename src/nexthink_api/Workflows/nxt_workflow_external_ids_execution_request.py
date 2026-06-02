"""Workflows API v2 external identifiers execution request model."""
# ruff: noqa: N815 - Field names follow the official Workflows API schema.

from typing import Self

from pydantic import BaseModel, Field, model_validator

from nexthink_api.Workflows.nxt_workflow_execution_request import SID_PATTERN, UUID_PATTERN

__all__ = ["NxtWorkflowDeviceData", "NxtWorkflowExternalIdsExecutionRequest", "NxtWorkflowUserData"]

UPN_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class NxtWorkflowDeviceData(BaseModel):
    """Device selector accepted by Workflows v2 execution."""

    name: str | None = None
    uid: str | None = Field(default=None, pattern=UUID_PATTERN)
    collectorUid: str | None = Field(default=None, pattern=UUID_PATTERN)

    @model_validator(mode="after")
    def validate_identifier(self) -> Self:
        """Require at least one supported device identifier."""
        if not any([self.name, self.uid, self.collectorUid]):
            raise ValueError("At least one device identifier is required")
        return self


class NxtWorkflowUserData(BaseModel):
    """User selector accepted by Workflows v2 execution."""

    uid: str | None = Field(default=None, pattern=UUID_PATTERN)
    upn: str | None = Field(default=None, pattern=UPN_PATTERN)
    sid: str | None = Field(default=None, pattern=SID_PATTERN)

    @model_validator(mode="after")
    def validate_identifier(self) -> Self:
        """Require at least one supported user identifier."""
        if not any([self.uid, self.upn, self.sid]):
            raise ValueError("At least one user identifier is required")
        return self


class NxtWorkflowExternalIdsExecutionRequest(BaseModel):
    """Request body used to execute a workflow with external identifiers."""

    workflowId: str = Field(min_length=1)
    devices: list[NxtWorkflowDeviceData] = Field(default_factory=list, max_length=10000)
    users: list[NxtWorkflowUserData] = Field(default_factory=list, max_length=10000)
    params: dict[str, str] | None = None

    @model_validator(mode="after")
    def validate_targets(self) -> Self:
        """Require at least one target despite contradictory docs required fields."""
        if not self.devices and not self.users:
            raise ValueError("At least one device or user target is required")
        return self
