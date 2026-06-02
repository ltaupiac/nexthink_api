# Models

## The DeviceDeletionRequest object

```json
{"openapi":"3.0.3","info":{"title":"Data Management API","version":"1.0.0"},"components":{"schemas":{"DeviceDeletionRequest":{"description":"Batch of devices to be deleted from the Nexthink inventory.","type":"object","required":["devices"],"properties":{"devices":{"description":"Non-empty list of devices to delete. The maximum number of devices per request is 100 (configurable per deployment). Split larger deletions into multiple requests.","type":"array","minItems":1,"maxItems":100,"items":{"$ref":"#/components/schemas/DeviceEntry"}}}},"DeviceEntry":{"description":"Identifies a single device for deletion.","type":"object","required":["uid","name"],"properties":{"uid":{"description":"UID of the device as reported by the Nexthink Collector. Must be a valid UUID. A malformed value results in a per-device `INVALID` status rather than failing the whole batch.","type":"string","format":"uuid"},"name":{"description":"Name of the device as reported by the Nexthink Collector. Must not be blank.","type":"string","minLength":1}}}}}}
```

## The DeviceEntry object

```json
{"openapi":"3.0.3","info":{"title":"Data Management API","version":"1.0.0"},"components":{"schemas":{"DeviceEntry":{"description":"Identifies a single device for deletion.","type":"object","required":["uid","name"],"properties":{"uid":{"description":"UID of the device as reported by the Nexthink Collector. Must be a valid UUID. A malformed value results in a per-device `INVALID` status rather than failing the whole batch.","type":"string","format":"uuid"},"name":{"description":"Name of the device as reported by the Nexthink Collector. Must not be blank.","type":"string","minLength":1}}}}}}
```

## The DeviceDeletionResponse object

```json
{"openapi":"3.0.3","info":{"title":"Data Management API","version":"1.0.0"},"components":{"schemas":{"DeviceDeletionResponse":{"description":"Scheduling result for the deletion batch.","type":"object","properties":{"scheduledCount":{"description":"Number of devices successfully queued for deletion.","type":"integer","format":"int32"},"status":{"description":"Overall batch status. Always `ACCEPTED` for a `202` response.","type":"string","enum":["ACCEPTED"]},"devices":{"description":"Per-device scheduling outcome, in the same order as the request.","type":"array","items":{"$ref":"#/components/schemas/DeviceStatus"}}}},"DeviceStatus":{"description":"Scheduling outcome for a single device.","type":"object","properties":{"uid":{"description":"UID of the device as submitted.","type":"string"},"name":{"description":"Name of the device as submitted.","type":"string"},"status":{"description":"Per-device outcome:\n- `SCHEDULED` — deletion queued successfully.\n- `INVALID` — the UID is malformed; the device was skipped. The rest of the batch proceeds.\n- `FAILED` — a downstream error prevented this device from being scheduled.\n","type":"string","enum":["SCHEDULED","INVALID","FAILED"]}}}}}}
```

## The DeviceStatus object

```json
{"openapi":"3.0.3","info":{"title":"Data Management API","version":"1.0.0"},"components":{"schemas":{"DeviceStatus":{"description":"Scheduling outcome for a single device.","type":"object","properties":{"uid":{"description":"UID of the device as submitted.","type":"string"},"name":{"description":"Name of the device as submitted.","type":"string"},"status":{"description":"Per-device outcome:\n- `SCHEDULED` — deletion queued successfully.\n- `INVALID` — the UID is malformed; the device was skipped. The rest of the batch proceeds.\n- `FAILED` — a downstream error prevented this device from being scheduled.\n","type":"string","enum":["SCHEDULED","INVALID","FAILED"]}}}}}}
```

## The ErrorResponse object

```json
{"openapi":"3.0.3","info":{"title":"Data Management API","version":"1.0.0"},"components":{"schemas":{"ErrorResponse":{"description":"Error details returned with 4xx and 5xx responses.","type":"object","properties":{"code":{"description":"Stable machine-readable error code identifying the failure reason.","type":"string","enum":["EMPTY_REQUEST","BATCH_SIZE_EXCEEDED","INVALID_REQUEST","EMPTY_TENANT","FEATURE_NOT_ENABLED","INTERNAL_ERROR"]},"message":{"description":"Human-readable description of the error.","type":"string"}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/data-management/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
