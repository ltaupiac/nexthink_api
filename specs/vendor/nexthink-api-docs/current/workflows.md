# Workflows

Trigger and query workflows using the Nexthink API, giving you the flexibility to create and visualize metrics using third-party software.

## Setting up API credentials

To set up an integration with the Nexthink API, you must first create a set of API credentials in your instance that the external application or service uses to access the Workflows API. Refer to the [API Credentials](/api/readme.md) documentation.

## Configuring workflows for API

To configure workflows via API:

1. Select **Workflows** from the main menu.
2. Create a **New** workflow or edit an existing one as described in the [Manage Workflows](https://docs.nexthink.com/platform/latest/manage-workflows) documentation.
3. Under the **General** tab, select the **API** checkbox.
4. Click the **Save workflow** button. The workflow is now available for API calls.

![image.png](/files/5UrXXobQKhyiwcq45zfh)

Alternatively, configure workflows by editing an existing one through the the Manage workflows page:

* Select **Manage workflows**.
* Select the relevant workflow and then click on the action menu on the right side of the row to **Edit**.

## Copying workflow NQL ID

1. Select **Workflows** > **Manage workflows** in the navigation panel.
2. Select the relevant workflow and then click on the action menu on the right side of the row to **Copy NQL ID**.
3. Save the workflow NQL ID for later use.

![ManageWorflow](/files/yxaU6NC4az2hn1CgDjpZ)

Extract the workflow NQL ID by querying it from the API.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/workflows.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
