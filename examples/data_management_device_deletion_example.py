# pylint: skip-file
# ruff: noqa

import os
import sys
from importlib.metadata import PackageNotFoundError, version

from rich_output import console, ko, ok, panel, step
from nexthink_api import (
    NexthinkClient,
    NxtApiException,
    NxtDataManagementErrorResponse,
    NxtDeviceDeletionResponse,
    NxtDeviceEntry,
    NxtInvalidTokenRequest,
    NxtRegionName,
    NxtUidValidationMode,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
device_uid = os.getenv("nexthink_device_uid", "00000000-0000-0000-0000-000000000000")
device_name = os.getenv("nexthink_device_name", "DEVICE-NAME")
request_id = os.getenv("nexthink_request_id", "11111111-1111-1111-1111-111111111111")
confirm_delete = os.getenv("confirm_data_management_delete")

if client_id is None or client_secret is None:
    ko("client_id or client_secret not found")
    sys.exit(1)

step("[1/5] Checking local package version")
try:
    ok(f"nexthink_api version: {version('nexthink_api')}")
except PackageNotFoundError:
    ko("nexthink_api version: package metadata not found")

device = NxtDeviceEntry(uid=device_uid, name=device_name)

# The Data Management API accepts 1 to 100 devices per request.
# Split larger deletion sets into multiple calls before sending them.
devices = [device]

step("[2/5] Preparing device deletion request")
panel(
    {
        "tenant": tenant,
        "region": region,
        "request_id": request_id,
        "devices": [device.model_dump() for device in devices],
    },
    title="Device deletion request",
)

step("[3/5] Checking deletion confirmation")
if confirm_delete != "yes":
    console.print("Set confirm_data_management_delete=yes to schedule this deletion.")
    sys.exit(0)

step("[4/5] Creating Nexthink client and retrieving token")
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

step("[5/5] Scheduling device deletion")
try:
    response = nxt_client.data_management.delete_devices(
        devices=devices,
        request_id=request_id,
        uid_validation=NxtUidValidationMode.WARN,
    )
except NxtApiException as error:
    ko("Data Management API call failed.")
    console.print(error)
    sys.exit(1)

if isinstance(response, NxtDeviceDeletionResponse):
    ok("Deletion batch accepted.")
    panel(
        {
            "batch_status": response.status,
            "scheduled_count": response.scheduledCount,
            "devices": [device_status.model_dump() for device_status in response.devices],
            "note": "The API is asynchronous; SCHEDULED means queued, not already deleted.",
        },
        title="Deletion response",
    )
elif isinstance(response, NxtDataManagementErrorResponse):
    ko("Data Management error.")
    panel(response.model_dump(), title="Data Management error", border_style="red")
elif isinstance(response, NxtInvalidTokenRequest):
    ko("Invalid token")
else:
    panel(response, title="Response", border_style="red")
