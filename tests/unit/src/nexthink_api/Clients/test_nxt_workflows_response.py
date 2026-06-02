"""Unit tests for Workflows response parsing."""

from http import HTTPStatus

from nexthink_api import (
    NxtInvalidTokenRequest,
    NxtWorkflow,
    NxtWorkflowErrorResponse,
    NxtWorkflowExecutionResponse,
    NxtWorkflowThinkletTriggerResponse,
)
from nexthink_api.Clients import NxtResponse


def _workflow_payload() -> dict:
    """Return a minimal documented Workflow payload."""
    return {
        "id": "#workflow",
        "uuid": "workflow-uuid",
        "name": "Workflow",
        "description": "Demo workflow",
        "status": "ACTIVE",
        "lastUpdateTime": "2026-05-25T10:00:00Z",
        "triggerMethods": ["API"],
        "versions": [],
    }


def test_execute_response_parses_execution_response(mocker: object) -> None:
    """Workflows v1 execute 200 response parses execution response."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/workflows/execute"
    response.status_code = HTTPStatus.OK
    response.json.return_value = {"requestUuid": "request-1", "executionsUuids": ["execution-1"]}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtWorkflowExecutionResponse)
    assert value.requestUuid == "request-1"


def test_external_ids_execute_response_parses_execution_response(mocker: object) -> None:
    """Workflows v2 execute 200 response parses execution response."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v2/workflows/execute"
    response.status_code = HTTPStatus.OK
    response.json.return_value = {"requestUuid": "request-1", "executionsUuids": ["execution-1"]}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtWorkflowExecutionResponse)


def test_thinklet_trigger_response_parses_response_list(mocker: object) -> None:
    """Workflows thinklet trigger 200 response parses response list."""
    response = mocker.Mock()
    response.url = (
        "https://tenant.api.eu.nexthink.cloud"
        "/api/v1/workflows/workflows/workflow-uuid/execution/execution-uuid/trigger"
    )
    response.status_code = HTTPStatus.OK
    response.json.return_value = [{"requestUuid": "request-1"}]

    value = NxtResponse().from_response(response)

    assert isinstance(value, list)
    assert isinstance(value[0], NxtWorkflowThinkletTriggerResponse)


def test_list_response_parses_workflow_list(mocker: object) -> None:
    """Workflows list 200 response parses workflow metadata list."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/workflows"
    response.status_code = HTTPStatus.OK
    response.json.return_value = [_workflow_payload()]

    value = NxtResponse().from_response(response)

    assert isinstance(value, list)
    assert isinstance(value[0], NxtWorkflow)
    assert value[0].id == "#workflow"


def test_details_response_parses_workflow_list(mocker: object) -> None:
    """Workflows details 200 response resolves to the details endpoint."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/workflows/details"
    response.status_code = HTTPStatus.OK
    response.json.return_value = [_workflow_payload()]

    value = NxtResponse().from_response(response)

    assert isinstance(value, list)
    assert isinstance(value[0], NxtWorkflow)


def test_details_response_accepts_single_workflow_object(mocker: object) -> None:
    """Workflows live API may return one object for details instead of a list."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/workflows/details"
    response.status_code = HTTPStatus.OK
    response.json.return_value = _workflow_payload()

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtWorkflow)
    assert value.id == "#workflow"


def test_error_response_parses_workflow_error(mocker: object) -> None:
    """Workflows error response parses documented error schema."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/workflows/execute"
    response.status_code = HTTPStatus.BAD_REQUEST
    response.json.return_value = {"code": "INVALID_REQUEST", "details": "Invalid request"}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtWorkflowErrorResponse)
    assert value.code == "INVALID_REQUEST"


def test_unauthorized_response_returns_invalid_token(mocker: object) -> None:
    """Workflows 401 response keeps the existing invalid token model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/workflows/execute"
    response.status_code = HTTPStatus.UNAUTHORIZED

    assert isinstance(NxtResponse().from_response(response), NxtInvalidTokenRequest)
