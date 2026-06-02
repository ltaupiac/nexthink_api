"""Unit tests for Spark public package exports."""

import nexthink_api
from nexthink_api.Spark import (
    NxtSparkErrorResponse,
    NxtSparkFilePartByContent,
    NxtSparkHandoffConversationMessageRequest,
    NxtSparkHandoffSuccessResponse,
    NxtSparkMessageDTO,
    NxtSparkPartType,
    NxtSparkTextPartDTO,
)


def test_spark_models_are_exported_from_domain_package() -> None:
    """Spark models are importable from the domain package."""
    assert NxtSparkErrorResponse.__name__ == "NxtSparkErrorResponse"
    assert NxtSparkFilePartByContent.__name__ == "NxtSparkFilePartByContent"
    assert NxtSparkHandoffConversationMessageRequest.__name__ == "NxtSparkHandoffConversationMessageRequest"
    assert NxtSparkHandoffSuccessResponse.__name__ == "NxtSparkHandoffSuccessResponse"
    assert NxtSparkMessageDTO.__name__ == "NxtSparkMessageDTO"
    assert NxtSparkPartType.__name__ == "NxtSparkPartType"
    assert NxtSparkTextPartDTO.__name__ == "NxtSparkTextPartDTO"


def test_spark_models_are_exported_from_root_package() -> None:
    """Spark models are available from the historical root package."""
    assert nexthink_api.NxtSparkErrorResponse is NxtSparkErrorResponse
    assert nexthink_api.NxtSparkFilePartByContent is NxtSparkFilePartByContent
    assert nexthink_api.NxtSparkHandoffConversationMessageRequest is NxtSparkHandoffConversationMessageRequest
    assert nexthink_api.NxtSparkHandoffSuccessResponse is NxtSparkHandoffSuccessResponse
    assert nexthink_api.NxtSparkMessageDTO is NxtSparkMessageDTO
    assert nexthink_api.NxtSparkPartType is NxtSparkPartType
    assert nexthink_api.NxtSparkTextPartDTO is NxtSparkTextPartDTO
