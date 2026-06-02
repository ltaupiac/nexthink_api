"""Spark API message model."""

from pydantic import BaseModel, Field

from nexthink_api.Spark.nxt_spark_parts import NxtSparkFilePartByContent, NxtSparkTextPartDTO

__all__ = ["NxtSparkMessageDTO"]


class NxtSparkMessageDTO(BaseModel):
    """Message payload handed off to Spark."""

    parts: list[NxtSparkTextPartDTO | NxtSparkFilePartByContent] = Field(min_length=1)
