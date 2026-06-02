"""Unit tests for Data Management error responses."""

import pytest
from pydantic import ValidationError

from nexthink_api.DataManagement import NxtDataManagementErrorCode, NxtDataManagementErrorResponse


class TestNxtDataManagementErrorResponse:
    """Test NxtDataManagementErrorResponse."""

    def test_error_response_accepts_error_code(self) -> None:
        """Error response accepts error code enum."""
        response = NxtDataManagementErrorResponse(
            code=NxtDataManagementErrorCode.INVALID_REQUEST,
            message="Schema validation failed.",
        )

        assert response.code == NxtDataManagementErrorCode.INVALID_REQUEST
        assert response.message == "Schema validation failed."
        assert response.request_id is None

    def test_error_response_accepts_request_id(self) -> None:
        """Error response accepts response request id."""
        response = NxtDataManagementErrorResponse(
            code=NxtDataManagementErrorCode.INTERNAL_ERROR,
            message="Unexpected server error.",
            request_id="22222222-2222-2222-2222-222222222222",
        )

        assert response.request_id == "22222222-2222-2222-2222-222222222222"

    def test_error_response_parses_error_code_from_string(self) -> None:
        """Error response parses error code from string."""
        response = NxtDataManagementErrorResponse(
            code="FEATURE_NOT_ENABLED",
            message="The Data Management API is not enabled for this tenant.",
        )

        assert response.code == NxtDataManagementErrorCode.FEATURE_NOT_ENABLED

    @pytest.mark.parametrize("error_code", list(NxtDataManagementErrorCode))
    def test_error_response_parses_documented_error_codes(
            self,
            error_code: NxtDataManagementErrorCode,
    ) -> None:
        """Error response parses every documented error code."""
        response = NxtDataManagementErrorResponse(
            code=error_code.value,
            message=f"{error_code.value} message.",
        )

        assert response.code == error_code

    def test_error_response_rejects_unknown_error_code(self) -> None:
        """Error response rejects unknown error code."""
        with pytest.raises(ValidationError):
            NxtDataManagementErrorResponse(code="UNKNOWN", message="Unknown error.")

    def test_error_code_matches_documented_values(self) -> None:
        """Error code enum matches documented Data Management values."""
        values = {error_code.value for error_code in NxtDataManagementErrorCode}

        assert values == {
            "EMPTY_REQUEST",
            "BATCH_SIZE_EXCEEDED",
            "INVALID_REQUEST",
            "EMPTY_TENANT",
            "FEATURE_NOT_ENABLED",
            "INTERNAL_ERROR",
        }
