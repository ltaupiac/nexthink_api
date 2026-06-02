# Workflows

Workflows exposes Nexthink workflow metadata lookup and execution through
`NexthinkClient.workflows`.

Workflow execution has a side effect on users or devices. Keep explicit
confirmation in scripts that execute a real workflow.

## List and inspect workflows

```python
from nexthink_api import NexthinkClient, NxtRegionName
from nexthink_api.Workflows import NxtWorkflowDependency, NxtWorkflowTriggerMethod

client = NexthinkClient(
    instance="example",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

workflows = client.workflows.list(
    dependency=NxtWorkflowDependency.USER,
    trigger_method=NxtWorkflowTriggerMethod.API,
    fetch_only_active_workflows=True,
)
details = client.workflows.get("#workflow_nql_id")
```

## Execute with Workflows v1

Use v1 when you already have Nexthink collector IDs for devices or SIDs for
users.

```python
from nexthink_api.Workflows import NxtWorkflowExecutionRequest

request = NxtWorkflowExecutionRequest(
    workflowId="#workflow_nql_id",
    devices=["collector-uid"],
    params={"inputName": "inputValue"},
)

result = client.workflows.execute(request, source="automation")
```

## Execute with Workflows v2 external identifiers

Use v2 when the caller naturally has external identifiers such as UPNs, device
names, device UIDs, or collector UIDs.

```python
from nexthink_api.Workflows import (
    NxtWorkflowExternalIdsExecutionRequest,
    NxtWorkflowUserData,
)

request = NxtWorkflowExternalIdsExecutionRequest(
    workflowId="#workflow_nql_id",
    users=[NxtWorkflowUserData(upn="user@example.com")],
    params={"inputName": "inputValue"},
)

result = client.workflows.execute_with_external_ids(request, source="automation")
```

Both execution request types require at least one device or user target. Target
lists accept up to 10000 entries.

## Trigger a thinklet

```python
result = client.workflows.trigger_thinklet(
    workflow_uuid="workflow-uuid",
    execution_uuid="execution-uuid",
    source="automation",
)
```

See [Workflows object models](object-models/Workflows.md) for the request and
response classes used by this domain.
