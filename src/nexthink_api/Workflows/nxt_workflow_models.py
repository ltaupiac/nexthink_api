"""Workflows API inventory models."""
# ruff: noqa: N815 - Field names follow the official Workflows API schema.

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

__all__ = [
    "NxtWorkflow",
    "NxtWorkflowDependency",
    "NxtWorkflowStatus",
    "NxtWorkflowTriggerMethod",
]


class NxtWorkflowDependency(str, Enum):
    """Workflow dependency filters supported by the API."""

    USER = "USER"
    DEVICE = "DEVICE"
    USER_AND_DEVICE = "USER_AND_DEVICE"
    NONE = "NONE"


class NxtWorkflowStatus(str, Enum):
    """Workflow activation status."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class NxtWorkflowTriggerMethod(str, Enum):
    """Workflow trigger method filters supported by the API."""

    API = "API"
    MANUAL = "MANUAL"
    MANUAL_MULTIPLE = "MANUAL_MULTIPLE"
    SCHEDULER = "SCHEDULER"


class NxtWorkflow(BaseModel):
    """Workflow configuration returned by inventory operations.

    The official model currently describes recursive fields for triggerMethods
    and versions. Those fields are kept tolerant until the live payload shape is
    validated across tenants.
    """

    id: str = Field(min_length=1)
    uuid: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None
    status: NxtWorkflowStatus | str | None = None
    lastUpdateTime: datetime | str | None = None
    triggerMethods: Any = None
    versions: list[Any] = Field(default_factory=list)
