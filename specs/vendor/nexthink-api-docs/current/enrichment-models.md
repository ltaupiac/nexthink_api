# Models

## The BadRequestResponse object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"BadRequestResponse":{"description":"Error response when ALL objects in the request contain errors","type":"object","properties":{"status":{"description":"Status of the request","type":"string","enum":["error"]},"errors":{"description":"List of all the individual errors for all objects","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/IndividualObjectError"}}}},"IndividualObjectError":{"description":"Error for an individual object, composed of identification information about the object and the list of errors","type":"object","properties":{"identification":{"description":"Field to be used to identify the object","type":"array","minimum":1,"maximum":1,"items":{"$ref":"#/components/schemas/Identification"}},"errors":{"description":"List of all the errors for the given object","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/Error"}}}},"Identification":{"description":"Identification information for the given object, composed of the name of the field and the value used to identify","type":"object","properties":{"name":{"description":"Name of the field to be used to identify the object","type":"string","enum":["device/device/name","device/device/uid","user/user/sid","user/user/uid","user/user/upn","binary/binary/uid","package/package/uid"]},"value":{"description":"Value to be used to identify the object","type":"string"}},"required":["name","value"]},"Error":{"description":"An error composed of a message and a code","type":"object","properties":{"message":{"description":"Error message with descriptive information about","minLength":1,"type":"string"},"code":{"description":"Internal error code","minLength":1,"type":"string"}}}}}}
```

## The Enrichment object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"Enrichment":{"description":"Enrichment composed of the identification information of the desired object and the fields to be enriched (names and values)","type":"object","properties":{"identification":{"description":"List of fields to be used to identify the object","type":"array","minimum":1,"maximum":1,"items":{"$ref":"#/components/schemas/Identification"}},"fields":{"description":"List of fields to be enriched","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/Field"}}},"required":["identification","fields"]},"Identification":{"description":"Identification information for the given object, composed of the name of the field and the value used to identify","type":"object","properties":{"name":{"description":"Name of the field to be used to identify the object","type":"string","enum":["device/device/name","device/device/uid","user/user/sid","user/user/uid","user/user/upn","binary/binary/uid","package/package/uid"]},"value":{"description":"Value to be used to identify the object","type":"string"}},"required":["name","value"]},"Field":{"description":"Enrichment information for the given object, composed of the name of field to be enriched and the desired value","type":"object","properties":{"name":{"description":"Name of the field to be enriched","type":"string","enum":["device/device/configuration_tag","device/device/virtualization/desktop_broker","device/device/virtualization/desktop_pool","device/device/virtualization/disk_image","device/device/virtualization/environment_name","device/device/virtualization/hostname","device/device/virtualization/hypervisor_name","device/device/virtualization/instance_size","device/device/virtualization/last_update","device/device/virtualization/region","device/device/virtualization/type","device/device/#<custom_field_name>","device/device/#<another_custom_field_name>","user/user/ad/city","user/user/ad/country_code","user/user/ad/department","user/user/ad/distinguished_name","user/user/ad/email_address","user/user/ad/full_name","user/user/ad/job_title","user/user/ad/last_update","user/user/ad/office","user/user/ad/organizational_unit","user/user/ad/username","user/user/#<custom_field_name>","binary/binary/#<custom_field_name>","package/package/#<custom_field_name>","user/user/organization/#<custom_field_name>"]},"value":{"description":"Desired value to be used while enriching","oneOf":[{"type":"string"},{"type":"integer"},{"type":"string","format":"date"}]}},"required":["name","value"]}}}}
```

## The EnrichmentRequest object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"EnrichmentRequest":{"description":"Objects to be enriched (with desired fields and values) and domain (configurable)","type":"object","properties":{"enrichments":{"description":"List of enrichments","type":"array","minimum":1,"maximum":10000,"items":{"$ref":"#/components/schemas/Enrichment"}},"domain":{"description":"Domain for which the given enrichment applies. For information and tracking purposes mainly","minLength":1,"type":"string"}},"required":["enrichments","domain"]},"Enrichment":{"description":"Enrichment composed of the identification information of the desired object and the fields to be enriched (names and values)","type":"object","properties":{"identification":{"description":"List of fields to be used to identify the object","type":"array","minimum":1,"maximum":1,"items":{"$ref":"#/components/schemas/Identification"}},"fields":{"description":"List of fields to be enriched","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/Field"}}},"required":["identification","fields"]},"Identification":{"description":"Identification information for the given object, composed of the name of the field and the value used to identify","type":"object","properties":{"name":{"description":"Name of the field to be used to identify the object","type":"string","enum":["device/device/name","device/device/uid","user/user/sid","user/user/uid","user/user/upn","binary/binary/uid","package/package/uid"]},"value":{"description":"Value to be used to identify the object","type":"string"}},"required":["name","value"]},"Field":{"description":"Enrichment information for the given object, composed of the name of field to be enriched and the desired value","type":"object","properties":{"name":{"description":"Name of the field to be enriched","type":"string","enum":["device/device/configuration_tag","device/device/virtualization/desktop_broker","device/device/virtualization/desktop_pool","device/device/virtualization/disk_image","device/device/virtualization/environment_name","device/device/virtualization/hostname","device/device/virtualization/hypervisor_name","device/device/virtualization/instance_size","device/device/virtualization/last_update","device/device/virtualization/region","device/device/virtualization/type","device/device/#<custom_field_name>","device/device/#<another_custom_field_name>","user/user/ad/city","user/user/ad/country_code","user/user/ad/department","user/user/ad/distinguished_name","user/user/ad/email_address","user/user/ad/full_name","user/user/ad/job_title","user/user/ad/last_update","user/user/ad/office","user/user/ad/organizational_unit","user/user/ad/username","user/user/#<custom_field_name>","binary/binary/#<custom_field_name>","package/package/#<custom_field_name>","user/user/organization/#<custom_field_name>"]},"value":{"description":"Desired value to be used while enriching","oneOf":[{"type":"string"},{"type":"integer"},{"type":"string","format":"date"}]}},"required":["name","value"]}}}}
```

## The Error object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"Error":{"description":"An error composed of a message and a code","type":"object","properties":{"message":{"description":"Error message with descriptive information about","minLength":1,"type":"string"},"code":{"description":"Internal error code","minLength":1,"type":"string"}}}}}}
```

