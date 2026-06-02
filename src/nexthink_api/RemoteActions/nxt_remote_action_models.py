"""Remote Actions API inventory models."""
# ruff: noqa: N815 - Field names follow the official Remote Actions API schema.

from enum import Enum

from pydantic import BaseModel, Field

__all__ = [
    "NxtRemoteAction",
    "NxtRemoteActionInput",
    "NxtRemoteActionOutput",
    "NxtRemoteActionPurpose",
    "NxtRemoteActionRunAsOption",
    "NxtRemoteActionScriptInfo",
    "NxtRemoteActionTargeting",
]


class NxtRemoteActionPurpose(str, Enum):
    """Remote action purpose values."""

    DATA_COLLECTION = "DATA_COLLECTION"
    REMEDIATION = "REMEDIATION"


class NxtRemoteActionRunAsOption(str, Enum):
    """Remote action run-as options."""

    LOCAL_SYSTEM = "LOCAL_SYSTEM"
    INTERACTIVE_USER = "INTERACTIVE_USER"
    DELEGATE_TO_SERVICE = "DELEGATE_TO_SERVICE"


class NxtRemoteActionInput(BaseModel):
    """Remote action input parameter metadata."""

    id: str
    name: str
    description: str | None = None
    usedByWindows: bool
    usedByMacOs: bool
    options: list[str]
    allowCustomValue: bool


class NxtRemoteActionOutput(BaseModel):
    """Remote action output parameter metadata."""

    id: str
    name: str
    type: str
    description: str | None = None
    usedByWindows: bool
    usedByMacOs: bool


class NxtRemoteActionTargeting(BaseModel):
    """Remote action targeting metadata."""

    apiEnabled: bool
    manualEnabled: bool
    workflowEnabled: bool
    manualAllowMultipleDevices: bool


class NxtRemoteActionScriptInfo(BaseModel):
    """Remote action script metadata."""

    executionServiceDelegate: str | None = None
    runAs: NxtRemoteActionRunAsOption
    timeoutSeconds: int
    hasScriptWindows: bool
    hasScriptMacOs: bool
    inputs: list[NxtRemoteActionInput] = Field(default_factory=list)
    outputs: list[NxtRemoteActionOutput] = Field(default_factory=list)


class NxtRemoteAction(BaseModel):
    """Remote action configuration metadata."""

    id: str
    uuid: str
    name: str
    description: str | None = None
    origin: str
    builtInContentVersion: str | None = None
    purpose: list[NxtRemoteActionPurpose]
    targeting: NxtRemoteActionTargeting
    scriptInfo: NxtRemoteActionScriptInfo
