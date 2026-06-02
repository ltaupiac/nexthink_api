# API credentials

Accessing features using the Nexthink APIs gives you the flexibility to create integrations from external third-party tools. Using APIs helps remove complexity, as IT teams do not have to access multiple consoles to carry out their work. API credentials provide authentication based on the OAuth client credentials, which you can manage using the Nexthink web interface.

## Accessing API credentials

To set up an integration with a Nexthink API, you must first create a set of API credentials for your instance that the external application or service must use to access the API and send requests.

Nexthink public API relies on OAuth 2.0. It comprises a Client Secret and Client ID, which the system uses to generate an access token to call an application or service.

To set up new credentials for your application:

1. Log in to the Nexthink web interface.
2. Select **Administration** from the main menu.
3. Click on **API credentials** in the navigation panel from the Account Management section.

![Accessing the API credential configuration screen](/files/TIMHMcIJ8gQe63cEswa6)

## Creating API credentials

Click on the **New OAuth client credentials** button located in the top-right of the API credentials page.

<figure><img src="/files/XjF39DBYKjn0vXsfXVpn" alt=""><figcaption></figcaption></figure>

* **Name**: provide a meaningful name for the credential. Nexthink recommends using the name of the application you are configuring to call the API.
* **Description**: enter a description to inform users what applications and services use the credentials and why.
* **Permissions**: select the features you want to enable the permissions for. Some permissions are related to features that may not be available to you, for example, features in technical preview or those not included in your license.
  * **Remote Actions API**: Select the checkbox to send API calls to trigger and query remote actions.
  * **Enrichment API**: Select the checkbox to send API calls to operate the enrichment feature.
  * **Data management**: Select the checkbox to send API calls to manage devices.
  * **Workflows API**: Select the checkbox to send API calls to trigger and query workflows.
  * **Campaigns API**: Select the checkbox to send API calls to trigger campaigns.
  * **NQL API**: Select the checkbox to send API calls to extract data.
  * **Spark API**: Select the checkbox to send API calls to transfer a live conversation to Spark.
* Click on **Save and generate credentials** to generate the credentials. A new modal appears with the OAuth client credentials.

![Client ID and secret key](/files/ZUr0JDEN2P1anBxhrLs1)

For security reasons, the credentials appear only once. Copy and save them securely, as you cannot access them beyond this point.

* Click on the **Copy** button for **Client ID** and **Secret key,** then paste the information into the secure vault authorized by your organization.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/readme.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
