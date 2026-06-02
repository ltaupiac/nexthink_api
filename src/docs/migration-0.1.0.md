# Migration From 0.0.9 To 0.1.0

`0.1.0` is a cleanup release for the public API. It keeps the historical
`NxtApiClient` available as a compatibility facade, but new code should use
`NexthinkClient` and domain properties.

## Client Entrypoint

Before:

```python
from nexthink_api import NxtApiClient, NxtRegionName

client = NxtApiClient(
    "tenant-name",
    NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)
```

After:

```python
from nexthink_api import NexthinkClient, NxtRegionName

client = NexthinkClient(
    "tenant-name",
    NxtRegionName.eu,
    client_id="client-id",
    client_secret="client-secret",
)
```

`NxtApiClient` remains importable for compatibility. Treat it as legacy code:
it should not be the entrypoint for new integrations.

Direct `NxtApiClient` construction emits `NxtLegacyApiWarning`. The warning is
a `FutureWarning` subclass so batch runs and test suites can see it by default
and migrate before the compatibility facade is removed.

## Domain Properties

The new public API groups calls by domain. Normal calls no longer need
`NxtEndpoint` arguments.

### Enrichment

Before:

```python
from nexthink_api import NxtEndpoint

response = client.run_enrichment(
    endpoint=NxtEndpoint.Enrichment,
    data=enrichment_request,
)
```

After:

```python
response = client.enrichment.run(enrichment_request)
```

### NQL Execute

Before:

```python
from nexthink_api import NxtEndpoint

response = client.run_nql(NxtEndpoint.Nql, data=nql_request)
```

After:

```python
response = client.nql.execute(nql_request, version="v2")
```

### NQL Export

Before:

```python
from nexthink_api import NxtEndpoint

export = client.run_nql(NxtEndpoint.NqlExport, data=nql_request)
status = client.wait_status(export)
download = client.download_export(status)
```

After:

```python
export = client.nql.export(nql_request)
status = client.nql.wait(export)
download = client.nql.download(status)
```

### Data Management

Before:

```python
response = client.delete_devices(
    devices=devices,
    request_id=request_id,
)
```

After:

```python
response = client.data_management.delete_devices(
    devices=devices,
    request_id=request_id,
)
```

## New Domains

`0.1.0` adds domain clients for API areas that were not part of the original
small surface:

```python
client.remote_actions.list()
client.campaigns.trigger(request)
client.workflows.list()
client.spark.handoff(request, user_principal_name="user@example.com")
```

Side-effecting operations such as Remote Action execution, Campaign trigger,
Workflow execution, Spark handoff, and Data Management deletion should keep an
explicit application-level confirmation in scripts.

## Runtime Contract

The package no longer relies on downloadable YAML files from the Nexthink
documentation site at runtime. Those files are not a stable distribution
contract for this package.

For normal users, this is not an application-code migration step. In `0.0.x`,
the YAML parser was mainly used internally by `NxtApiClient.check_method()` to
validate supported HTTP methods. User code normally did not need to load,
modify, or pass YAML files.

It only affects code that used undocumented internals directly, for example:

- importing `NxtYamlParser`;
- reading packaged files from `src/nexthink_api/yaml/`;
- depending on the old parser cache behavior;
- expecting `check_method()` to reflect local YAML file edits at runtime.

The runtime contract is now defined by:

- Python request and response models.
- Domain clients.
- Unit and integration tests.
- The local `SpecRegistry` for supported operations, methods, paths and
  response builders.

`NxtEndpoint` still exists for compatibility, internal routing, tests and
diagnostics. It is not required for normal `NexthinkClient` domain calls.

Historical facade methods such as `run_enrichment()`, `run_nql()`,
`delete_devices()`, `wait_status()`, `get_status_export()`,
`download_export()` and `download_export_as_df()` emit `NxtLegacyApiWarning`.
Use the domain properties shown above for new code.

## Authentication

Token retrieval now follows the official OAuth token endpoint:

```text
https://<tenant>-login.<region>.nexthink.cloud/oauth2/default/v1/token
```

The client sends Basic authentication built from `client_id:client_secret` and
the `client_credentials` form payload. Code that only instantiated the client
does not need to change beyond switching to `NexthinkClient`.

If your environment uses a corporate proxy with TLS inspection, for example
Zscaler, call `enable_truststore()` before creating the client:

```python
from nexthink_api import enable_truststore

enable_truststore()
```

This only enables an internal package flag. Nexthink HTTP calls use a dedicated
`requests.Session` adapter with a truststore SSL context, without monkey
patching Python SSL.

## Responses And Errors

`0.1.0` keeps a hybrid response strategy for compatibility:

| Case | Behavior |
| --- | --- |
| Documented success | Returns a typed response model, or a list of typed models for list operations. |
| Documented domain error | Returns the documented typed error model when implemented for that domain. |
| `401 Unauthorized` | Returns `NxtInvalidTokenRequest` for protected API domains. |
| Unsupported status code | Raises `NxtApiException`. |
| Expected JSON but non-JSON body | Raises `NxtApiException`, except for Spark documented non-JSON error handling. |
| Token transport failure | Raises `NxtTokenException` for token HTTP errors wrapped by the token provider. |

Do not assume every non-2xx response raises an exception. Some domains return
typed error models by design in `0.1.0`.

## Minimal Migration Checklist

- Replace `NxtApiClient` with `NexthinkClient` in new code.
- Replace direct `run_*` calls with domain property calls.
- Remove `NxtEndpoint` from normal application calls.
- Treat `NxtLegacyApiWarning` as a migration signal for old facade usage.
- Keep explicit `enable_truststore()` setup for corporate TLS inspection; it no
  longer permanently patches Python SSL for the whole process.
- Audit error handling to accept both typed error models and explicit
  exceptions depending on the domain.
- Only if your code imported package internals: remove direct usage of
  `NxtYamlParser`, packaged YAML files, parser cache behavior, or runtime YAML
  patching.
