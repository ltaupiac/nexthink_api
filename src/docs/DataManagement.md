# Data Management

The Data Management API schedules device deletions from the Nexthink inventory.

Use `NexthinkClient.data_management.delete_devices()` with one to 100 devices. The API is
asynchronous: a `202 ACCEPTED` response means the deletion batch was queued, not
that devices have already been removed. Inspect each returned device status to
confirm whether a device was scheduled, rejected as invalid, or failed.

## Batch Limit And Asynchronous Behavior

Each request must contain at least one device and at most 100 devices. Split
larger deletion sets into multiple batches before calling `delete_devices()`.

Deletion scheduling is asynchronous. A successful `202 ACCEPTED` response only
confirms that the API accepted the batch for processing. It does not confirm
that inventory deletion has already completed.

## Schedule Device Deletions

```python
from nexthink_api import (
    NexthinkClient,
    NxtDeviceEntry,
    NxtRegionName,
    NxtUidValidationMode,
)

client = NexthinkClient(
    instance="tenant-name",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

response = client.data_management.delete_devices(
    # Maximum 100 devices per request. Split larger inputs into batches.
    devices=[
        NxtDeviceEntry(
            uid="00000000-0000-0000-0000-000000000000",
            name="DEVICE-1",
        ),
    ],
    request_id="11111111-1111-1111-1111-111111111111",
    uid_validation=NxtUidValidationMode.WARN,
)

for device in response.devices:
    # The API is asynchronous: SCHEDULED means queued, not already deleted.
    print(device.uid, device.name, device.status)
```

## UID Validation

`delete_devices()` validates UID format before the request. The default mode is
`NxtUidValidationMode.WARN`.

| Mode | Behavior |
| --- | --- |
| `STRICT` | Raises `ValueError` before the API call if any UID is malformed. |
| `WARN` | Logs malformed UIDs and still sends the request. |
| `PERMISSIVE` | Sends the request without local UID warnings. |

`WARN` and `PERMISSIVE` allow the API to return per-device `INVALID` statuses,
which is useful when testing or preserving server-side behavior.

## Correlation Header

Pass `request_id` to send an optional `x-request-id` header for support
correlation:

```python
client.data_management.delete_devices(
    devices=[NxtDeviceEntry(uid="00000000-0000-0000-0000-000000000000", name="DEVICE-1")],
    request_id="11111111-1111-1111-1111-111111111111",
)
```

The request header is applied only to that call and does not mutate the client's
stored headers.

When the API returns an `x-request-id` response header, Data Management success
and error responses expose it as `response.request_id`.

## Responses

Successful scheduling returns `NxtDeviceDeletionResponse`:

```python
if response.status == "ACCEPTED":
    for device in response.devices:
        if device.status == "SCHEDULED":
            print(f"{device.name} queued for deletion")
```

Documented device statuses are:

| Status | Meaning |
| --- | --- |
| `SCHEDULED` | Device deletion was queued. |
| `INVALID` | Device entry was rejected, for example because the UID is malformed. |
| `FAILED` | Device could not be scheduled for deletion. |

Documented error responses are represented by `NxtDataManagementErrorResponse`.
`401` responses are represented by `NxtInvalidTokenRequest`.

See [Data Management object models](object-models/DataManagement.md) for the
request and response classes used by this domain.
