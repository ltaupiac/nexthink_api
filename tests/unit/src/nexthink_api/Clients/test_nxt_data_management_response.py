"""Unit tests for Data Management response factory."""

from http import HTTPStatus
from unittest.mock import Mock

import pytest

from nexthink_api import (
    NxtApiException,
    NxtDataManagementErrorCode,
    NxtDataManagementErrorResponse,
    NxtDataManagementBatchStatus,
    NxtDataManagementDeviceStatus,
    NxtDeviceDeletionResponse,
    NxtEndpoint,
    NxtInvalidTokenRequest,
)
from nexthink_api.Clients import NxtResponse


class TestNxtDataManagementResponse:
    """Test Data Management response factory."""

    @staticmethod
    def _mock_response(mocker: object, status: int, json_data: dict | None = None) -> Mock:
        response = mocker.Mock()
        response.status_code = status
        response.url = NxtEndpoint.DataManagement.value
        response.headers = {}
        if json_data is not None:
            response.json = mocker.Mock(return_value=json_data)
        return response

    def test_data_management_response_builds_accepted_response(self, mocker: object) -> None:
        """Data Management response builds accepted response."""
        response = self._mock_response(
            mocker,
            HTTPStatus.ACCEPTED,
            {
                "scheduledCount": 1,
                "status": "ACCEPTED",
                "devices": [
                    {
                        "uid": "00000000-0000-0000-0000-000000000000",
                        "name": "DEVICE-1",
                        "status": "SCHEDULED",
                    }
                ],
            },
        )

        value = NxtResponse().from_response(response)

        assert isinstance(value, NxtDeviceDeletionResponse)
        assert value.status == NxtDataManagementBatchStatus.ACCEPTED
        assert value.devices[0].status == NxtDataManagementDeviceStatus.SCHEDULED
        assert value.request_id is None

    def test_data_management_response_preserves_success_request_id(self, mocker: object) -> None:
        """Data Management success response preserves x-request-id."""
        response = self._mock_response(
            mocker,
            HTTPStatus.ACCEPTED,
            {
                "scheduledCount": 1,
                "status": "ACCEPTED",
                "devices": [
                    {
                        "uid": "00000000-0000-0000-0000-000000000000",
                        "name": "DEVICE-1",
                        "status": "SCHEDULED",
                    }
                ],
            },
        )
        response.headers = {"x-request-id": "11111111-1111-1111-1111-111111111111"}

        value = NxtResponse().from_response(response)

        assert isinstance(value, NxtDeviceDeletionResponse)
        assert value.request_id == "11111111-1111-1111-1111-111111111111"

    @pytest.mark.parametrize(
        ("status", "code"),
        [
            (HTTPStatus.BAD_REQUEST, NxtDataManagementErrorCode.INVALID_REQUEST),
            (HTTPStatus.FORBIDDEN, NxtDataManagementErrorCode.FEATURE_NOT_ENABLED),
            (HTTPStatus.INTERNAL_SERVER_ERROR, NxtDataManagementErrorCode.INTERNAL_ERROR),
        ],
    )
    def test_data_management_response_builds_error_response(
            self,
            mocker: object,
            status: HTTPStatus,
            code: NxtDataManagementErrorCode,
    ) -> None:
        """Data Management response builds error response."""
        response = self._mock_response(
            mocker,
            status,
            {
                "code": code.value,
                "message": "Error message.",
            },
        )

        value = NxtResponse().from_response(response)

        assert isinstance(value, NxtDataManagementErrorResponse)
        assert value.code == code
        assert value.message == "Error message."
        assert value.request_id is None

    def test_data_management_response_preserves_error_request_id(self, mocker: object) -> None:
        """Data Management error response preserves x-request-id."""
        response = self._mock_response(
            mocker,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {
                "code": NxtDataManagementErrorCode.INTERNAL_ERROR.value,
                "message": "Unexpected server error.",
            },
        )
        response.headers = {"x-request-id": "22222222-2222-2222-2222-222222222222"}

        value = NxtResponse().from_response(response)

        assert isinstance(value, NxtDataManagementErrorResponse)
        assert value.request_id == "22222222-2222-2222-2222-222222222222"

    def test_data_management_response_builds_invalid_token_response(self, mocker: object) -> None:
        """Data Management response builds invalid token response."""
        response = self._mock_response(mocker, HTTPStatus.UNAUTHORIZED)

        value = NxtResponse().from_response(response)

        assert isinstance(value, NxtInvalidTokenRequest)

    def test_data_management_response_rejects_unknown_status_code(self, mocker: object) -> None:
        """Data Management response rejects unknown status code."""
        response = self._mock_response(mocker, HTTPStatus.OK)

        with pytest.raises(NxtApiException):
            NxtResponse().from_response(response)

    @pytest.mark.parametrize(
        "status",
        [
            HTTPStatus.ACCEPTED,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        ],
    )
    def test_data_management_response_rejects_non_json_body(
            self,
            mocker: object,
            status: HTTPStatus,
    ) -> None:
        """Data Management response rejects non-JSON bodies with context."""
        response = self._mock_response(mocker, status)
        response.headers = {"x-request-id": "33333333-3333-3333-3333-333333333333"}
        response.text = "not json"
        response.json.side_effect = ValueError("Invalid JSON")

        with pytest.raises(NxtApiException) as error:
            NxtResponse().from_response(response)

        message = str(error.value)
        assert "Data Management response body is not valid JSON" in message
        assert "status_code=" in message
        assert "33333333-3333-3333-3333-333333333333" in message
