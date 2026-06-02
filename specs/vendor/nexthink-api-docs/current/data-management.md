# Data management

Remove devices from the Nexthink inventory in bulk using the Data management API. Submit a batch of devices identified by their UID and name. The API is asynchronous: it queues each valid device for deletion and returns a per-device scheduling status immediately.

## Prerequisites

Before using the Data management API, ensure the following are in place:

1. **API credentials**: Create a set of API credentials in your Nexthink instance as described in the API Credentials documentation.
2. **JWT permission scope**: The API credential must include the `nx_dataplatform_device_deletion_api` permission scope.

## Identifying devices

Each entry in the request requires two fields:

<table><thead><tr><th width="136.6666259765625">Field</th><th>Description</th></tr></thead><tbody><tr><td><code>uid</code></td><td>Device UID assigned by the Nexthink Collector. Must be a valid UUID.</td></tr><tr><td><code>name</code></td><td>Device name as reported by the Nexthink Collector. Must not be blank.</td></tr></tbody></table>

To retrieve device UIDs, run an [Investigation](https://docs.nexthink.com/platform/latest/investigations) scoped to the devices you want to remove and export the result to CSV.

## Request limits

A single request can contain a maximum of 100 devices. For larger deletions, split the list into batches of up to 100 and call the API once per batch.

## Per-device status

The API validates each device independently. A malformed UID does not cause the entire batch to be rejected, it produces an `INVALID` status for that entry while the rest of the batch proceeds.

<table><thead><tr><th width="135.333251953125">Status</th><th>Meaning</th></tr></thead><tbody><tr><td><code>SCHEDULED</code></td><td>Device successfully queued for deletion.</td></tr><tr><td><code>INVALID</code></td><td>The device UID is malformed; this entry was skipped.</td></tr><tr><td><code>FAILED</code></td><td>A downstream error prevented this device from being scheduled.</td></tr></tbody></table>

The `scheduledCount` field in the response indicates how many devices were queued successfully.

## Asynchronous deletion

A `202 Accepted` response confirms that the valid devices have been queued. Actual removal from the Nexthink inventory happens asynchronously in the background. The response does not indicate whether the deletion has been completed.

## Correlation headers

Pass an `x-request-id` header (UUID format) to correlate your calls with Nexthink support logs. The value is echoed back in the response. If you omit it, the API generates and returns one.

<table><thead><tr><th width="137">Header</th><th width="198.3333740234375">Direction</th><th>Description</th></tr></thead><tbody><tr><td><code>x-request-id</code></td><td>Request / Response</td><td>Client-supplied or server-generated correlation UUID.</td></tr><tr><td><code>x-trace-id</code></td><td>Response</td><td>W3C <code>traceparent</code>-derived trace identifier; falls back to <code>x-request-id</code>.</td></tr></tbody></table>

## Error codes

<table><thead><tr><th width="135.6666259765625">HTTP status</th><th width="206">Code</th><th>When</th></tr></thead><tbody><tr><td><code>400</code></td><td><code>EMPTY_REQUEST</code></td><td>The <code>devices</code> array is empty or missing.</td></tr><tr><td><code>400</code></td><td><code>INVALID_REQUEST</code></td><td>Schema validation failed, for example, blank <code>uid</code> or <code>name</code>.</td></tr><tr><td><code>400</code></td><td><code>BATCH_SIZE_EXCEEDED</code></td><td>More than 100 devices submitted in a single request.</td></tr><tr><td><code>400</code></td><td><code>EMPTY_TENANT</code></td><td>Tenant context could not be resolved from the JWT claims.</td></tr><tr><td><code>401</code></td><td>—</td><td>Bearer token is missing or invalid.</td></tr><tr><td><code>403</code></td><td><code>FEATURE_NOT_ENABLED</code></td><td>The Data management API is not enabled for this tenant.</td></tr><tr><td><code>500</code></td><td><code>INTERNAL_ERROR</code></td><td>Unexpected server error. Provide the <code>x-request-id</code> value when contacting support.</td></tr></tbody></table>


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/data-management.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
