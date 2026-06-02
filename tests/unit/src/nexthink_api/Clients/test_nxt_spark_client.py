"""Unit tests for the internal Spark client."""

import pytest

from nexthink_api import (
    NxtEndpoint,
    NxtSparkHandoffConversationMessageRequest,
    NxtSparkMessageDTO,
    NxtSparkTextPartDTO,
)
from nexthink_api.Clients.nxt_spark_client import NxtSparkClient


def _request() -> NxtSparkHandoffConversationMessageRequest:
    """Return a minimal valid Spark handoff request."""
    return NxtSparkHandoffConversationMessageRequest(
        message=NxtSparkMessageDTO(parts=[NxtSparkTextPartDTO(text="I need help")]),
    )


def test_handoff_posts_spark_request_with_required_headers(mocker: object) -> None:
    """Spark handoff validates POST support and delegates transport POST."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token", "Content-Type": "application/json"}
    api_client.check_method.return_value = True
    api_client.transport.post.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_spark_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtSparkClient(api_client)

    value = client.handoff(_request(), user_principal_name="user@example.com", timezone="Europe/Paris")

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.SparkHandoff, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.SparkHandoff)
    api_client.transport.post.assert_called_once_with(
        "/api/v1/spark/handoff",
        headers={
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
            "User-Principal-Name": "user@example.com",
            "Timezone": "Europe/Paris",
        },
        json={"message": {"parts": [{"type": "TEXT", "text": "I need help"}]}},
    )


def test_handoff_rejects_missing_user_principal_name(mocker: object) -> None:
    """Spark handoff fails before sending HTTP when UPN is missing."""
    api_client = mocker.Mock()
    client = NxtSparkClient(api_client)

    with pytest.raises(ValueError, match="user_principal_name is required"):
        client.handoff(_request(), user_principal_name="")

    api_client.transport.post.assert_not_called()


def test_handoff_rejects_unsupported_post_method(mocker: object) -> None:
    """Spark handoff fails before sending HTTP when POST is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    client = NxtSparkClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.handoff(_request(), user_principal_name="user@example.com")

    api_client.transport.post.assert_not_called()
