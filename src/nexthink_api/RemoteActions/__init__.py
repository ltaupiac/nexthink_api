"""Models for the Nexthink Remote Actions API."""

from nexthink_api.RemoteActions.nxt_remote_action_error_response import NxtRemoteActionErrorResponse
from nexthink_api.RemoteActions.nxt_remote_action_execution_request import NxtRemoteActionExecutionRequest
from nexthink_api.RemoteActions.nxt_remote_action_execution_response import NxtRemoteActionExecutionResponse
from nexthink_api.RemoteActions.nxt_remote_action_models import (
    NxtRemoteAction,
    NxtRemoteActionInput,
    NxtRemoteActionOutput,
    NxtRemoteActionPurpose,
    NxtRemoteActionRunAsOption,
    NxtRemoteActionScriptInfo,
    NxtRemoteActionTargeting,
)
from nexthink_api.RemoteActions.nxt_remote_action_trigger_info_request import NxtRemoteActionTriggerInfoRequest

__all__ = [
    "NxtRemoteAction",
    "NxtRemoteActionErrorResponse",
    "NxtRemoteActionExecutionRequest",
    "NxtRemoteActionExecutionResponse",
    "NxtRemoteActionInput",
    "NxtRemoteActionOutput",
    "NxtRemoteActionPurpose",
    "NxtRemoteActionRunAsOption",
    "NxtRemoteActionScriptInfo",
    "NxtRemoteActionTargeting",
    "NxtRemoteActionTriggerInfoRequest",
]
