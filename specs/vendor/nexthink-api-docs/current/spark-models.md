# Models

## The ErrorResponse object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"ErrorResponse":{"type":"object","properties":{"message":{"type":"string"}}}}}}
```

## The FilePartByContent object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"FilePartByContent":{"required":["mimeType","fileContent"],"type":"object","properties":{"fileContent":{"type":"string"},"mimeType":{"minLength":1,"type":"string"}}}}}}
```

## The MessageDTO object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"MessageDTO":{"required":["parts"],"type":"object","properties":{"parts":{"minItems":1,"type":"array","items":{"$ref":"#/components/schemas/PartDTO"}}}},"PartDTO":{"type":"object","required":["type"],"properties":{"type":{"$ref":"#/components/schemas/PartType"}},"discriminator":{"propertyName":"type","mapping":{"TEXT":"#/components/schemas/TextPartDTO","FILE":"#/components/schemas/FilePartByContent"}},"oneOf":[{"$ref":"#/components/schemas/TextPartDTO"},{"$ref":"#/components/schemas/FilePartByContent"}]},"PartType":{"type":"string","enum":["TEXT","FILE"]},"TextPartDTO":{"required":["text"],"type":"object","properties":{"text":{"minLength":1,"type":"string"}}},"FilePartByContent":{"required":["mimeType","fileContent"],"type":"object","properties":{"fileContent":{"type":"string"},"mimeType":{"minLength":1,"type":"string"}}}}}}
```

## The PartDTO object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"PartDTO":{"type":"object","required":["type"],"properties":{"type":{"$ref":"#/components/schemas/PartType"}},"discriminator":{"propertyName":"type","mapping":{"TEXT":"#/components/schemas/TextPartDTO","FILE":"#/components/schemas/FilePartByContent"}},"oneOf":[{"$ref":"#/components/schemas/TextPartDTO"},{"$ref":"#/components/schemas/FilePartByContent"}]},"PartType":{"type":"string","enum":["TEXT","FILE"]},"TextPartDTO":{"required":["text"],"type":"object","properties":{"text":{"minLength":1,"type":"string"}}},"FilePartByContent":{"required":["mimeType","fileContent"],"type":"object","properties":{"fileContent":{"type":"string"},"mimeType":{"minLength":1,"type":"string"}}}}}}
```

## The PartType object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"PartType":{"type":"string","enum":["TEXT","FILE"]}}}}
```

## The HandoffConversationMessageRequest object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"HandoffConversationMessageRequest":{"required":["message"],"type":"object","properties":{"metadata":{"type":"object","additionalProperties":{"type":"string"},"nullable":true,"description":"Optional metadata that will be passed through the request flow"},"message":{"$ref":"#/components/schemas/MessageDTO"}}},"MessageDTO":{"required":["parts"],"type":"object","properties":{"parts":{"minItems":1,"type":"array","items":{"$ref":"#/components/schemas/PartDTO"}}}},"PartDTO":{"type":"object","required":["type"],"properties":{"type":{"$ref":"#/components/schemas/PartType"}},"discriminator":{"propertyName":"type","mapping":{"TEXT":"#/components/schemas/TextPartDTO","FILE":"#/components/schemas/FilePartByContent"}},"oneOf":[{"$ref":"#/components/schemas/TextPartDTO"},{"$ref":"#/components/schemas/FilePartByContent"}]},"PartType":{"type":"string","enum":["TEXT","FILE"]},"TextPartDTO":{"required":["text"],"type":"object","properties":{"text":{"minLength":1,"type":"string"}}},"FilePartByContent":{"required":["mimeType","fileContent"],"type":"object","properties":{"fileContent":{"type":"string"},"mimeType":{"minLength":1,"type":"string"}}}}}}
```

## The TextPartDTO object

```json
{"openapi":"3.0.1","info":{"title":"public-api","version":"1.0.0"},"components":{"schemas":{"TextPartDTO":{"required":["text"],"type":"object","properties":{"text":{"minLength":1,"type":"string"}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/spark/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
