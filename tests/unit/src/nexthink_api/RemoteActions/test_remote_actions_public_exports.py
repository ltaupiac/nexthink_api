"""Unit tests for Remote Actions public exports."""

import nexthink_api
from nexthink_api import (
    NxtRemoteAction,
    NxtRemoteActionErrorResponse,
    NxtRemoteActionExecutionRequest,
    NxtRemoteActionExecutionResponse,
    NxtRemoteActionInput,
    NxtRemoteActionOutput,
    NxtRemoteActionPurpose,
    NxtRemoteActionRunAsOption,
    NxtRemoteActionScriptInfo,
    NxtRemoteActionTargeting,
    NxtRemoteActionTriggerInfoRequest,
)


def test_remote_actions_classes_are_exported_from_root_package() -> None:
    """Remote Actions classes are exported from nexthink_api."""
    assert nexthink_api.NxtRemoteAction is NxtRemoteAction
    assert nexthink_api.NxtRemoteActionErrorResponse is NxtRemoteActionErrorResponse
    assert nexthink_api.NxtRemoteActionExecutionRequest is NxtRemoteActionExecutionRequest
    assert nexthink_api.NxtRemoteActionExecutionResponse is NxtRemoteActionExecutionResponse
    assert nexthink_api.NxtRemoteActionInput is NxtRemoteActionInput
    assert nexthink_api.NxtRemoteActionOutput is NxtRemoteActionOutput
    assert nexthink_api.NxtRemoteActionPurpose is NxtRemoteActionPurpose
    assert nexthink_api.NxtRemoteActionRunAsOption is NxtRemoteActionRunAsOption
    assert nexthink_api.NxtRemoteActionScriptInfo is NxtRemoteActionScriptInfo
    assert nexthink_api.NxtRemoteActionTargeting is NxtRemoteActionTargeting
    assert nexthink_api.NxtRemoteActionTriggerInfoRequest is NxtRemoteActionTriggerInfoRequest
