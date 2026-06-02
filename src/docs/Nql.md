# NQL

NQL executes saved query IDs and starts exports through `NexthinkClient.nql`.

## Execute a query

```python
from nexthink_api import NexthinkClient, NxtNqlApiExecuteRequest, NxtRegionName

client = NexthinkClient(
    instance="tenant-name",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

request = NxtNqlApiExecuteRequest(queryId="#query_nql_id")
response = client.nql.execute(request, version="v2")
```

## Export and download

```python
export = client.nql.export(request)
status = client.nql.wait(export, timeout=300)
download_response = client.nql.download(status)
dataframe = client.nql.download_dataframe(status)
```

`execute()` supports `version="v1"` and `version="v2"`. New code should use
`v2` unless a tenant-specific constraint requires the historical endpoint.

See [NQL object models](object-models/Nql.md) for the request and response
classes used by this domain.
