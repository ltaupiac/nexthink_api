"""Spark API handoff conversation request model."""

from pydantic import BaseModel

from nexthink_api.Spark.nxt_spark_message_dto import NxtSparkMessageDTO

__all__ = ["NxtSparkHandoffConversationMessageRequest"]


class NxtSparkHandoffConversationMessageRequest(BaseModel):
    """Request body used to hand off a user conversation to Spark."""

    message: NxtSparkMessageDTO
    metadata: dict[str, str] | None = None
