# Models

## The ErrorResponse object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"ErrorResponse":{"required":["code","message"],"type":"object","properties":{"code":{"minLength":1,"type":"string","description":"error code"},"message":{"minLength":1,"type":"string","description":"error message"}}}}}}
```

## The ExecutionRequest object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"ExecutionRequest":{"required":["devices","remoteActionId"],"type":"object","properties":{"remoteActionId":{"minLength":1,"type":"string","description":"The ID of the remote action to execute"},"params":{"type":"object","additionalProperties":{"type":"string"},"description":"Any parameters to send to the script. Leave the object empty if there are none. Example: {StartType: \"Automatic\", StatusChange: \"On\", SetStartTypeTo: \"Manual\"}"},"devices":{"maxItems":10000,"minItems":1,"type":"array","description":"Nexthink Collector IDs of the devices that the remote action should be executed on","items":{"type":"string"}},"expiresInMinutes":{"maximum":10080,"minimum":60,"type":"integer","description":"The amount of time in minutes before the execution will expire if a targeted device does not come online to process it.","format":"int32"},"triggerInfo":{"$ref":"#/components/schemas/TriggerInfoRequest"}}},"TriggerInfoRequest":{"type":"object","properties":{"externalSource":{"type":"string","description":"The external application/tool name from where the action was triggered"},"reason":{"maxLength":500,"type":"string","description":"The reason behind triggering the action "},"externalReference":{"type":"string","description":"The external ticket reference ID for which this action was taken"}}}}}}
```

## The ExecutionResponse object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"ExecutionResponse":{"required":["requestId"],"type":"object","properties":{"requestId":{"minLength":1,"type":"string","description":"The Nexthink ID of the request created that spawned the executions. Use this ID to query remote action executions in NQL."},"expiresInMinutes":{"maximum":10080,"minimum":1,"type":"integer","description":"The amount of time in minutes before the execution will expire if a targeted device does not come online to process it.","format":"int32"}}}}}}
```

## The Input object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"Input":{"required":["allowCustomValue","description","id","name","options","usedByMacOs","usedByWindows"],"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"usedByWindows":{"type":"boolean"},"usedByMacOs":{"type":"boolean"},"options":{"type":"array","items":{"type":"string"}},"allowCustomValue":{"type":"boolean"}}}}}}
```

## The Output object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"Output":{"required":["description","id","name","type","usedByMacOs","usedByWindows"],"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"type":{"type":"string"},"description":{"type":"string"},"usedByWindows":{"type":"boolean"},"usedByMacOs":{"type":"boolean"}}}}}}
```

## The Purpose object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"Purpose":{"type":"string","enum":["DATA_COLLECTION","REMEDIATION"]}}}}
```

## The RemoteAction object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"RemoteAction":{"required":["builtInContentVersion","description","id","name","origin","purpose","scriptInfo","targeting","uuid"],"type":"object","properties":{"id":{"type":"string"},"uuid":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"origin":{"type":"string"},"builtInContentVersion":{"type":"string"},"purpose":{"type":"array","items":{"$ref":"#/components/schemas/Purpose"}},"targeting":{"$ref":"#/components/schemas/Targeting"},"scriptInfo":{"$ref":"#/components/schemas/ScriptInfo"}}},"Purpose":{"type":"string","enum":["DATA_COLLECTION","REMEDIATION"]},"Targeting":{"required":["apiEnabled","manualAllowMultipleDevices","manualEnabled","workflowEnabled"],"type":"object","properties":{"apiEnabled":{"type":"boolean"},"manualEnabled":{"type":"boolean"},"workflowEnabled":{"type":"boolean"},"manualAllowMultipleDevices":{"type":"boolean"}}},"ScriptInfo":{"required":["executionServiceDelegate","hasScriptMacOs","hasScriptWindows","inputs","outputs","runAs","timeoutSeconds"],"type":"object","properties":{"executionServiceDelegate":{"type":"string"},"runAs":{"$ref":"#/components/schemas/RunAsOption"},"timeoutSeconds":{"type":"integer","format":"int32"},"hasScriptWindows":{"type":"boolean"},"hasScriptMacOs":{"type":"boolean"},"inputs":{"type":"array","items":{"$ref":"#/components/schemas/Input"}},"outputs":{"type":"array","items":{"$ref":"#/components/schemas/Output"}}}},"RunAsOption":{"type":"string","enum":["LOCAL_SYSTEM","INTERACTIVE_USER","DELEGATE_TO_SERVICE"]},"Input":{"required":["allowCustomValue","description","id","name","options","usedByMacOs","usedByWindows"],"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"usedByWindows":{"type":"boolean"},"usedByMacOs":{"type":"boolean"},"options":{"type":"array","items":{"type":"string"}},"allowCustomValue":{"type":"boolean"}}},"Output":{"required":["description","id","name","type","usedByMacOs","usedByWindows"],"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"type":{"type":"string"},"description":{"type":"string"},"usedByWindows":{"type":"boolean"},"usedByMacOs":{"type":"boolean"}}}}}}
```

## The RunAsOption object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"RunAsOption":{"type":"string","enum":["LOCAL_SYSTEM","INTERACTIVE_USER","DELEGATE_TO_SERVICE"]}}}}
```

## The ScriptInfo object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"ScriptInfo":{"required":["executionServiceDelegate","hasScriptMacOs","hasScriptWindows","inputs","outputs","runAs","timeoutSeconds"],"type":"object","properties":{"executionServiceDelegate":{"type":"string"},"runAs":{"$ref":"#/components/schemas/RunAsOption"},"timeoutSeconds":{"type":"integer","format":"int32"},"hasScriptWindows":{"type":"boolean"},"hasScriptMacOs":{"type":"boolean"},"inputs":{"type":"array","items":{"$ref":"#/components/schemas/Input"}},"outputs":{"type":"array","items":{"$ref":"#/components/schemas/Output"}}}},"RunAsOption":{"type":"string","enum":["LOCAL_SYSTEM","INTERACTIVE_USER","DELEGATE_TO_SERVICE"]},"Input":{"required":["allowCustomValue","description","id","name","options","usedByMacOs","usedByWindows"],"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"usedByWindows":{"type":"boolean"},"usedByMacOs":{"type":"boolean"},"options":{"type":"array","items":{"type":"string"}},"allowCustomValue":{"type":"boolean"}}},"Output":{"required":["description","id","name","type","usedByMacOs","usedByWindows"],"type":"object","properties":{"id":{"type":"string"},"name":{"type":"string"},"type":{"type":"string"},"description":{"type":"string"},"usedByWindows":{"type":"boolean"},"usedByMacOs":{"type":"boolean"}}}}}}
```

## The Targeting object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"Targeting":{"required":["apiEnabled","manualAllowMultipleDevices","manualEnabled","workflowEnabled"],"type":"object","properties":{"apiEnabled":{"type":"boolean"},"manualEnabled":{"type":"boolean"},"workflowEnabled":{"type":"boolean"},"manualAllowMultipleDevices":{"type":"boolean"}}}}}}
```

## The TriggerInfoRequest object

```json
{"openapi":"3.0.1","info":{"title":"Remote Actions API","version":"1.0.0"},"components":{"schemas":{"TriggerInfoRequest":{"type":"object","properties":{"externalSource":{"type":"string","description":"The external application/tool name from where the action was triggered"},"reason":{"maxLength":500,"type":"string","description":"The reason behind triggering the action "},"externalReference":{"type":"string","description":"The external ticket reference ID for which this action was taken"}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/remote-actions/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
