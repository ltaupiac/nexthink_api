"""Unit tests for Remote Actions execution request model."""

import pytest
from pydantic import ValidationError

from nexthink_api import NxtRemoteActionExecutionRequest, NxtRemoteActionTriggerInfoRequest


def test_execution_request_accepts_valid_payload() -> None:
    """Execution request accepts the documented payload shape."""
    request = NxtRemoteActionExecutionRequest(
        remoteActionId="#restart_service",
        devices=["collector-1"],
        params={"StartType": "Automatic"},
        expiresInMinutes=60,
        triggerInfo=NxtRemoteActionTriggerInfoRequest(
            externalSource="ServiceNow",
            reason="Ticket remediation",
            externalReference="INC001",
        ),
    )

    assert request.model_dump(exclude_none=True) == {
        "remoteActionId": "#restart_service",
        "devices": ["collector-1"],
        "params": {"StartType": "Automatic"},
        "expiresInMinutes": 60,
        "triggerInfo": {
            "externalSource": "ServiceNow",
            "reason": "Ticket remediation",
            "externalReference": "INC001",
        },
    }


def test_execution_request_rejects_empty_devices() -> None:
    """Execution request requires at least one device collector ID."""
    with pytest.raises(ValidationError):
        NxtRemoteActionExecutionRequest(remoteActionId="#restart_service", devices=[])


def test_execution_request_rejects_expiration_below_api_minimum() -> None:
    """Execution request follows the documented expiration lower bound."""
    with pytest.raises(ValidationError):
        NxtRemoteActionExecutionRequest(
            remoteActionId="#restart_service",
            devices=["collector-1"],
            expiresInMinutes=59,
        )


def test_trigger_info_rejects_reason_above_api_limit() -> None:
    """Trigger info reason follows the documented length limit."""
    with pytest.raises(ValidationError):
        NxtRemoteActionTriggerInfoRequest(reason="x" * 501)
