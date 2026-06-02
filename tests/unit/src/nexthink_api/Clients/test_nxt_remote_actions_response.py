"""Unit tests for Remote Actions response parsing."""

from http import HTTPStatus

from nexthink_api import (
    NxtInvalidTokenRequest,
    NxtRemoteAction,
    NxtRemoteActionErrorResponse,
    NxtRemoteActionExecutionResponse,
)
from nexthink_api.Clients import NxtResponse


def _remote_action_payload() -> dict:
    """Return a minimal documented RemoteAction payload."""
    return {
        "id": "#restart_service",
        "uuid": "remote-action-uuid",
        "name": "Restart service",
        "description": "Restart a service",
        "origin": "CUSTOM",
        "builtInContentVersion": "1.0.0",
        "purpose": ["REMEDIATION"],
        "targeting": {
            "apiEnabled": True,
            "manualEnabled": True,
            "workflowEnabled": False,
            "manualAllowMultipleDevices": True,
        },
        "scriptInfo": {
            "executionServiceDelegate": "NONE",
            "runAs": "LOCAL_SYSTEM",
            "timeoutSeconds": 300,
            "hasScriptWindows": True,
            "hasScriptMacOs": False,
            "inputs": [],
            "outputs": [],
        },
    }


def test_execute_response_parses_execution_response(mocker: object) -> None:
    """Remote Actions execute 200 response parses execution response."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/act/execute"
    response.status_code = HTTPStatus.OK
    response.json.return_value = {"requestId": "request-1", "expiresInMinutes": 60}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtRemoteActionExecutionResponse)
    assert value.requestId == "request-1"


def test_list_response_parses_remote_action_list(mocker: object) -> None:
    """Remote Actions list 200 response parses remote action metadata list."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/act/remote-action"
    response.status_code = HTTPStatus.OK
    response.json.return_value = [_remote_action_payload()]

    value = NxtResponse().from_response(response)

    assert isinstance(value, list)
    assert isinstance(value[0], NxtRemoteAction)
    assert value[0].id == "#restart_service"


def test_details_response_parses_remote_action(mocker: object) -> None:
    """Remote Actions details 200 response resolves to the specific details endpoint."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/act/remote-action/details"
    response.status_code = HTTPStatus.OK
    response.json.return_value = _remote_action_payload()

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtRemoteAction)
    assert value.id == "#restart_service"


def test_error_response_parses_remote_action_error(mocker: object) -> None:
    """Remote Actions error response parses documented error schema."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/act/execute"
    response.status_code = HTTPStatus.BAD_REQUEST
    response.json.return_value = {"code": "INVALID_REQUEST", "message": "Invalid request"}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtRemoteActionErrorResponse)
    assert value.code == "INVALID_REQUEST"


def test_unauthorized_response_returns_invalid_token(mocker: object) -> None:
    """Remote Actions 401 response keeps the existing invalid token model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/act/execute"
    response.status_code = HTTPStatus.UNAUTHORIZED

    assert isinstance(NxtResponse().from_response(response), NxtInvalidTokenRequest)
