"""Unit tests for Workflows execution request models."""

import pytest
from pydantic import ValidationError

from nexthink_api import (
    NxtWorkflowDeviceData,
    NxtWorkflowExecutionRequest,
    NxtWorkflowExternalIdsExecutionRequest,
    NxtWorkflowUserData,
)


def test_execution_request_accepts_device_targets() -> None:
    """V1 execution request accepts collector UUID targets."""
    request = NxtWorkflowExecutionRequest(
        workflowId="#workflow",
        devices=["8d868f83-547c-471a-bb7b-452211ed38a1"],
        params={"ticket": "INC001"},
    )

    assert request.model_dump(exclude_none=True) == {
        "workflowId": "#workflow",
        "devices": ["8d868f83-547c-471a-bb7b-452211ed38a1"],
        "users": [],
        "params": {"ticket": "INC001"},
    }


def test_execution_request_requires_at_least_one_target() -> None:
    """V1 execution request requires either devices or users."""
    with pytest.raises(ValidationError):
        NxtWorkflowExecutionRequest(workflowId="#workflow")


def test_external_ids_execution_request_accepts_user_and_device_identifiers() -> None:
    """V2 execution request accepts external user and device identifiers."""
    request = NxtWorkflowExternalIdsExecutionRequest(
        workflowId="#workflow",
        devices=[NxtWorkflowDeviceData(name="macbook-001")],
        users=[NxtWorkflowUserData(upn="user@example.com")],
    )

    assert request.model_dump(exclude_none=True) == {
        "workflowId": "#workflow",
        "devices": [{"name": "macbook-001"}],
        "users": [{"upn": "user@example.com"}],
    }


def test_external_ids_execution_request_requires_at_least_one_target() -> None:
    """V2 execution request requires either devices or users."""
    with pytest.raises(ValidationError):
        NxtWorkflowExternalIdsExecutionRequest(workflowId="#workflow")


def test_device_data_requires_identifier() -> None:
    """DeviceData rejects empty selectors."""
    with pytest.raises(ValidationError):
        NxtWorkflowDeviceData()


def test_user_data_rejects_invalid_upn() -> None:
    """UserData follows the documented UPN pattern."""
    with pytest.raises(ValidationError):
        NxtWorkflowUserData(upn="not-an-email")
