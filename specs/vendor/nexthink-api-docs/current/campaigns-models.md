# Models

## The TriggerErrorResponse object

```json
{"openapi":"3.0.1","info":{"title":"Campaigns API","version":"1.0.0"},"components":{"schemas":{"TriggerErrorResponse":{"required":["code","message"],"type":"object","properties":{"code":{"type":"string","description":"The error code returned to the client."},"message":{"type":"string","description":"The error message returned to the client."}}}}}}
```

## The TriggerRequest object

```json
{"openapi":"3.0.1","info":{"title":"Campaigns API","version":"1.0.0"},"components":{"schemas":{"TriggerRequest":{"required":["campaignNqlId","expiresInMinutes","userSid"],"type":"object","properties":{"campaignNqlId":{"minLength":1,"type":"string","description":"The ID of the campaign to send."},"userSid":{"maxItems":10000,"minItems":1,"type":"array","description":"SIDs of users that the campaign should be sent to.","items":{"type":"string","description":"SID of a user."}},"expiresInMinutes":{"maximum":525600,"minimum":1,"type":"integer","description":"The number of minutes before the campaign response expires and will stop being shown to the users, starting from the current time. The expiration date and time is set at the time of the API call and is not influenced by the time at which the campaign is displayed to the user or by the user postponing the campaign.","format":"int32"},"parameters":{"maxItems":30,"type":"object","additionalProperties":{"type":"string"},"description":"Key and value of the parameters within the campaign to be replaced to compose the final questions to be displayed. The provided keys must match exactly the IDs of all parameters of the campaign. In case a duplicated key is specified, only the latest value of the parameter will be taken into account."}}}}}}
```

## The TriggerResponseDetails object

```json
{"openapi":"3.0.1","info":{"title":"Campaigns API","version":"1.0.0"},"components":{"schemas":{"TriggerResponseDetails":{"required":["userSid"],"type":"object","properties":{"requestId":{"type":"string","description":"ID of the request created for the user that can be used to retrieve later the status and answers to the campaign, in case the request could be created successfully"},"userSid":{"type":"string","description":"SID of the user"},"message":{"type":"string","description":"Reason why a request could not be created for that user SID"}}}}}}
```

## The TriggerSuccessResponse object

```json
{"openapi":"3.0.1","info":{"title":"Campaigns API","version":"1.0.0"},"components":{"schemas":{"TriggerSuccessResponse":{"required":["requests"],"type":"object","properties":{"requests":{"minItems":1,"type":"array","description":"Identifiers of the requests created for each user SID sent in the request or corresponding message in case of error. Duplicate SIDs in the API request are filtered out from the response list.","items":{"$ref":"#/components/schemas/TriggerResponseDetails"}}}},"TriggerResponseDetails":{"required":["userSid"],"type":"object","properties":{"requestId":{"type":"string","description":"ID of the request created for the user that can be used to retrieve later the status and answers to the campaign, in case the request could be created successfully"},"userSid":{"type":"string","description":"SID of the user"},"message":{"type":"string","description":"Reason why a request could not be created for that user SID"}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/campaigns/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
