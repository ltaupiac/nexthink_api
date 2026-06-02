# pylint: skip-file
# ruff: noqa

import os
import sys
from importlib.metadata import PackageNotFoundError, version

from rich_output import console, ko, ok, panel, step
from nexthink_api import (
    NexthinkClient,
    NxtInvalidTokenRequest,
    NxtRegionName,
    NxtRemoteAction,
    NxtRemoteActionErrorResponse,
    NxtRemoteActionExecutionRequest,
    NxtRemoteActionExecutionResponse,
    NxtRemoteActionTriggerInfoRequest,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
default_remote_action_id = "#your_remote_action_id"
default_collector_uid = "collector-uid"
remote_action_id = os.getenv("nexthink_remote_action_id", default_remote_action_id)
collector_uid = os.getenv("nexthink_collector_uid", default_collector_uid)
confirm_execute = os.getenv("confirm_remote_action_execute")

if client_id is None or client_secret is None:
    ko("client_id or client_secret not found")
    sys.exit(1)

step("[1/6] Checking local package version")
try:
    ok(f"nexthink_api version: {version('nexthink_api')}")
except PackageNotFoundError:
    ko("nexthink_api version: package metadata not found")

step("[2/6] Creating Nexthink client and retrieving token")
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

step("[3/6] Listing available remote actions")
remote_actions = nxt_client.remote_actions.list()
if isinstance(remote_actions, list):
    ok("Remote actions listed.")
    panel(
        [{"id": remote_action.id, "name": remote_action.name} for remote_action in remote_actions[:10]],
        title="Remote actions available",
    )
elif isinstance(remote_actions, NxtRemoteActionErrorResponse):
    ko("Remote Actions list error.")
    panel(remote_actions.model_dump(), title="Remote Actions list error", border_style="red")
elif isinstance(remote_actions, NxtInvalidTokenRequest):
    ko("Invalid token")

step("[4/6] Retrieving configured remote action details")
if remote_action_id == default_remote_action_id:
    console.print("Set nexthink_remote_action_id to a real remote action ID before retrieving details.")
else:
    details = nxt_client.remote_actions.get(remote_action_id)
    if isinstance(details, NxtRemoteAction):
        ok("Remote action details retrieved.")
        panel(
            {
                "id": details.id,
                "name": details.name,
                "description": details.description or "<no description>",
                "origin": details.origin,
                "purpose": [purpose.value for purpose in details.purpose],
                "api_enabled": details.targeting.apiEnabled,
                "windows_script": details.scriptInfo.hasScriptWindows,
                "macos_script": details.scriptInfo.hasScriptMacOs,
                "inputs": len(details.scriptInfo.inputs),
                "outputs": len(details.scriptInfo.outputs),
            },
            title="Remote action details",
        )
    elif isinstance(details, NxtRemoteActionErrorResponse):
        ko("Remote action details error.")
        panel(details.model_dump(), title="Remote action details error", border_style="red")

step("[5/6] Preparing remote action execution request")
request = NxtRemoteActionExecutionRequest(
    remoteActionId=remote_action_id,
    devices=[collector_uid],
    triggerInfo=NxtRemoteActionTriggerInfoRequest(
        externalSource="nexthink_api example",
        reason="Manual API example",
    ),
)

panel(request.model_dump(exclude_none=True), title="Remote action execution request")

step("[6/6] Checking execution confirmation")
if remote_action_id == default_remote_action_id:
    console.print("Set nexthink_remote_action_id to a real remote action ID before executing.")
    sys.exit(0)
if collector_uid == default_collector_uid:
    console.print("Set nexthink_collector_uid to a real Collector UID before executing.")
    sys.exit(0)
if confirm_execute != "yes":
    console.print()
    console.print("Set confirm_remote_action_execute=yes to execute this remote action.")
    sys.exit(0)

step("Executing remote action")
response = nxt_client.remote_actions.execute(request)
if isinstance(response, NxtRemoteActionExecutionResponse):
    ok("Remote action execution started.")
    panel(response.model_dump(), title="Remote action execution response")
elif isinstance(response, NxtRemoteActionErrorResponse):
    ko("Remote action execution error.")
    panel(response.model_dump(), title="Remote action execution error", border_style="red")
elif isinstance(response, NxtInvalidTokenRequest):
    ko("Invalid token")
else:
    panel(response, title="Response", border_style="red")
