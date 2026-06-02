# Remote Actions

Remote Actions exposes Nexthink remote action catalog lookup and execution
through `NexthinkClient.remote_actions`.

The execution endpoint has a side effect on target devices. Keep an explicit
operator confirmation in scripts that trigger a real action.

## List and inspect actions

```python
from nexthink_api import NexthinkClient, NxtRegionName

client = NexthinkClient(
    instance="example",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

actions = client.remote_actions.list()
details = client.remote_actions.get("#remote_action_nql_id")
```

## Execute a remote action

```python
from nexthink_api.RemoteActions import (
    NxtRemoteActionExecutionRequest,
    NxtRemoteActionTriggerInfoRequest,
)

request = NxtRemoteActionExecutionRequest(
    remoteActionId="#remote_action_nql_id",
    devices=["collector-uid"],
    params={"argumentName": "argumentValue"},
    expiresInMinutes=60,
    triggerInfo=NxtRemoteActionTriggerInfoRequest(
        externalSource="automation",
        reason="maintenance",
        externalReference="ticket-123",
    ),
)

result = client.remote_actions.execute(request)
```

`devices` accepts between 1 and 10000 collector IDs. `expiresInMinutes` must be
between 60 and 10080 when provided.

See [Remote Actions object models](object-models/RemoteActions.md) for the
request and response classes used by this domain.
