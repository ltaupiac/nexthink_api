# pylint: skip-file
# ruff: noqa

import os
import sys
from importlib.metadata import PackageNotFoundError, version

from rich_output import console, ko, ok, panel, step, text_panel
from nexthink_api import (
    NexthinkClient,
    NxtRegionName,
    NxtNqlApiExecuteRequest,
    NxtNqlApiExecuteResponse,
    NxtNqlApiExecuteV2Response,
    NxtNqlApiExportResponse,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
default_nql_query_id = "#your_nql_query_id"
nql_query_id = (
    os.getenv("nexthink_nql_query_id")
    or os.getenv("NEXTHINK_API_INTEGRATION_NQL_QUERY_ID")
    or default_nql_query_id
)

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

if not nql_query_id or nql_query_id == default_nql_query_id:
    console.print()
    console.print("Set nexthink_nql_query_id to a real NQL query ID before executing.")
    sys.exit(0)

step("[2/4] Creating Nexthink client and retrieving token")
nxtClient = NexthinkClient(tenant, NxtRegionName(region), client_id=client_id, client_secret=client_secret)
if nxtClient.token is None:
    ko("Token retrieval failed.")
    sys.exit(1)
ok("Token retrieved successfully.")

step("[3/4] Executing NQL query")
console.print("Query id:", f"[bold]{nql_query_id}[/bold]")
nqlRequest = NxtNqlApiExecuteRequest(queryId=nql_query_id)
response = nxtClient.nql.execute(nqlRequest, version="v2")

step("[4/4] Displaying response")
if isinstance(response, NxtNqlApiExecuteResponse) or isinstance(response, NxtNqlApiExecuteV2Response):
    ok("NQL query executed successfully.")

    summary = {
        "rows": response.rows,
        "executionDateTime": response.executionDateTime,
    }

    panel(summary, title="NQL summary")
    panel(response.data, title="Data")
elif isinstance(response, NxtNqlApiExportResponse):
    ok("NQL export created successfully.")
    response = nxtClient.nql.wait(response)
    panel(response, title="Export status")
    res = nxtClient.nql.download(response)
    first_lines = [line for line in res.text.split('\n')[:10]]
    text_panel("\n".join(first_lines), title="First 10 export lines", border_style="cyan")
else:
    ko("NQL query returned an unexpected response.")
    panel(response, title="Response", border_style="red")
