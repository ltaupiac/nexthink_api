"""Unit tests for Remote Actions inventory models."""

from nexthink_api import (
    NxtRemoteAction,
    NxtRemoteActionPurpose,
    NxtRemoteActionRunAsOption,
)


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
            "inputs": [
                {
                    "id": "StartType",
                    "name": "Start type",
                    "description": "Target start type",
                    "usedByWindows": True,
                    "usedByMacOs": False,
                    "options": ["Automatic", "Manual"],
                    "allowCustomValue": False,
                }
            ],
            "outputs": [
                {
                    "id": "status",
                    "name": "Status",
                    "type": "STRING",
                    "description": "Result",
                    "usedByWindows": True,
                    "usedByMacOs": False,
                }
            ],
        },
    }


def test_remote_action_model_accepts_documented_payload() -> None:
    """RemoteAction model parses documented inventory metadata."""
    remote_action = NxtRemoteAction.model_validate(_remote_action_payload())

    assert remote_action.id == "#restart_service"
    assert remote_action.purpose == [NxtRemoteActionPurpose.REMEDIATION]
    assert remote_action.scriptInfo.runAs == NxtRemoteActionRunAsOption.LOCAL_SYSTEM


def test_remote_action_model_accepts_missing_optional_metadata_seen_in_api() -> None:
    """RemoteAction model accepts fields omitted by real API responses."""
    payload = _remote_action_payload()
    del payload["description"]
    del payload["builtInContentVersion"]
    del payload["scriptInfo"]["executionServiceDelegate"]
    del payload["scriptInfo"]["inputs"]
    del payload["scriptInfo"]["outputs"][0]["description"]

    remote_action = NxtRemoteAction.model_validate(payload)

    assert remote_action.description is None
    assert remote_action.builtInContentVersion is None
    assert remote_action.scriptInfo.executionServiceDelegate is None
    assert remote_action.scriptInfo.inputs == []
    assert remote_action.scriptInfo.outputs[0].description is None
