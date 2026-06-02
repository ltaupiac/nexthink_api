"""Spark API message part models."""
# ruff: noqa: N815 - Field names follow the official Spark API schema.

from enum import Enum

from pydantic import BaseModel, Field

__all__ = ["NxtSparkFilePartByContent", "NxtSparkPartType", "NxtSparkTextPartDTO"]


class NxtSparkPartType(str, Enum):
    """Supported Spark message part types."""

    TEXT = "TEXT"
    FILE = "FILE"


class NxtSparkTextPartDTO(BaseModel):
    """Text message part handed off to Spark."""

    type: NxtSparkPartType = NxtSparkPartType.TEXT
    text: str = Field(min_length=1)


class NxtSparkFilePartByContent(BaseModel):
    """File message part handed off to Spark by content."""

    type: NxtSparkPartType = NxtSparkPartType.FILE
    fileContent: str
    mimeType: str = Field(min_length=1)
