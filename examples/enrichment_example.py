# pylint: skip-file
# ruff: noqa

import os
import sys
from importlib.metadata import PackageNotFoundError, version
from datetime import datetime

from rich_output import console, ko, ok, panel, step
from nexthink_api import (
    NexthinkClient,
    NxtRegionName,
    NxtIdentification,
    NxtIdentificationName,
    NxtField,
    NxtFieldName,
    NxtEnrichment,
    NxtEnrichmentRequest,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
default_device_name = "DEVICE-NAME"
device_name = os.getenv("nexthink_enrichment_device_name", default_device_name)
domain = os.getenv("nexthink_enrichment_domain", "nexthink_api_example")

https_proxy = os.getenv("https_proxy") or os.getenv("HTTPS_PROXY")
http_proxy = os.getenv("http_proxy") or os.getenv("HTTP_PROXY")

if client_id is None or client_secret is None:
    ko("client_id or client_secret not found")
    sys.exit(1)

step("[1/4] Checking local package version")
try:
    ok(f"nexthink_api version: {version('nexthink_api')}")
except PackageNotFoundError:
    ko("nexthink_api version: package metadata not found")
if https_proxy or http_proxy:
    ok("Proxy environment detected.")

if not device_name or device_name == default_device_name:
    console.print()
    console.print("Set nexthink_enrichment_device_name to a real device name before running enrichment.")
    sys.exit(0)

step("[2/4] Creating Nexthink client and retrieving token")
nxtClient = NexthinkClient(tenant, NxtRegionName(region), client_id=client_id, client_secret=client_secret)
if nxtClient.token is None:
    ko("Token retrieval failed.")
    sys.exit(1)
ok("Token retrieved successfully.")


step("[3/4] Preparing enrichment request")
# Creating the Enrichment record
identification = NxtIdentification(name=NxtIdentificationName.DEVICE_DEVICE_NAME, value=device_name)
field1 = NxtField(name=NxtFieldName.CUSTOM_DEVICE, value=str(datetime.now()), custom_value="clw1")
field2 = NxtField(name=NxtFieldName.CUSTOM_DEVICE, value=str(datetime.now()), custom_value="clw2")
field3 = NxtField(name=NxtFieldName.CUSTOM_DEVICE, value=str(datetime.now()), custom_value="clw3")

enrichments = [NxtEnrichment(identification=[identification], fields=[field1, field2, field3])]
enrichmentRequest = NxtEnrichmentRequest(enrichments=enrichments, domain=domain)
payload = enrichmentRequest.model_dump()
panel(payload, title="Enrichment request")

step("[4/4] Running enrichment")
# use the client to perform the enrichment on the Enrichment endpoint
response = nxtClient.enrichment.run(enrichmentRequest)
panel(response, title="Enrichment response")
