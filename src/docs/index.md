# nexthink_api

Python client for the [Nexthink API](https://docs.nexthink.com/api).

## Documentation Sources

The official Nexthink API documentation is the upstream reference:

- [Nexthink API documentation](https://docs.nexthink.com/api)
- [Nexthink API sitemap](https://docs.nexthink.com/api/sitemap.md)
- [Nexthink API LLM snapshot](https://docs.nexthink.com/api/llms-full.txt)

Runtime behavior does not depend on downloading YAML files from the Nexthink
documentation site. The package contract is defined by the Python models,
domain clients, tests, and the local `SpecRegistry`.

## Public Client

Use `NexthinkClient` for new code:

```python
from nexthink_api import NexthinkClient, NxtRegionName

client = NexthinkClient(
    "tenant-name",
    NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)
```

The historical `NxtApiClient` remains available as a compatibility facade.

## Supported Domains

- Enrichment
- NQL
- Data Management
- Remote Actions
- Campaigns
- Workflows
- Spark

## Corporate Proxy TLS Inspection

When running behind a corporate proxy with TLS inspection, for example Zscaler,
call `enable_truststore()` before creating the client:

```python
from nexthink_api import enable_truststore

enable_truststore()
```

This enables the operating system trust store for Nexthink HTTP calls without
permanently patching Python SSL for the whole process.
