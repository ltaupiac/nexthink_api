# Models

## The DeviceData object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"DeviceData":{"type":"object","properties":{"name":{"type":"string"},"uid":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"},"collectorUid":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"}}}}}}
```

## The ErrorResponse object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"ErrorResponse":{"required":["code","details"],"type":"object","properties":{"code":{"minLength":1,"type":"string"},"details":{"type":"string"}}}}}}
```

## The ExecutionRequest object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"ExecutionRequest":{"required":["workflowId","users","devices"],"type":"object","properties":{"workflowId":{"type":"string","description":"The ID of the workflow to execute."},"devices":{"maxItems":10000,"type":"array","description":"Nexthink Collector IDs of the devices that the workflow should be executed on. **Note**: If `devices` are included in the request, then `users` are optional by default.\n","items":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"}},"users":{"maxItems":10000,"type":"array","description":"The security IDs of the users that the workflow would target. **Note**: If `users` are included in the request, then `devices` are optional by default.\n","items":{"pattern":"^S(-\\d+){2,10}$|^0$","type":"string"}},"params":{"allOf":[{"type":"object","additionalProperties":{"type":"string"}},{"description":"Any parameters that can be sent to the workflow. If your workflow has been configured with a parameter, then `params` is optional. \nLeave the object empty if there are no parameters.\n"}]}}}}}}
```

## The ExecutionResponse object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"ExecutionResponse":{"required":["executionsUuids","requestUuid"],"type":"object","properties":{"requestUuid":{"minLength":1,"type":"string","description":"The request ID. Use this ID to query workflow executions in NQL `workflow.executions.request_id`."},"executionsUuids":{"minItems":1,"type":"array","description":"A list of execution ID for each object targeted `workflow.executions.execution_id`.","items":{"type":"string"}}},"description":"Each request spawns one or more executions depending on the input. All executions will have the same request ID and a unique execution ID."}}}}
```

## The ExternalIdsExecutionRequest object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"ExternalIdsExecutionRequest":{"required":["workflowId","users","devices"],"type":"object","properties":{"workflowId":{"type":"string","description":"The ID of the workflow to execute."},"devices":{"maxItems":10000,"type":"array","description":"Nexthink Collector IDs, device names and/or device UIDs of the devices that the workflow should be executed on.","items":{"$ref":"#/components/schemas/DeviceData"}},"users":{"maxItems":10000,"type":"array","description":"User's Security IDs, user's principal name and/or users UIDs that the workflow would target.","items":{"$ref":"#/components/schemas/UserData"}},"params":{"allOf":[{"type":"object","additionalProperties":{"type":"string"}},{"description":"Any parameters to send to the workflow. Leave the object empty if there are none."}]}}},"DeviceData":{"type":"object","properties":{"name":{"type":"string"},"uid":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"},"collectorUid":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"}}},"UserData":{"type":"object","properties":{"uid":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"},"upn":{"pattern":"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$","type":"string"},"sid":{"pattern":"^S(-\\d+){2,10}$|^0$","type":"string"}}}}}}
```

## The ThinkletTriggerRequest object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"ThinkletTriggerRequest":{"type":"object","properties":{"parameters":{"allOf":[{"type":"object","additionalProperties":{"minLength":1,"type":"string"}},{"description":"Any parameters to send to the thinklet waiting for this trigger. Leave the object empty if there are none."}]}}}}}}
```

## The ThinkletTriggerResponse object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"ThinkletTriggerResponse":{"required":["requestUuid"],"type":"object","properties":{"requestUuid":{"type":"string","description":"The request ID.","format":"uuid"}}}}}}
```

## The TriggerInfo object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"TriggerInfo":{"type":"object","properties":{"externalReference":{"type":"string","description":"External reference: An identifier of the external web application record in reference to which the workflow was executed."},"internalSource":{"type":"string","description":"Displays the name of the feature from which the workflow was triggered."},"externalSource":{"type":"string","description":"Name of the external system, outside of Nexthink, from where the workflow was triggered."},"reason":{"type":"string","description":"The reason behind triggering the action."},"extra":{"type":"string","description":"Use this field to store any extra information."}}}}}}
```

## The UserData object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"UserData":{"type":"object","properties":{"uid":{"pattern":"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$","type":"string"},"upn":{"pattern":"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$","type":"string"},"sid":{"pattern":"^S(-\\d+){2,10}$|^0$","type":"string"}}}}}}
```

## The Workflow object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"Workflow":{"required":["description","id","lastUpdateTime","name","status","triggerMethods","uuid","versions"],"type":"object","properties":{"id":{"type":"string"},"uuid":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"status":{"$ref":"#/components/schemas/Workflow.Status"},"lastUpdateTime":{"type":"string","format":"date-time"},"triggerMethods":{"$ref":"#/components/schemas/Workflow"},"versions":{"type":"array","items":{"$ref":"#/components/schemas/Workflow"}}}},"Workflow.Status":{"type":"string","enum":["ACTIVE","INACTIVE"]}}}}
```

## The Workflow\.Status object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"Workflow.Status":{"type":"string","enum":["ACTIVE","INACTIVE"]}}}}
```

## The WorkflowFilter.TriggerMethod object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"WorkflowFilter.TriggerMethod":{"type":"string","enum":["API","MANUAL","MANUAL_MULTIPLE","SCHEDULER"]}}}}
```

## The WorkflowFilter.WorkflowDependency object

```json
{"openapi":"3.0.1","info":{"title":"Workflows","version":"1.0.0"},"components":{"schemas":{"WorkflowFilter.WorkflowDependency":{"type":"string","enum":["USER","DEVICE","USER_AND_DEVICE","NONE"]}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/workflows/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
