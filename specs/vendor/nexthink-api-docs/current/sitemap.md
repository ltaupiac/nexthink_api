# Nexthink API

## Nexthink API&#x20;

- [API credentials](https://docs.nexthink.com/api/readme.md)
- [Getting an authentication token](https://docs.nexthink.com/api/getting-authentication-token.md)
- [Campaigns](https://docs.nexthink.com/api/campaigns.md)
- [Trigger a campaign](https://docs.nexthink.com/api/campaigns/trigger-a-campaign.md): Send campaigns to users using the Nexthink public API.
- [Models](https://docs.nexthink.com/api/campaigns/models.md)
- [Data management](https://docs.nexthink.com/api/data-management.md)
- [Schedule device deletions](https://docs.nexthink.com/api/data-management/schedule-device-deletions.md): Schedule batch deletion of devices from the Nexthink inventory.
- [Models](https://docs.nexthink.com/api/data-management/models.md)
- [Enrichment](https://docs.nexthink.com/api/enrichment.md)
- [Enrich fields for given objects](https://docs.nexthink.com/api/enrichment/enrich-fields-for-given-objects.md): Enrich object data in the Nexthink inventory with specific information.
- [Models](https://docs.nexthink.com/api/enrichment/models.md)
- [NQL](https://docs.nexthink.com/api/nql.md)
- [Execute an NQL](https://docs.nexthink.com/api/nql/execute-an-nql.md): Execute NQL queries and retrieve data in JSON or CSV format
- [Export an NQL](https://docs.nexthink.com/api/nql/export-an-nql.md): Export large datasets to S3 and track export status
- [Models](https://docs.nexthink.com/api/nql/models.md)
- [Remote Actions](https://docs.nexthink.com/api/remote-actions.md)
- [Remote actions API](https://docs.nexthink.com/api/remote-actions/remote-actions-api.md): Trigger and query remote actions using the Nexthink API.
- [Models](https://docs.nexthink.com/api/remote-actions/models.md)
- [Spark](https://docs.nexthink.com/api/spark.md)
- [Handoff API](https://docs.nexthink.com/api/spark/handoff-api.md)
- [Models](https://docs.nexthink.com/api/spark/models.md)
- [Workflows](https://docs.nexthink.com/api/workflows.md)
- [Trigger a workflow](https://docs.nexthink.com/api/workflows/trigger-a-workflow.md): Trigger and query workflows using the Nexthink API.
- [Models](https://docs.nexthink.com/api/workflows/models.md)


---

# Agent Instructions: Querying This Documentation

If you need additional information, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on a page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/readme.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
