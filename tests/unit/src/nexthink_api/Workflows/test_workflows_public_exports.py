"""Unit tests for Workflows public package exports."""

import nexthink_api
from nexthink_api.Workflows import (
    NxtWorkflow,
    NxtWorkflowDeviceData,
    NxtWorkflowErrorResponse,
    NxtWorkflowExecutionRequest,
    NxtWorkflowExecutionResponse,
    NxtWorkflowExternalIdsExecutionRequest,
    NxtWorkflowThinkletTriggerRequest,
    NxtWorkflowThinkletTriggerResponse,
)


def test_workflows_models_are_exported_from_domain_package() -> None:
    """Workflows models are importable from the domain package."""
    assert NxtWorkflow.__name__ == "NxtWorkflow"
    assert NxtWorkflowDeviceData.__name__ == "NxtWorkflowDeviceData"
    assert NxtWorkflowErrorResponse.__name__ == "NxtWorkflowErrorResponse"
    assert NxtWorkflowExecutionRequest.__name__ == "NxtWorkflowExecutionRequest"
    assert NxtWorkflowExecutionResponse.__name__ == "NxtWorkflowExecutionResponse"
    assert NxtWorkflowExternalIdsExecutionRequest.__name__ == "NxtWorkflowExternalIdsExecutionRequest"
    assert NxtWorkflowThinkletTriggerRequest.__name__ == "NxtWorkflowThinkletTriggerRequest"
    assert NxtWorkflowThinkletTriggerResponse.__name__ == "NxtWorkflowThinkletTriggerResponse"


def test_workflows_models_are_exported_from_root_package() -> None:
    """Workflows models are available from the historical root package."""
    assert nexthink_api.NxtWorkflow is NxtWorkflow
    assert nexthink_api.NxtWorkflowDeviceData is NxtWorkflowDeviceData
    assert nexthink_api.NxtWorkflowErrorResponse is NxtWorkflowErrorResponse
    assert nexthink_api.NxtWorkflowExecutionRequest is NxtWorkflowExecutionRequest
    assert nexthink_api.NxtWorkflowExecutionResponse is NxtWorkflowExecutionResponse
    assert nexthink_api.NxtWorkflowExternalIdsExecutionRequest is NxtWorkflowExternalIdsExecutionRequest
    assert nexthink_api.NxtWorkflowThinkletTriggerRequest is NxtWorkflowThinkletTriggerRequest
    assert nexthink_api.NxtWorkflowThinkletTriggerResponse is NxtWorkflowThinkletTriggerResponse
