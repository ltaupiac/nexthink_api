# Spark

Spark exposes conversation handoff through `NexthinkClient.spark`.

The handoff endpoint requires a target user principal name in the request
headers. The client takes it as an explicit argument so scripts do not hide
which user context is used.

## Hand off a text message

```python
from nexthink_api import NexthinkClient, NxtRegionName
from nexthink_api.Spark import (
    NxtSparkHandoffConversationMessageRequest,
    NxtSparkMessageDTO,
    NxtSparkTextPartDTO,
)

client = NexthinkClient(
    instance="example",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

request = NxtSparkHandoffConversationMessageRequest(
    message=NxtSparkMessageDTO(
        parts=[NxtSparkTextPartDTO(text="Summarize the current device health.")]
    ),
    metadata={"source": "automation"},
)

result = client.spark.handoff(
    request,
    user_principal_name="user@example.com",
    timezone="Europe/Paris",
)
```

`user_principal_name` is required. `timezone` is optional and is sent as the
Spark `Timezone` header when provided.

## Include file content

```python
from nexthink_api.Spark import NxtSparkFilePartByContent

request = NxtSparkHandoffConversationMessageRequest(
    message=NxtSparkMessageDTO(
        parts=[
            NxtSparkTextPartDTO(text="Analyze this CSV."),
            NxtSparkFilePartByContent(
                fileContent="base64-encoded-content",
                mimeType="text/csv",
            ),
        ]
    )
)
```

See [Spark object models](object-models/Spark.md) for the request and response
classes used by this domain.
