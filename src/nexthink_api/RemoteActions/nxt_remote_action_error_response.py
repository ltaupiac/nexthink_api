"""Remote Actions API error response model."""

from pydantic import BaseModel, Field

__all__ = ["NxtRemoteActionErrorResponse"]


class NxtRemoteActionErrorResponse(BaseModel):
    """Error details returned by the Remote Actions API."""

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
