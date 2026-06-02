# Remote Actions

Trigger and query remote actions using the Nexthink API, allowing you to create integrations with external applications like ServiceNow.

{% hint style="info" %}
For the execute calls, obtain the Collector IDs using the [data export](https://docs.nexthink.com/platform/latest/data-export) or the [CSV export](https://docs.nexthink.com/platform/latest/investigations). In the future, the upcoming NQL API will allow you to fetch those IDs directly.
{% endhint %}

## Setting up API credentials

To set up an integration with the Nexthink API, you must first create a set of API credentials in your instance that the external application or service uses to access the API and send requests to Remote Actions. For more information, refer to the [API Credentials](/api/readme.md) documentation.

## Configuring remote actions for API

1. Create a new remote action or edit an existing one as described in the [Manage Remote Actions](https://docs.nexthink.com/platform/latest/manage-remote-actions) documentation.
2. Under the **General** tab, select the **API** check box.
3. Click on the **Save Remote Action** button.<br>

<figure><img src="/files/xQ2iYICZqoq4RcsTryBJ" alt=""><figcaption></figcaption></figure>

The remote action is now available for API calls.

## Copying a remote action ID

To trigger a remote action via API, you must know its ID.

1. Select **Remote Actions** from the main menu.
2. Click the **Manage remote actions** button at the bottom of the navigation panel.
3. Find the remote action you need the ID for and click on the action menu on the right side of the row to **Copy NQL ID**.4. Save the NQL ID for late use.

![Copy NQL ID](/files/sjrfqOTGrghvc9YagEX2)

Extract the remote action ID by querying it from the API.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/remote-actions.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
