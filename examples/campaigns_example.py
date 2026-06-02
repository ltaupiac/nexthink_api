# pylint: skip-file
# ruff: noqa

import os
import sys
from importlib.metadata import PackageNotFoundError, version

from rich_output import console, ko, ok, panel, step
from nexthink_api import (
    NexthinkClient,
    NxtCampaignTriggerErrorResponse,
    NxtCampaignTriggerRequest,
    NxtCampaignTriggerSuccessResponse,
    NxtInvalidTokenRequest,
    NxtRegionName,
    enable_truststore,
)

# Enable OS trust store support for Nexthink HTTP calls behind corporate TLS
# inspection proxies. This does not monkey patch Python SSL globally.
enable_truststore()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant = os.getenv("nexthink_tenant") or os.getenv("nxt_instance") or "your-tenant-name"
region = os.getenv("nexthink_region", NxtRegionName.eu.value)
default_campaign_nql_id = "#your_campaign_nql_id"
default_user_sid = "S-1-5-21-user-sid"
campaign_nql_id = os.getenv("nexthink_campaign_nql_id", default_campaign_nql_id)
user_sid = os.getenv("nexthink_campaign_user_sid", default_user_sid)
confirm_trigger = os.getenv("confirm_campaign_trigger")

if client_id is None or client_secret is None:
    ko("client_id or client_secret not found")
    sys.exit(1)

step("[1/4] Checking local package version")
try:
    ok(f"nexthink_api version: {version('nexthink_api')}")
except PackageNotFoundError:
    ko("nexthink_api version: package metadata not found")

step("[2/4] Creating Nexthink client and retrieving token")
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

if not campaign_nql_id or campaign_nql_id == default_campaign_nql_id:
    console.print()
    console.print("Set nexthink_campaign_nql_id to a real campaign NQL ID before triggering.")
    sys.exit(0)
if not user_sid or user_sid == default_user_sid:
    console.print()
    console.print("Set nexthink_campaign_user_sid to a real user SID before triggering.")
    sys.exit(0)

step("[3/4] Preparing campaign trigger request")
request = NxtCampaignTriggerRequest(
    campaignNqlId=campaign_nql_id,
    userSid=[user_sid],
    expiresInMinutes=60,
)

panel(request.model_dump(exclude_none=True), title="Campaign trigger request")

step("[4/4] Checking trigger confirmation")
if confirm_trigger != "yes":
    console.print()
    console.print("Set confirm_campaign_trigger=yes to trigger this campaign.")
    sys.exit(0)

step("Triggering campaign")
response = nxt_client.campaigns.trigger(request)
if isinstance(response, NxtCampaignTriggerSuccessResponse):
    ok("Campaign trigger accepted.")
    panel(response.model_dump(), title="Campaign trigger response")
elif isinstance(response, NxtCampaignTriggerErrorResponse):
    ko("Campaign trigger error.")
    panel(response.model_dump(), title="Campaign trigger error", border_style="red")
elif isinstance(response, NxtInvalidTokenRequest):
    ko("Invalid token")
else:
    panel(response, title="Response", border_style="red")
