# NQL

The NQL API allows you to extract data from the Nexthink cloud platform, giving you the flexibility to create and visualize metrics using external applications.

### Setting up API credentials

To set up an integration using the Nexthink API, you must first create a set of dedicated credentials in your instance for your application or service. Refer to the [API Credentials](/api/readme.md) documentation.

#### Permissions

To enable proper permissions for NQL API queries:

1. Select **Administration** from the main menu.
2. Click on **Profile** from the navigation panel.
3. Click on the **New Profile** button to create a new profile or edit an existing profile by hovering over it and clicking on the edit icon to change the profile configuration.
4. In the **Permissions** section, scroll down to the **Administration** section and select **Manage all NQL API queries** to enable appropriate permissions for the profile.

Refer to the [Profiles](https://docs.nexthink.com/platform/latest/creating-a-profile) documentation for a detailed description of the permission options.

### Preparing queries

The NQL API executes predefined queries using the Nexthink web interface. Each query gets a unique ID, a required parameter for every API call.

**Accessing NQL API queries**

![Accessing NQL API queries](/files/Xnm9yJ4108okPgjd7q4x)

1. Log in to the Nexthink web interface.
2. Select **Administration** from the main menu.
3. Click on **NQL API queries** in the navigation panel in the Content Management section.

**Managing NQL API queries**

![Configure NQL Query](/files/mz5nLsCbaWp5gZ74RGlA)

1. Create a new NQL API query by clicking on the **New NQL API query** button in the top-right corner of the page.
2. Edit an existing query by hovering over it to reveal the action menu on the right side, click on it and select the **Edit** option.
3. Use the **Delete** option from the action menu to permanently delete a saved query.

**Configuring an NQL API query**

![Configure NQL Query](/files/cWPFPgxZNFEiFJqnZoZm)

* **Name:** Enter the name as you would like it to appear on the list of queries.
* **Query ID:** Enter an identifier for the query. Once you have created the query, you can no longer change the Query ID.
* **Description (optional):** Enter a description to help others understand the meaning and purpose of the query.
* **NQL query:** Write the NQL query to execute. Refer to the [NQL](https://docs.nexthink.com/platform/latest/nexthink-query-language-nql) documentation for more information.

#### Parameterized NQL queries

Parameterized NQL queries allow you to place parameters on a query instead of including a constant value. The system uses placeholders for parameters and provides the parameter value during execution. This approach allows you to reuse the query with different values for different purposes. For example, use a parameterized query to get the number of hard resets on a device, with a different device each time. With this generalized approach, you don’t need to write a separate query for each device.

Create a parameterized query:

1. Create a new NQL API query or edit an existing one.
2. Write an NQL query and explicitly name the parameters in the `where` clause. Parameters are allowed only in the `where` clause.
3. The parameter name must begin with a single `$` character and must be unique within the scope of the query.
4. The parameter datatype is inferred upon query execution.

```
execution.crashes during past 240h
| where device.collector.uid == $collector_uid
| summarize c1 = number_of_crashes.sum()
```

In the example above, `$collector_uid` is the placeholder for a Collector UID. Provide the UID value upon query execution.

### Choosing the right endpoint

The NQL API provides two separate endpoints to start the execution of a query:

* **api/v2/nql/execute** - highly optimized for relatively small requests at a high frequency.
* **api/v1/nql/export** - optimized for large queries at a low frequency.

The `execute` operation returns the results immediately in the response, however the `export` operation, since it is a longer and heavier operation, returns an identifier whose status you can consult at the following endpoint:

* **api/v1/nql/status/{exportId}** - Retrieves the status of an export and the URL link to a file containing the results once the execution is COMPLETE. For security, the URL link is only valid and accessible for 15 minutes after generation.

Suggested example use cases for each endpoint:

| Example                                            | Endpoint         |
| -------------------------------------------------- | ---------------- |
| Get a list of all devices, packages or executions. | `api/v1/export`  |
| Get detailed information about an execution.       | `api/v2/execute` |
| Integrate with a chatbot or self-service portal.   | `api/v2/execute` |
| Create a daily dashboard with operation data.      | `api/v1/export`  |

Both endpoints support the execution of the same NQL queries. However, the limits that apply to each NQL API endpoint are different. See the Limitations section below.

### Output formats

The `execute` operation supports both CSV and JSON formats.

The `status` endpoint associated with the `export` operation provides a URL to download a CSV file that contains the actual result of the NQL query.

### Limits

Nexthink makes continuous improvements to NQL to ensure optimal performance of all requests. Refer to the [Nexthink Infinity thresholds and limits overview](https://edocs.nexthink.com/nexthink-infinity/infinity-specifications/nexthink-infinity-default-thresholds-overview) for the list of the most up-to-date limits.

Nexthink aims to maintain optimal service performance. In the case of excessive and rapid acceleration of API use, Nexthink may temporarily pause access to the NQL API on a per-tenant basis.

### Supported compression algorithms

NQL Analytical API exports now support file compression using the GZIP and ZSTD algorithms, enabling faster downloads and smaller file sizes.

### Reduce throttling errors

Consider the following best practices to avoid throttling:

#### Targeted queries

Use filters to target your query to only the data you need. For example, if you want information about a specific device, use the `where` clause to restrict the returned data to only that device.

#### Catch errors caused by rate limiting

When throttling occurs, the API returns the HTTP status code 429, and the requests fail. It is best practice to catch 429 responses in your code and retry the request after a suitable waiting period. Refer to the value specified in the *Retry-After* header from the response.

#### Reducing the number of API requests

Optimize your code to eliminate any unnecessary API calls and cache frequently used data.

#### Regulate the request rate

If you regularly approach or bump into the rate limit, consider including a process in your code that regulates the rate of your requests so that they are more evenly distributed over time.

### Example

A set of utilities for different programming languages is available to integrate with `execute` and `export` operations. Below is an example of how to use PowerShell scripts and Power BI queries.

#### PowerShell

A collection of scripts compatible with PowerShell 7.2 (LTS) is available. These scripts enable customization of authentication credentials, NQL queries, parameters, output directory, file name, and format, as outlined in the [output](#output-formats) formats section.

* Execute NQL queries: [PowerShell script for `execute` operation](https://download.nexthink.com/integrations/NQL+API+Utils/PowerShell/nql_api_interactive.ps1)
* Export NQL query results: [PowerShell script for `export` operation](https://download.nexthink.com/integrations/NQL+API+Utils/PowerShell/nql_api_analytics.ps1)

#### Power BI

Nexthink offers two Power BI connectors as examples for connecting to the NQL API. These connectors allow the customization of authentication credentials, NQL queries, and parameters.

To start integration with NQL API, follow these steps:

* Install the custom connector from Power BI Desktop. Refer to the [Microsoft Power BI documentation](https://learn.microsoft.com/en-us/power-query/install-sdk#power-bi-desktop) for detailed installation instructions.<br>
* Open Power BI Desktop and click on **Get Data** in the toolbar.<br>

![Custom connectors in Power BI Desktop](/files/OKFFXLNjD2xiKJCvp6fR)<br>

* Type **Nexthink** in the search field to select the desired custom connector from the results.
* Click the **Connect** button. The configuration tab appears.
* Enter the necessary data and then click the **OK** buttom.<br>

![Custom connector configuration](/files/dcit4GXzOdix8ZoVyZHB)

Use custom connectors to:

* Execute NQL queries: [Power BI query custom connector for `execute` operation](https://download.nexthink.com/integrations/NQL+API+Utils/PowerBI/Nexthink-Interactive.mez)
* Export NQL results: [Power BI query custom connector for `export` operation](https://download.nexthink.com/integrations/NQL+API+Utils/PowerBI/Nexthink-Analytics.mez)


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/nql.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
