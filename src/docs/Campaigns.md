# Campaigns

Campaigns exposes Nexthink campaign triggering through
`NexthinkClient.campaigns`.

Triggering a campaign sends it to real users. Keep an explicit operator
confirmation in scripts that run outside tests.

## Trigger a campaign

```python
from nexthink_api import NexthinkClient, NxtRegionName
from nexthink_api.Campaigns import NxtCampaignTriggerRequest

client = NexthinkClient(
    instance="example",
    region=NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)

request = NxtCampaignTriggerRequest(
    campaignNqlId="#campaign_nql_id",
    userSid=["S-1-5-21-..."],
    expiresInMinutes=60,
    parameters={"language": "fr"},
)

result = client.campaigns.trigger(request)
```

`userSid` accepts between 1 and 10000 user SIDs. `expiresInMinutes` must be
between 1 and 525600. `parameters` accepts up to 30 entries when provided.

See [Campaigns object models](object-models/Campaigns.md) for the request and
response classes used by this domain.
