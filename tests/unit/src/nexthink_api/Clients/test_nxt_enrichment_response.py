"""Unit tests for Enrichment response parsing."""

from http import HTTPStatus

import pytest

from nexthink_api import (
    NxtApiException,
    NxtBadRequestResponse,
    NxtEndpoint,
    NxtForbiddenResponse,
    NxtInvalidTokenRequest,
    NxtPartialSuccessResponse,
    NxtSuccessResponse,
)
from nexthink_api.Clients import NxtResponse


def _mock_enrichment_response(
    mocker: object,
    status_code: HTTPStatus,
    json_data: dict | None = None,
    reason: str = "Forbidden",
) -> object:
    response = mocker.Mock()
    response.url = NxtEndpoint.Enrichment.value
    response.status_code = status_code
    response.reason = reason
    response.json.return_value = json_data or {}
    return response


def _object_error_payload(device_name: str = "DEVICE-1") -> dict:
    return {
        "identification": [
            {
                "name": "device/device/name",
                "value": device_name,
            }
        ],
        "errors": [
            {
                "message": "Wrong type for field",
                "code": "ENRICH_011",
            }
        ],
    }


def test_enrichment_ok_response_returns_success(mocker: object) -> None:
    """Enrichment 200 responses use the success model."""
    response = _mock_enrichment_response(mocker, HTTPStatus.OK)

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtSuccessResponse)


def test_enrichment_multi_status_response_parses_partial_success(mocker: object) -> None:
    """Enrichment 207 responses keep individual object errors."""
    data = {
        "status": "partial_success",
        "errors": [_object_error_payload()],
    }
    response = _mock_enrichment_response(mocker, HTTPStatus.MULTI_STATUS, data)

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtPartialSuccessResponse)
    assert value.errors[0].identification[0].value == "DEVICE-1"
    assert value.errors[0].errors[0].code == "ENRICH_011"


def test_enrichment_bad_request_response_parses_object_errors(mocker: object) -> None:
    """Enrichment 400 responses keep all object errors."""
    data = {
        "status": "error",
        "errors": [
            _object_error_payload("DEVICE-1"),
            _object_error_payload("DEVICE-2"),
        ],
    }
    response = _mock_enrichment_response(mocker, HTTPStatus.BAD_REQUEST, data)

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtBadRequestResponse)
    assert [error.identification[0].value for error in value.errors] == ["DEVICE-1", "DEVICE-2"]


def test_enrichment_unauthorized_response_returns_invalid_token(mocker: object) -> None:
    """Enrichment 401 response uses the shared invalid token model."""
    response = _mock_enrichment_response(mocker, HTTPStatus.UNAUTHORIZED)

    assert isinstance(NxtResponse().from_response(response), NxtInvalidTokenRequest)


def test_enrichment_forbidden_response_preserves_reason(mocker: object) -> None:
    """Enrichment 403 response keeps the HTTP reason as message."""
    response = _mock_enrichment_response(mocker, HTTPStatus.FORBIDDEN, reason="Missing permission")

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtForbiddenResponse)
    assert value.message == "Missing permission"


def test_enrichment_response_rejects_non_json_body(mocker: object) -> None:
    """Enrichment JSON responses reject non-JSON bodies with context."""
    response = mocker.Mock()
    response.url = NxtEndpoint.Enrichment.value
    response.status_code = HTTPStatus.MULTI_STATUS
    response.text = "<html>proxy error</html>"
    response.json.side_effect = ValueError("Invalid JSON")

    with pytest.raises(NxtApiException) as error:
        NxtResponse().from_response(response)

    message = str(error.value)
    assert "Enrichment response body is not valid JSON" in message
    assert "status_code=" in message
    assert "<html>proxy error</html>" in message
