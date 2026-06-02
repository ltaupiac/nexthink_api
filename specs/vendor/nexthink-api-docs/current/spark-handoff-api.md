# Handoff API

## Hand off a conversation to Spark

> Handles user message requests for which responses will be redirected to Spark MS Teams.<br>

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"tags":[],"paths":{"/api/v1/spark/handoff":{"post":{"tags":["Handoff API"],"summary":"Hand off a conversation to Spark","description":"Handles user message requests for which responses will be redirected to Spark MS Teams.\n","operationId":"handleHandoffRequest","parameters":[{"name":"Authorization","in":"header","description":"Authorization part for this request","required":true,"schema":{"type":"string"}},{"name":"Timezone","in":"header","description":"Timezone to be used for this request","required":false,"schema":{"type":"string"}},{"name":"User-Principal-Name","in":"header","description":"UPN to be used for this request","required":true,"schema":{"type":"string"}}],"requestBody":{"description":"Handoff conversation request containing user message","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HandoffConversationMessageRequest"}}},"required":true},"responses":{"204":{"description":"Request successful"},"400":{"description":"Bad request"},"401":{"description":"Unauthorized"},"403":{"description":"Forbidden","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ErrorResponse"}}}},"404":{"description":"Not found","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ErrorResponse"}}}},"500":{"description":"Internal server error"},"502":{"description":"Bad gateway"},"503":{"description":"Service unavailable"}}}}},"components":{"schemas":{"HandoffConversationMessageRequest":{"required":["message"],"type":"object","properties":{"metadata":{"type":"object","additionalProperties":{"type":"string"},"nullable":true,"description":"Optional metadata that will be passed through the request flow"},"message":{"$ref":"#/components/schemas/MessageDTO"}}},"MessageDTO":{"required":["parts"],"type":"object","properties":{"parts":{"minItems":1,"type":"array","items":{"$ref":"#/components/schemas/PartDTO"}}}},"PartDTO":{"type":"object","required":["type"],"properties":{"type":{"$ref":"#/components/schemas/PartType"}},"discriminator":{"propertyName":"type","mapping":{"TEXT":"#/components/schemas/TextPartDTO","FILE":"#/components/schemas/FilePartByContent"}},"oneOf":[{"$ref":"#/components/schemas/TextPartDTO"},{"$ref":"#/components/schemas/FilePartByContent"}]},"PartType":{"type":"string","enum":["TEXT","FILE"]},"TextPartDTO":{"required":["text"],"type":"object","properties":{"text":{"minLength":1,"type":"string"}}},"FilePartByContent":{"required":["mimeType","fileContent"],"type":"object","properties":{"fileContent":{"type":"string"},"mimeType":{"minLength":1,"type":"string"}}},"ErrorResponse":{"type":"object","properties":{"message":{"type":"string"}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/spark/handoff-api.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
