"""Spark API handoff success response model."""

from pydantic import BaseModel

__all__ = ["NxtSparkHandoffSuccessResponse"]


class NxtSparkHandoffSuccessResponse(BaseModel):
    """Typed success marker for Spark handoff 204 No Content responses."""

    accepted: bool = True
