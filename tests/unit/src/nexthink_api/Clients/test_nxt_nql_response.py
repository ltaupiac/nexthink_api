"""Unit tests for NQL response parsing."""

from http import HTTPStatus

import pytest

from nexthink_api import (
    NxtApiException,
    NxtEndpoint,
    NxtInvalidTokenRequest,
    NxtNqlApiExecuteV2Response,
    NxtNqlApiExportResponse,
    NxtNqlApiStatusResponse,
)
from nexthink_api.Clients import NxtResponse
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse


def _mock_nql_response(mocker: object, endpoint: NxtEndpoint, json_data: dict) -> object:
    response = mocker.Mock()
    response.url = endpoint.value
    response.status_code = HTTPStatus.OK
    response.json.return_value = json_data
    return response


def test_execute_v2_success_response_parses_execute_model(mocker: object) -> None:
    """NQL v2 execute success responses use the v2 execute model."""
    response = _mock_nql_response(
        mocker,
        NxtEndpoint.NqlV2,
        {
            "queryId": "query-1",
            "executedQuery": "devices | list",
            "rows": 1,
            "executionDateTime": "2023-03-07T15:56:02",
            "data": [{"device.name": "DEVICE-1"}],
        },
    )

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtNqlApiExecuteV2Response)
    assert value.queryId == "query-1"
    assert value.data == [{"device.name": "DEVICE-1"}]


def test_export_success_response_parses_export_model(mocker: object) -> None:
    """NQL export success responses use the export model."""
    response = _mock_nql_response(
        mocker,
        NxtEndpoint.NqlExport,
        {"exportId": "export-1"},
    )

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtNqlApiExportResponse)
    assert value.exportId == "export-1"


def test_status_success_response_parses_status_model(mocker: object) -> None:
    """NQL status success responses use the status model."""
    response = _mock_nql_response(
        mocker,
        NxtEndpoint.NqlStatus,
        {
            "status": "SUBMITTED",
            "resultsFileUrl": "https://www.fileresults.com/data/value/id?token=1234566",
            "errorDescription": "An error description",
        },
    )

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtNqlApiStatusResponse)
    assert value.status.value == "SUBMITTED"


def test_unauthorized_response_returns_invalid_token(mocker: object) -> None:
    """NQL 401 response uses the shared invalid token model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v2/nql/execute"
    response.status_code = HTTPStatus.UNAUTHORIZED

    assert isinstance(NxtResponse().from_response(response), NxtInvalidTokenRequest)


def test_forbidden_response_keeps_nql_error_response(mocker: object) -> None:
    """Other documented NQL API errors keep the NQL error model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v2/nql/execute"
    response.status_code = HTTPStatus.FORBIDDEN
    response.reason = "Forbidden"

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtErrorResponse)
    assert value.code == HTTPStatus.FORBIDDEN


def test_success_response_rejects_non_json_body(mocker: object) -> None:
    """NQL JSON success responses reject non-JSON bodies with context."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v2/nql/execute"
    response.status_code = HTTPStatus.OK
    response.text = "<html>proxy error</html>"
    response.json.side_effect = ValueError("Invalid JSON")

    with pytest.raises(NxtApiException) as error:
        NxtResponse().from_response(response)

    message = str(error.value)
    assert "NQL response body is not valid JSON" in message
    assert "status_code=" in message
    assert "<html>proxy error</html>" in message
