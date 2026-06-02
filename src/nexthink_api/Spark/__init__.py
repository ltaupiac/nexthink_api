"""Models for the Nexthink Spark API."""

from nexthink_api.Spark.nxt_spark_error_response import NxtSparkErrorResponse
from nexthink_api.Spark.nxt_spark_handoff_conversation_message_request import (
    NxtSparkHandoffConversationMessageRequest,
)
from nexthink_api.Spark.nxt_spark_handoff_success_response import NxtSparkHandoffSuccessResponse
from nexthink_api.Spark.nxt_spark_message_dto import NxtSparkMessageDTO
from nexthink_api.Spark.nxt_spark_parts import NxtSparkFilePartByContent, NxtSparkPartType, NxtSparkTextPartDTO

__all__ = [
    "NxtSparkErrorResponse",
    "NxtSparkFilePartByContent",
    "NxtSparkHandoffConversationMessageRequest",
    "NxtSparkHandoffSuccessResponse",
    "NxtSparkMessageDTO",
    "NxtSparkPartType",
    "NxtSparkTextPartDTO",
]
