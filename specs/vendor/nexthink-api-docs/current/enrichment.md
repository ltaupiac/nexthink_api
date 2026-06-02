# Enrichment

Enrich object data in Nexthink inventory with attributes from outside sources using the Nexthink Enrichment API, allowing you to create integrations with external applications such as ServiceNow or Azure AD.

The Enrichment API allows you to update the values of any number of fields for any object. Enrich object data for manual custom fields (any object) or virtualization fields (devices only).

## Setting up API credentials

To set up an integration with the Nexthink API, you must first create a set of API credentials in your instance that the external application or service will use to access the API. Refer to the [API Credentials](/api/readme.md) documentation.

## Retrieving object IDs

The API accepts the following IDs:

* `device/device/name`
* `device/device/uid`
* `user/user/sid`
* `user/user/uid`
* `user/user/upn`
* `binary/binary/uid`
* `package/package/uid`

Device name information (`device/device/name`) as well as Windows security identifier (SID) and User Principal Name (UPN) for users (`user/user/sid` and `user/user/upn` respectively) might already exist in the source system.

> You can enable UPN opt-in metric collection at a Collector level using the [Collector Configuration](https://www.nexthink.com/library/collector-configuration) library pack. Only non-anonymized (cleartext) UPN is supported with the API. Library links:
>
> * [Set Anonymization Features macOS](https://www.nexthink.com/library/collector-configuration#set-anonymization-features-macos), setting: anonymize\_upn, value: cleartext
> * [Set Anonymization Features Windows](https://www.nexthink.com/library/collector-configuration#set-anonymization-features-windows), setting: anonymize\_upn, value: 2

Nexthink generates UID fields for all objects. Retrieve them by running [Investigations](https://docs.nexthink.com/platform/latest/investigations) and exporting the UID values to CSV.

## Retrieving field IDs

Depending on your use case, you might want to update device virtualization fields, user Entra ID fields or create custom fields to store the enrichment data. The following sections describe the flow for each use case. Combining both use cases into a single API call is also possible.

The system clears the data by sending an empty string as the value of the field that you want to clear.

### Entra ID

You can enrich the following user Entra ID properties:

* `user/user/ad/city` (string)
* `user/user/ad/country_code` (string)
* `user/user/ad/department` (string)
* `user/user/ad/distinguished_name` (string)
* `user/user/ad/email_address` (string)
* `user/user/ad/full_name` (string)
* `user/user/ad/job_title` (string)
* `user/user/ad/last_update` (datetime)
* `user/user/ad/office` (string)
* `user/user/ad/organizational_unit` (string)
* `user/user/ad/username` (string)

Find more information on these fields on the [NQL data model](https://docs.nexthink.com/platform/latest/nql-data-model) documentation page.

### Virtualization

You can enrich the following device virtualization properties:

* `device/device/virtualization/desktop_broker` enumeration with the following allowed values:
  * 0: sets null value
  * 1: citrix\_cvad
  * 2: citrix\_daas
  * 3: azure\_virtual\_desktops
  * 4: windows\_365
  * 5: horizon\_on\_prem
  * 6: aws\_workspace
  * 7: aws\_appstream
* `device/device/virtualization/desktop_pool` (string)
* `device/device/virtualization/disk_image` (string)
* `device/device/virtualization/environment_name` (string)
* `device/device/virtualization/hostname` (string)
* `device/device/virtualization/hypervisor_name` (string)
* `device/device/virtualization/instance_size` (string)
* `device/device/virtualization/last_update` (datetime)
* `device/device/virtualization/region` (string)
* `device/device/virtualization/type` (enumeration with the following allowed values: 1, 2, 3, corresponding to 1 - shared, 2 - personal, 3 - pooled)

Find more information on these fields on the [NQL data model](https://docs.nexthink.com/platform/latest/nql-data-model) documentation page.

### Configuring device organization

Assign a configurable label `device/device/configuration_tag` to identify a group of devices.

### Configuring user organization

Assign a configurable label `user/user/organization/#<custom_field_name>` to identify a group of users.

### Custom fields

First, create manual custom fields for each object attribute you wish to store, as described in the [Custom fields](https://docs.nexthink.com/platform/latest/custom-fields) documentation. All custom fields are of string type.

Next, create the field ID in the format required by the API as a concatenation of the object type and the NQL ID of the field.

1. Navigate to the custom fields administration page from the main menu.
2. Find the custom field you need the ID for and click on the action menu on the right side of the row to **Copy NQL ID**.
3. Paste the NQL ID into another location or tool to continue your work.
4. The field ID in the format required by the API is the NQL ID with the prefix `<object>/<object>/`.

### Example

If you have defined a custom field on binary objects with the NQL ID `#test_binary`, then its field ID for the API is `binary/binary/#test_binary`.

![](/files/vJWwzTtSJboSle9iHPPK)


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/enrichment.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
