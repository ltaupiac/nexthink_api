"""Spark API error response model."""

from pydantic import BaseModel

__all__ = ["NxtSparkErrorResponse"]


class NxtSparkErrorResponse(BaseModel):
    """Error details returned by the Spark API."""

    message: str | None = None
