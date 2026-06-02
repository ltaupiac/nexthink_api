"""Unit tests for Spark response parsing."""

from http import HTTPStatus

from nexthink_api import NxtInvalidTokenRequest, NxtSparkErrorResponse, NxtSparkHandoffSuccessResponse
from nexthink_api.Clients import NxtResponse


def test_handoff_success_response_parses_no_content(mocker: object) -> None:
    """Spark 204 response returns a typed success marker without parsing JSON."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/spark/handoff"
    response.status_code = HTTPStatus.NO_CONTENT

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtSparkHandoffSuccessResponse)
    assert value.accepted is True
    response.json.assert_not_called()


def test_handoff_success_response_accepts_live_ok_status(mocker: object) -> None:
    """Spark live API may return 200 even though the docs describe 204."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/spark/handoff"
    response.status_code = HTTPStatus.OK

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtSparkHandoffSuccessResponse)
    response.json.assert_not_called()


def test_error_response_parses_spark_error_json(mocker: object) -> None:
    """Spark documented error response parses message payload."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/spark/handoff"
    response.status_code = HTTPStatus.FORBIDDEN
    response.json.return_value = {"message": "Forbidden"}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtSparkErrorResponse)
    assert value.message == "Forbidden"


def test_error_response_synthesizes_message_for_non_json_body(mocker: object) -> None:
    """Spark undocumented error bodies still produce a typed error model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/spark/handoff"
    response.status_code = HTTPStatus.BAD_GATEWAY
    response.reason = "Bad gateway"
    response.text = ""
    response.json.side_effect = ValueError

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtSparkErrorResponse)
    assert value.message == "Bad gateway"


def test_unauthorized_response_returns_invalid_token(mocker: object) -> None:
    """Spark 401 response keeps the existing invalid token model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/spark/handoff"
    response.status_code = HTTPStatus.UNAUTHORIZED

    assert isinstance(NxtResponse().from_response(response), NxtInvalidTokenRequest)
