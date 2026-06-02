# Models

## The DateTime object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"DateTime":{"type":"object","properties":{"year":{"type":"integer","format":"int64"},"month":{"type":"integer","format":"int64"},"day":{"type":"integer","format":"int64"},"hour":{"type":"integer","format":"int64"},"minute":{"type":"integer","format":"int64"},"second":{"type":"integer","format":"int64"}}}}}}
```

## The ErrorResponse object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"ErrorResponse":{"type":"object","properties":{"message":{"type":"string","description":"Message with the description of the error."},"code":{"type":"integer","description":"Error code","format":"int32"},"source":{"type":"string","description":"Source of the error, if any."}}}}}}
```

## The NqlApiExecuteRequest object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"NqlApiExecuteRequest":{"required":["queryId"],"type":"object","properties":{"queryId":{"maxLength":255,"minLength":1,"pattern":"^#[a-z0-9_]{2,255}$","type":"string","description":"Identifier of the query which is going to be executed."},"parameters":{"type":"object","additionalProperties":{"type":"string"},"description":"Key and value of the parameters to be replaced within the NQL query in order to compose a final query for execution. Example: {\\\"alert_name\\\": \\\"my_alert\\\", \\\"alert_status\\\": \\\"Open\\\"}\""}}}}}}
```

## The NqlApiExportRequest object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"NqlApiExportRequest":{"required":["queryId"],"type":"object","properties":{"queryId":{"maxLength":255,"minLength":1,"pattern":"^#[a-z0-9_]{2,255}$","type":"string","description":"Identifier of the query which is going to be executed."},"parameters":{"type":"object","additionalProperties":{"type":"string"},"description":"Key and value of the parameters to be replaced within the NQL query in order to compose a final query for execution. Example: {\\\"alert_name\\\": \\\"my_alert\\\", \\\"alert_status\\\": \\\"Open\\\"}\""},"compression":{"type":"string","description":"The compression algorithm for the export. If not set, no compression is applied.","enum":["ZSTD","GZIP","NONE"],"nullable":true}}}}}}
```

## The NqlApiExecuteResponse object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"NqlApiExecuteResponse":{"type":"object","properties":{"queryId":{"type":"string","description":"Identifier of the executed query"},"executedQuery":{"type":"string","description":"Final query executed with the replaced parameters."},"rows":{"type":"integer","description":"Number of rows returned","format":"int64"},"executionDateTime":{"allOf":[{"$ref":"#/components/schemas/DateTime"},{"type":"object","description":"Date and time of the execution"}]},"headers":{"type":"array","description":"Ordered list with the headers of the returned fields.","items":{"type":"string"}},"data":{"type":"array","description":"List of rows with the data returned by the query execution.","items":{"type":"array","items":{"type":"object"}}}}},"DateTime":{"type":"object","properties":{"year":{"type":"integer","format":"int64"},"month":{"type":"integer","format":"int64"},"day":{"type":"integer","format":"int64"},"hour":{"type":"integer","format":"int64"},"minute":{"type":"integer","format":"int64"},"second":{"type":"integer","format":"int64"}}}}}}
```

## The NqlApiExportResponse object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"NqlApiExportResponse":{"type":"object","properties":{"exportId":{"type":"string","description":"Export identifier to be used in the \"status\" operation to know the state of the export and to retrieve the URL of the file with the results."}}}}}}
```

## The NqlApiStatusResponse object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"NqlApiStatusResponse":{"type":"object","properties":{"status":{"type":"string","description":"Status of the export","enum":["SUBMITTED","IN_PROGRESS","ERROR","COMPLETED"],"nullable":false},"resultsFileUrl":{"type":"string","description":"URL of the file with the content once the export has been completed.","nullable":true},"errorDescription":{"type":"string","description":"Message with the description of the error.","nullable":true}}}}}}
```

## The NqlApiExecuteV2Response object

```json
{"openapi":"3.0.1","info":{"title":"NQL API","version":"1.2.0"},"components":{"schemas":{"NqlApiExecuteV2Response":{"type":"object","properties":{"queryId":{"type":"string","description":"Identifier of the executed query"},"executedQuery":{"type":"string","description":"Final query executed with the parameters replaced"},"rows":{"type":"integer","description":"Number of rows returned","format":"int64"},"executionDateTime":{"type":"string","description":"Date and time of the execution in ISO format"},"data":{"type":"array","description":"List of rows with the data returned by the query execution","items":{"type":"object","properties":{"key1":{},"key2":{}}}}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/nql/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