## The Field object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"Field":{"description":"Enrichment information for the given object, composed of the name of field to be enriched and the desired value","type":"object","properties":{"name":{"description":"Name of the field to be enriched","type":"string","enum":["device/device/configuration_tag","device/device/virtualization/desktop_broker","device/device/virtualization/desktop_pool","device/device/virtualization/disk_image","device/device/virtualization/environment_name","device/device/virtualization/hostname","device/device/virtualization/hypervisor_name","device/device/virtualization/instance_size","device/device/virtualization/last_update","device/device/virtualization/region","device/device/virtualization/type","device/device/#<custom_field_name>","device/device/#<another_custom_field_name>","user/user/ad/city","user/user/ad/country_code","user/user/ad/department","user/user/ad/distinguished_name","user/user/ad/email_address","user/user/ad/full_name","user/user/ad/job_title","user/user/ad/last_update","user/user/ad/office","user/user/ad/organizational_unit","user/user/ad/username","user/user/#<custom_field_name>","binary/binary/#<custom_field_name>","package/package/#<custom_field_name>","user/user/organization/#<custom_field_name>"]},"value":{"description":"Desired value to be used while enriching","oneOf":[{"type":"string"},{"type":"integer"},{"type":"string","format":"date"}]}},"required":["name","value"]}}}}
```

## The ForbiddenResponse object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"ForbiddenResponse":{"description":"Error response when no permissions","type":"object","properties":{"message":{"description":"Error message when no permissions","type":"string"}}}}}}
```

## The Identification object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"Identification":{"description":"Identification information for the given object, composed of the name of the field and the value used to identify","type":"object","properties":{"name":{"description":"Name of the field to be used to identify the object","type":"string","enum":["device/device/name","device/device/uid","user/user/sid","user/user/uid","user/user/upn","binary/binary/uid","package/package/uid"]},"value":{"description":"Value to be used to identify the object","type":"string"}},"required":["name","value"]}}}}
```

## The IndividualObjectError object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"IndividualObjectError":{"description":"Error for an individual object, composed of identification information about the object and the list of errors","type":"object","properties":{"identification":{"description":"Field to be used to identify the object","type":"array","minimum":1,"maximum":1,"items":{"$ref":"#/components/schemas/Identification"}},"errors":{"description":"List of all the errors for the given object","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/Error"}}}},"Identification":{"description":"Identification information for the given object, composed of the name of the field and the value used to identify","type":"object","properties":{"name":{"description":"Name of the field to be used to identify the object","type":"string","enum":["device/device/name","device/device/uid","user/user/sid","user/user/uid","user/user/upn","binary/binary/uid","package/package/uid"]},"value":{"description":"Value to be used to identify the object","type":"string"}},"required":["name","value"]},"Error":{"description":"An error composed of a message and a code","type":"object","properties":{"message":{"description":"Error message with descriptive information about","minLength":1,"type":"string"},"code":{"description":"Internal error code","minLength":1,"type":"string"}}}}}}
```

## The PartialSuccessResponse object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"PartialSuccessResponse":{"description":"Partial success response when some of the objects in the request contain errors but other objects are processed","type":"object","properties":{"status":{"description":"Status of the request","type":"string","enum":["partial_success"]},"errors":{"description":"List of all the individual errors for those objects with error","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/IndividualObjectError"}}}},"IndividualObjectError":{"description":"Error for an individual object, composed of identification information about the object and the list of errors","type":"object","properties":{"identification":{"description":"Field to be used to identify the object","type":"array","minimum":1,"maximum":1,"items":{"$ref":"#/components/schemas/Identification"}},"errors":{"description":"List of all the errors for the given object","type":"array","minimum":1,"items":{"$ref":"#/components/schemas/Error"}}}},"Identification":{"description":"Identification information for the given object, composed of the name of the field and the value used to identify","type":"object","properties":{"name":{"description":"Name of the field to be used to identify the object","type":"string","enum":["device/device/name","device/device/uid","user/user/sid","user/user/uid","user/user/upn","binary/binary/uid","package/package/uid"]},"value":{"description":"Value to be used to identify the object","type":"string"}},"required":["name","value"]},"Error":{"description":"An error composed of a message and a code","type":"object","properties":{"message":{"description":"Error message with descriptive information about","minLength":1,"type":"string"},"code":{"description":"Internal error code","minLength":1,"type":"string"}}}}}}
```

## The SuccessResponse object

```json
{"openapi":"3.0.3","info":{"title":"Enrichment API","version":"1.31.0"},"components":{"schemas":{"SuccessResponse":{"description":"Response when ALL objects have been processed correctly","type":"object","properties":{"status":{"description":"Status of the request","type":"string","enum":["success"]}}}}}}
```


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/enrichment/models.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
