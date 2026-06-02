# Python Nexthink

This Python library provides a small client for the
[Nexthink API](https://docs.nexthink.com/api).

## Installation

```bash
pip install nexthink_api
# or
uv add nexthink_api
```

## Source And Documentation

- [Repository source](https://github.com/ltaupiac/nexthink_api)
- [Online documentation](https://ltaupiac.github.io/nexthink_api/)
- [Official Nexthink API documentation](https://docs.nexthink.com/api)

## Quickstart

The recommended entrypoint for new code is `NexthinkClient`. The historical
`NxtApiClient` remains available as a compatibility facade.

The examples below assume these environment variables are set:

```bash
export nexthink_tenant="your-tenant-name"
export nexthink_region="eu"
export client_id="your-client-id"
export client_secret="your-client-secret"
```

When running behind a corporate proxy with TLS inspection, for example Zscaler,
call `enable_truststore()` before creating the client. This enables the
operating system trust store for Nexthink HTTP calls without permanently
patching Python SSL for the whole process.

```python
import os

from nexthink_api import NexthinkClient, NxtRegionName, enable_truststore

enable_truststore()

client = NexthinkClient(
    os.environ["nexthink_tenant"],
    NxtRegionName(os.getenv("nexthink_region", NxtRegionName.eu.value)),
    client_id=os.environ["client_id"],
    client_secret=os.environ["client_secret"],
)
```

### NQL Execute

The NQL query must already exist in Nexthink Administration as an API query.

```python
import os

from nexthink_api import NxtNqlApiExecuteRequest

request = NxtNqlApiExecuteRequest(
    queryId=os.environ["nexthink_nql_query_id"],
)

response = client.nql.execute(request, version="v2")
print(response.rows)
print(response.data)
```

### Enrichment

This example updates one custom device field for one device identified by name.

```python
import os
from datetime import datetime

from nexthink_api import (
    MAX_ENRICHMENTS_PER_REQUEST,
    NxtEnrichment,
    NxtEnrichmentRequest,
    NxtField,
    NxtFieldName,
    NxtIdentification,
    NxtIdentificationName,
)

identification = NxtIdentification(
    name=NxtIdentificationName.DEVICE_DEVICE_NAME,
    value=os.environ["nexthink_enrichment_device_name"],
)
field = NxtField(
    name=NxtFieldName.CUSTOM_DEVICE,
    custom_value="nexthink_api_example",
    value=datetime.now().isoformat(),
)
enrichments = [NxtEnrichment(identification=[identification], fields=[field])]

if len(enrichments) > MAX_ENRICHMENTS_PER_REQUEST:
    raise ValueError("Too many enrichment objects for one request")

request = NxtEnrichmentRequest(
    domain=os.getenv("nexthink_enrichment_domain", "nexthink_api_example"),
    enrichments=enrichments,
)

response = client.enrichment.run(request)
print(response)
```

### Data Management Device Deletion

The Data Management deletion API is asynchronous and destructive. Keep an
explicit confirmation in scripts and validate identifiers before calling it.

```python
import os

from nexthink_api import NxtDeviceEntry, NxtUidValidationMode

if os.getenv("confirm_data_management_delete") != "yes":
    raise SystemExit("Set confirm_data_management_delete=yes before deleting devices.")

devices = [
    NxtDeviceEntry(
        uid=os.environ["nexthink_device_uid"],
        name=os.environ["nexthink_device_name"],
    )
]

response = client.data_management.delete_devices(
    devices=devices,
    request_id=os.environ["nexthink_request_id"],
    uid_validation=NxtUidValidationMode.WARN,
)
print(response)
```

## Examples

Runnable examples are available in `examples/`:

```bash
uv run python examples/nql_query_example.py
uv run python examples/enrichment_example.py
uv run python examples/data_management_device_deletion_example.py
uv run python examples/remote_actions_example.py
uv run python examples/campaigns_example.py
uv run python examples/workflows_example.py
uv run python examples/spark_handoff_example.py
```

## API Classes

Most request and response classes are Pydantic models. Use:

- `model_dump()` to serialize to a dictionary.
- `model_dump_json()` to serialize to JSON.
- `model_validate(data)` to build a model from serialized data.
