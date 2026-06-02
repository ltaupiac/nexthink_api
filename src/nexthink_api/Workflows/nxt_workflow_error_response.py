"""Workflows API error response model."""

from pydantic import BaseModel, Field

__all__ = ["NxtWorkflowErrorResponse"]


class NxtWorkflowErrorResponse(BaseModel):
    """Error details returned by the Workflows API."""

    code: str = Field(min_length=1)
    details: str
