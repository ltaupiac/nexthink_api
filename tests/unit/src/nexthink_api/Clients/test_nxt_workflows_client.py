"""Unit tests for the internal Workflows client."""

import pytest

from nexthink_api import (
    NxtEndpoint,
    NxtWorkflowDependency,
    NxtWorkflowDeviceData,
    NxtWorkflowExecutionRequest,
    NxtWorkflowExternalIdsExecutionRequest,
    NxtWorkflowThinkletTriggerRequest,
    NxtWorkflowTriggerMethod,
)
from nexthink_api.Clients.nxt_workflows_client import NxtWorkflowsClient


def test_execute_posts_v1_workflow_request(mocker: object) -> None:
    """Workflow v1 execution validates POST support and delegates transport POST."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.post.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_workflows_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtWorkflowsClient(api_client)
    request = NxtWorkflowExecutionRequest(
        workflowId="#workflow",
        devices=["8d868f83-547c-471a-bb7b-452211ed38a1"],
    )

    value = client.execute(request, source="example")

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.Workflow, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Workflow)
    api_client.transport.post.assert_called_once_with(
        "/api/v1/workflows/execute",
        headers={"Authorization": "Bearer token", "Source": "example"},
        json={
            "workflowId": "#workflow",
            "devices": ["8d868f83-547c-471a-bb7b-452211ed38a1"],
            "users": [],
        },
    )


def test_execute_with_external_ids_posts_v2_workflow_request(mocker: object) -> None:
    """Workflow v2 execution owns the external IDs endpoint."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.post.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_workflows_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtWorkflowsClient(api_client)
    request = NxtWorkflowExternalIdsExecutionRequest(
        workflowId="#workflow",
        devices=[NxtWorkflowDeviceData(name="macbook-001")],
    )

    value = client.execute_with_external_ids(request)

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.WorkflowV2, "POST")
    api_client.transport.post.assert_called_once_with(
        "/api/v2/workflows/execute",
        headers={"Authorization": "Bearer token"},
        json={"workflowId": "#workflow", "devices": [{"name": "macbook-001"}], "users": []},
    )


def test_trigger_thinklet_posts_dynamic_path(mocker: object) -> None:
    """Workflow thinklet trigger builds the documented dynamic path."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.post.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_workflows_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtWorkflowsClient(api_client)

    value = client.trigger_thinklet(
        "workflow-uuid",
        "execution-uuid",
        NxtWorkflowThinkletTriggerRequest(parameters={"approval": "yes"}),
    )

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.WorkflowThinkletTrigger, "POST")
    api_client.transport.post.assert_called_once_with(
        "/api/v1/workflows/workflows/workflow-uuid/execution/execution-uuid/trigger",
        headers={"Authorization": "Bearer token"},
        json={"parameters": {"approval": "yes"}},
    )


def test_list_gets_workflow_inventory(mocker: object) -> None:
    """Workflow list sends documented query filters."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.get.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_workflows_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtWorkflowsClient(api_client)

    value = client.list(
        dependency=NxtWorkflowDependency.USER,
        trigger_method=NxtWorkflowTriggerMethod.API,
        fetch_only_active_workflows=True,
    )

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.Workflows, "GET")
    api_client.transport.get.assert_called_once_with(
        "/api/v1/workflows",
        headers={"Authorization": "Bearer token"},
        params={"dependency": "USER", "triggerMethod": "API", "fetchOnlyActiveWorkflows": True},
    )


def test_get_fetches_workflow_details_by_nql_id(mocker: object) -> None:
    """Workflow get sends the documented nqlId query parameter."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.get.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_workflows_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtWorkflowsClient(api_client)

    value = client.get("#workflow")

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.WorkflowDetails, "GET")
    api_client.transport.get.assert_called_once_with(
        "/api/v1/workflows/details",
        headers={"Authorization": "Bearer token"},
        params={"nqlId": "#workflow"},
    )


def test_execute_rejects_unsupported_post_method(mocker: object) -> None:
    """Workflow execution fails before sending HTTP when POST is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    client = NxtWorkflowsClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.execute(NxtWorkflowExecutionRequest(workflowId="#workflow", users=["S-1-5-21-1"]))

    api_client.transport.post.assert_not_called()
