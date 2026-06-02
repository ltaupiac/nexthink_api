"""Unit tests for Spark handoff request models."""

import pytest
from pydantic import ValidationError

from nexthink_api import (
    NxtSparkFilePartByContent,
    NxtSparkHandoffConversationMessageRequest,
    NxtSparkMessageDTO,
    NxtSparkPartType,
    NxtSparkTextPartDTO,
)


def test_handoff_request_accepts_text_and_file_parts() -> None:
    """Spark handoff request accepts the documented message part shapes."""
    request = NxtSparkHandoffConversationMessageRequest(
        metadata={"ticket": "INC001"},
        message=NxtSparkMessageDTO(
            parts=[
                NxtSparkTextPartDTO(text="I need help"),
                NxtSparkFilePartByContent(fileContent="Zm9v", mimeType="text/plain"),
            ],
        ),
    )

    assert request.model_dump(mode="json", exclude_none=True) == {
        "metadata": {"ticket": "INC001"},
        "message": {
            "parts": [
                {"type": "TEXT", "text": "I need help"},
                {"type": "FILE", "fileContent": "Zm9v", "mimeType": "text/plain"},
            ],
        },
    }


def test_message_rejects_empty_parts() -> None:
    """Spark message requires at least one part."""
    with pytest.raises(ValidationError):
        NxtSparkMessageDTO(parts=[])


def test_text_part_rejects_empty_text() -> None:
    """Spark text part follows the documented minLength."""
    with pytest.raises(ValidationError):
        NxtSparkTextPartDTO(text="")


def test_part_type_values_follow_documentation() -> None:
    """Spark part type enum exposes documented values."""
    assert NxtSparkPartType.TEXT.value == "TEXT"
    assert NxtSparkPartType.FILE.value == "FILE"
