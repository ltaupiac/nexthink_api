# Campaigns

Trigger campaigns using the Nexthink Campaigns API, giving you the flexibility to create integrations with external applications.

## Setting up API credentials

To set up an integration with the Nexthink API, you must first create a set of API credentials in your instance that the external application or service will use to access the API and send requests to Remote Actions. Refer to the [API Credentials](/api/readme.md) documentation.

## Configuring a campaign for API

1. Create a new campaign or edit an existing one as described in the [Manage Campaigns](https://docs.nexthink.com/platform/latest/manage-campaigns) documentation.
2. Under the **General** tab, check the **API** check box.

![Enabling a campaign for the API](/files/qypSY899d9jv7aIgUs3H)

## Copying a campaign ID

To trigger a campaign via the API, you must know its NQL ID.

1. Select **Campaigns** from the main menu.
2. Click the **Manage campaigns** button at the bottom of the navigation panel.
3. Find the campaign you need the ID for and edit it.
4. Save the NQL ID for late use.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/campaigns.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
