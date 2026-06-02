# Enrichment

Enrichment writes custom fields to Nexthink objects through
`NexthinkClient.enrichment`.

## Run Enrichment

```python
from nexthink_api import (
    NexthinkClient,
    NxtEnrichment,
    NxtEnrichmentRequest,
    NxtField,
    NxtFieldName,
    NxtIdentification,
    NxtIdentificationName,
    NxtRegionName,
)

client = NexthinkClient(
    instance="tenant-name",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

request = NxtEnrichmentRequest(
    domain="automation",
    enrichments=[
        NxtEnrichment(
            identification=[
                NxtIdentification(
                    name=NxtIdentificationName.DEVICE_DEVICE_NAME,
                    value="DEVICE-1",
                )
            ],
            fields=[
                NxtField(
                    name=NxtFieldName.CUSTOM_DEVICE,
                    value="patched",
                    custom_value="maintenance_status",
                )
            ],
        )
    ],
)

response = client.enrichment.run(request)
```

## Request Limits

`NxtEnrichmentRequest.enrichments` accepts between 1 and
`MAX_ENRICHMENTS_PER_REQUEST` objects. The constant is exported by the package
so applications can check or split their payload before creating the request.

```python
from nexthink_api import MAX_ENRICHMENTS_PER_REQUEST

if len(enrichments) > MAX_ENRICHMENTS_PER_REQUEST:
    raise ValueError(
        f"Enrichment request contains more than {MAX_ENRICHMENTS_PER_REQUEST} objects"
    )
```

See [Enrichment object models](object-models/Enrichment.md) for the request and
response classes used by this domain.
