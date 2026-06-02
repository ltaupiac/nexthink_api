# Spark

## Spark API overview

Meet employees where they are. Spark provides a standard handover mechanism that allows third-party chatbots to transfer a live conversation to Spark without losing context. The process consists of the following steps:

1. Employees initiate an IT request through a familiar enterprise chatbot interface.
2. The chatbot forwards the user message to Spark using the Handoff API.
3. Spark responds in Microsoft Teams and notifies the employee.
4. The employee continues the resolution in Microsoft Teams by interacting with Spark.

This ensures a seamless employee experience and minimizes development effort.

## Setting up API credentials

To set up an integration with the Nexthink API, you must first create a set of API credentials in your instance that the external application or service uses to access the Spark API. Refer to the [API Credentials](/api/readme.md) documentation.

## Configuring Spark for API

The Spark redirection API does not require any configuration within the Nexthink platform. Redirection is currently handled automatically through the Spark MS Teams application.

Refer to [Handoff API](/api/spark/handoff-api.md) for more details about request structure, authentication requirements, and supported parameters.


---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.nexthink.com/api/spark.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
