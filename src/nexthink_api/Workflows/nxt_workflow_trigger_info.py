"""Workflows API trigger info model."""
# ruff: noqa: N815 - Field names follow the official Workflows API schema.

from pydantic import BaseModel

__all__ = ["NxtWorkflowTriggerInfo"]


class NxtWorkflowTriggerInfo(BaseModel):
    """Optional trigger metadata described by the Workflows API models."""

    externalReference: str | None = None
    internalSource: str | None = None
    externalSource: str | None = None
    reason: str | None = None
    extra: str | None = None
