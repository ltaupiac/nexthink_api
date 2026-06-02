# pylint: skip-file
# ruff: noqa

import os
import sys
from importlib.metadata import PackageNotFoundError, version

from rich_output import console, ko, ok, panel, step
from nexthink_api import (
    NexthinkClient,
    NxtInvalidTokenRequest,
    NxtRegionName,
    NxtSparkErrorResponse,
    NxtSparkHandoffConversationMessageRequest,
    NxtSparkHandoffSuccessResponse,
    NxtSparkMessageDTO,
    NxtSparkTextPartDTO,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
default_user_principal_name = "user@example.com"
user_principal_name = os.getenv("nexthink_spark_user_principal_name", default_user_principal_name)
timezone = os.getenv("nexthink_spark_timezone")
message_text = os.getenv("nexthink_spark_message", "I need help from IT")
confirm_handoff = os.getenv("confirm_spark_handoff")
spark_handoff_api = "POST /api/v1/spark/handoff"

if client_id is None or client_secret is None:
    ko("client_id or client_secret not found")
    sys.exit(1)

step("[1/5] Checking local package version")
try:
    ok(f"nexthink_api version: {version('nexthink_api')}")
except PackageNotFoundError:
    ko("nexthink_api version: package metadata not found")

step("[2/5] Creating Nexthink client and retrieving token")
nxt_client = NexthinkClient(
    tenant,
    NxtRegionName(region),
    client_id=client_id,
    client_secret=client_secret,
)

if nxt_client.token is None:
    ko("Token retrieval failed.")
    sys.exit(1)

ok("Token retrieved successfully.")

if not user_principal_name or user_principal_name == default_user_principal_name:
    console.print()
    console.print("Set nexthink_spark_user_principal_name to a real user UPN before handoff.")
    sys.exit(0)

step("[3/5] Preparing Spark handoff request")
console.print("API:", spark_handoff_api)
request = NxtSparkHandoffConversationMessageRequest(
    metadata={"source": "nexthink_api example"},
    message=NxtSparkMessageDTO(parts=[NxtSparkTextPartDTO(text=message_text)]),
)

panel(request.model_dump(exclude_none=True, mode="json"), title="Spark handoff request")
console.print("Spark user principal name:", user_principal_name)
if timezone:
    console.print("Spark timezone:", timezone)

step("[4/5] Checking handoff confirmation")
if confirm_handoff != "yes":
    console.print()
    console.print("Set confirm_spark_handoff=yes to hand off this conversation to Spark.")
    sys.exit(0)

step("[5/5] Handing off conversation to Spark")
console.print("API:", spark_handoff_api)
response = nxt_client.spark.handoff(
    request,
    user_principal_name=user_principal_name,
    timezone=timezone,
)
if isinstance(response, NxtSparkHandoffSuccessResponse):
    ok("Spark handoff accepted.")
    panel(response.model_dump(), title="Spark handoff response")
elif isinstance(response, NxtSparkErrorResponse):
    ko("Spark handoff error.")
    panel(response.model_dump(), title="Spark handoff error", border_style="red")
elif isinstance(response, NxtInvalidTokenRequest):
    ko("Invalid token")
else:
    panel(response, title="Response", border_style="red")
