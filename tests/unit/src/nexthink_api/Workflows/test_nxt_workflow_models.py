"""Unit tests for Workflows inventory models."""

from nexthink_api import (
    NxtWorkflow,
    NxtWorkflowDependency,
    NxtWorkflowStatus,
    NxtWorkflowThinkletTriggerRequest,
    NxtWorkflowTriggerInfo,
    NxtWorkflowTriggerMethod,
)


def test_workflow_model_accepts_tolerant_inventory_payload() -> None:
    """Workflow inventory model accepts documented fields and tolerant nested fields."""
    workflow = NxtWorkflow(
        id="#workflow",
        uuid="workflow-uuid",
        name="Workflow",
        description="Demo workflow",
        status="ACTIVE",
        lastUpdateTime="2026-05-25T10:00:00Z",
        triggerMethods=["API"],
        versions=[{"uuid": "version-uuid"}],
    )

    assert workflow.id == "#workflow"
    assert workflow.status == NxtWorkflowStatus.ACTIVE
    assert workflow.triggerMethods == ["API"]


def test_workflow_filter_enums_follow_documented_values() -> None:
    """Workflow filter enums expose documented values."""
    assert NxtWorkflowDependency.USER_AND_DEVICE.value == "USER_AND_DEVICE"
    assert NxtWorkflowTriggerMethod.MANUAL_MULTIPLE.value == "MANUAL_MULTIPLE"


def test_thinklet_trigger_request_accepts_parameters() -> None:
    """Thinklet trigger request serializes optional parameters."""
    request = NxtWorkflowThinkletTriggerRequest(parameters={"approval": "yes"})

    assert request.model_dump(exclude_none=True) == {"parameters": {"approval": "yes"}}


def test_trigger_info_accepts_documented_fields() -> None:
    """TriggerInfo model accepts documented metadata fields."""
    trigger_info = NxtWorkflowTriggerInfo(
        externalReference="INC001",
        internalSource="Workflow",
        externalSource="ServiceNow",
        reason="Approval",
        extra="metadata",
    )

    assert trigger_info.externalReference == "INC001"
