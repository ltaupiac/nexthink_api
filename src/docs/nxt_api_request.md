# Public API Entry Points

## Public Root Client

::: nexthink_api.Clients.NexthinkClient

## Compatibility Facade

::: nexthink_api.Clients.NxtApiClient

## Official Domain Entry Points

Domain clients are created by `NexthinkClient` and accessed through properties:

```python
client.enrichment.run(request)
client.nql.execute(request)
client.data_management.delete_devices(devices)
client.remote_actions.list()
client.campaigns.trigger(request)
client.workflows.execute(request)
client.spark.handoff(request, user_principal_name="user@example.com")
```

The implementation classes behind those properties are internal delegates. Use
the domain pages for request and response models.
