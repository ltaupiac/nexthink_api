# pylint: skip-file
# ruff: noqa

import os
import sys
import time
from importlib.metadata import PackageNotFoundError, version

from rich_output import console, ko, ok, panel, step
from nexthink_api import (
    NexthinkClient,
    NxtInvalidTokenRequest,
    NxtRegionName,
    NxtWorkflow,
    NxtWorkflowDependency,
    NxtWorkflowDeviceData,
    NxtWorkflowErrorResponse,
    NxtWorkflowExecutionRequest,
    NxtWorkflowExecutionResponse,
    NxtWorkflowExternalIdsExecutionRequest,
    NxtWorkflowTriggerMethod,
    NxtWorkflowUserData,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
default_workflow_id = "#your_workflow_id"
default_device_collector_uid = "device-collector-uid"
default_user_upn = "user@example.com"
workflow_id = os.getenv("nexthink_workflow_id", default_workflow_id)
device_collector_uid = os.getenv("nexthink_workflow_device_collector_uid", default_device_collector_uid)
user_upn = os.getenv("nexthink_workflow_user_upn", default_user_upn)
confirm_execute = os.getenv("confirm_workflow_execute")
workflow_execute_v1_api = "POST /api/v1/workflows/execute"
workflow_execute_v2_api = "POST /api/v2/workflows/execute"

if client_id is None or client_secret is None:
    ko("client_id or client_secret not found")
    sys.exit(1)

def print_execution_response(label, response):
    if isinstance(response, NxtWorkflowExecutionResponse):
        ok(f"{label} execution started.")
        panel(response.model_dump(), title=f"{label} response")
    elif isinstance(response, NxtWorkflowErrorResponse):
        ko(f"{label} execution error.")
        panel(response.model_dump(), title=f"{label} error", border_style="red")
    elif isinstance(response, NxtInvalidTokenRequest):
        ko("Invalid token")
    else:
        panel(response, title=f"{label} response", border_style="red")


step("[1/8] Checking local package version")
try:
    ok(f"nexthink_api version: {version('nexthink_api')}")
except PackageNotFoundError:
    ko("nexthink_api version: package metadata not found")

step("[2/8] Creating Nexthink client and retrieving token")
nxt_client = NexthinkClient(
    tenant,
    NxtRegionName(region),
    client_id=client_id,
    client_secret=client_secret,
)

if nxt_client.token is None:
    ko("Token retrieval failed.")
    sys.exit(1)

ok("Token retrieved successfully.")

step("[3/8] Listing active API-triggerable workflows")
workflows_by_id = {}
for dependency in [
    NxtWorkflowDependency.USER,
    NxtWorkflowDependency.DEVICE,
    NxtWorkflowDependency.USER_AND_DEVICE,
    NxtWorkflowDependency.NONE,
]:
    workflows = nxt_client.workflows.list(
        dependency=dependency,
        trigger_method=NxtWorkflowTriggerMethod.API,
        fetch_only_active_workflows=True,
    )
    if isinstance(workflows, list):
        for workflow in workflows:
            workflows_by_id[workflow.id] = workflow
    elif isinstance(workflows, NxtWorkflowErrorResponse):
        ko(f"Workflows list error for dependency={dependency.value}.")
        panel(workflows.model_dump(), title="Workflows list error", border_style="red")
    elif isinstance(workflows, NxtInvalidTokenRequest):
        ko("Invalid token")

if workflows_by_id:
    ok("Workflows listed.")
    panel(
        [{"id": workflow.id, "name": workflow.name} for workflow in list(workflows_by_id.values())[:10]],
        title="Workflows available",
    )
else:
    console.print("No active API-triggerable workflow returned by list filters.")

if not workflow_id or workflow_id == default_workflow_id:
    console.print()
    console.print("Set nexthink_workflow_id to a real workflow NQL ID before retrieving details or executing.")
    sys.exit(0)

step("[4/8] Retrieving configured workflow details")
details = nxt_client.workflows.get(workflow_id)
if isinstance(details, NxtWorkflow):
    workflow = details
    ok("Workflow details retrieved.")
    panel(
        {
            "id": workflow.id,
            "uuid": workflow.uuid,
            "name": workflow.name,
            "description": workflow.description or "<no description>",
            "status": workflow.status,
            "last_update": workflow.lastUpdateTime,
        },
        title="Workflow details",
    )
elif isinstance(details, list):
    console.print("No workflow returned for the configured NQL ID.")
elif isinstance(details, NxtWorkflowErrorResponse):
    ko("Workflow details error.")
    panel(details.model_dump(), title="Workflow details error", border_style="red")

if not device_collector_uid or device_collector_uid == default_device_collector_uid:
    console.print()
    console.print("Set nexthink_workflow_device_collector_uid to a real device Collector UID before executing V1.")
    sys.exit(0)

if not user_upn or user_upn == default_user_upn:
    console.print()
    console.print("Set nexthink_workflow_user_upn to a real user UPN before executing V2.")
    sys.exit(0)

step("[5/8] Preparing workflow execution request V1")
console.print("API:", workflow_execute_v1_api)
v1_request = NxtWorkflowExecutionRequest(
    workflowId=workflow_id,
    devices=[device_collector_uid],
)

panel(v1_request.model_dump(exclude_none=True), title="Workflow V1 execution request")

step("[6/8] Preparing workflow execution request V2")
console.print("API:", workflow_execute_v2_api)
v2_request = NxtWorkflowExternalIdsExecutionRequest(
    workflowId=workflow_id,
    users=[NxtWorkflowUserData(upn=user_upn)],
)

panel(v2_request.model_dump(exclude_none=True), title="Workflow V2 execution request")

step("[7/8] Checking execution confirmation")
if confirm_execute != "yes":
    console.print()
    console.print("Set confirm_workflow_execute=yes to execute both workflow examples.")
    sys.exit(0)

step("[8/8] Executing workflow examples")
console.print("Executing workflow V1")
console.print("API:", workflow_execute_v1_api)
v1_response = nxt_client.workflows.execute(v1_request)
print_execution_response("Workflow V1", v1_response)

console.print()
console.print("Waiting 1 second before executing workflow V2")
time.sleep(1)

console.print("Executing workflow V2")
console.print("API:", workflow_execute_v2_api)
v2_response = nxt_client.workflows.execute_with_external_ids(v2_request)
print_execution_response("Workflow V2", v2_response)
