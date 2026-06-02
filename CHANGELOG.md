# Changelog

All notable changes to this project are documented in this file.

## 0.1.0 - 2026-06-02

### Breaking Changes

- `NexthinkClient` is the recommended public entrypoint for new code.
  `NxtApiClient` remains available as a compatibility facade, but examples and
  documentation now use `NexthinkClient`.
- Public API calls are grouped by domain properties such as `client.nql`,
  `client.enrichment`, `client.data_management`, `client.remote_actions`,
  `client.campaigns`, `client.workflows` and `client.spark`.
- Normal application calls no longer need `NxtEndpoint` arguments. Historical
  facade methods remain available for compatibility, but new code should use
  domain methods. Direct `NxtApiClient` construction and historical facade
  methods now emit `NxtLegacyApiWarning`.
- Runtime YAML parsing has been removed from the public runtime contract.
  Supported operations, HTTP methods and metadata are now defined by code,
  tests and `SpecRegistry`.
- Response handling is explicit: documented successes return typed models,
  documented domain errors may return typed error models, unsupported status
  codes raise `NxtApiException`, and invalid JSON raises `NxtApiException`
  where JSON is expected.
- Corporate TLS inspection support is explicit. Applications and examples that
  need OS trust store support must call `enable_truststore()` before creating
  the client.

### Added

- First-class Data Management, Remote Actions, Campaigns, Workflows and Spark
  domain clients.
- Public models and response builders for the newly supported domains.
- Runnable examples for the supported domains.
- Migration documentation from `0.0.9` to `0.1.0`.

### Fixed

- `enable_truststore()` no longer monkey patches Python SSL globally. Nexthink
  HTTP calls now use a dedicated `requests.Session` adapter with a truststore
  SSL context when the feature is enabled.

### Notes

- `0.1.0` is a cleanup and completion release, not a long-term stability
  promise. `1.0.0` remains reserved until the `0.1.x` API surface has been used
  enough to confirm ergonomics and compatibility.
