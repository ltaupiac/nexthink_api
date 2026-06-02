"""Models for the Nexthink Workflows API."""

from nexthink_api.Workflows.nxt_workflow_error_response import NxtWorkflowErrorResponse
from nexthink_api.Workflows.nxt_workflow_execution_request import NxtWorkflowExecutionRequest
from nexthink_api.Workflows.nxt_workflow_execution_response import NxtWorkflowExecutionResponse
from nexthink_api.Workflows.nxt_workflow_external_ids_execution_request import (
    NxtWorkflowDeviceData,
    NxtWorkflowExternalIdsExecutionRequest,
    NxtWorkflowUserData,
)
from nexthink_api.Workflows.nxt_workflow_models import (
    NxtWorkflow,
    NxtWorkflowDependency,
    NxtWorkflowStatus,
    NxtWorkflowTriggerMethod,
)
from nexthink_api.Workflows.nxt_workflow_thinklet_trigger_request import NxtWorkflowThinkletTriggerRequest
from nexthink_api.Workflows.nxt_workflow_thinklet_trigger_response import NxtWorkflowThinkletTriggerResponse
from nexthink_api.Workflows.nxt_workflow_trigger_info import NxtWorkflowTriggerInfo

__all__ = [
    "NxtWorkflow",
    "NxtWorkflowDependency",
    "NxtWorkflowDeviceData",
    "NxtWorkflowErrorResponse",
    "NxtWorkflowExecutionRequest",
    "NxtWorkflowExecutionResponse",
    "NxtWorkflowExternalIdsExecutionRequest",
    "NxtWorkflowStatus",
    "NxtWorkflowThinkletTriggerRequest",
    "NxtWorkflowThinkletTriggerResponse",
    "NxtWorkflowTriggerInfo",
    "NxtWorkflowTriggerMethod",
    "NxtWorkflowUserData",
]
