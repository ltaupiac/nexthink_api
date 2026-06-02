"""Unit tests for the static Nexthink API spec registry."""

from collections import Counter
from dataclasses import fields
from pathlib import Path

from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Utils.nxt_spec_registry import EndpointSpec, SpecRegistry

HTTP_SUCCESS_MIN = 200
HTTP_SUCCESS_MAX = 300
HTTP_ERROR_MIN = 400
HTTP_ERROR_MAX = 600


def _project_root() -> Path:
    """Return the project root from this test file."""
    return next(parent for parent in Path(__file__).resolve().parents if (parent / "pyproject.toml").exists())


def test_endpoint_spec_stays_minimal() -> None:
    """Endpoint specs contain only the metadata the client uses."""
    assert {field.name for field in fields(EndpointSpec)} == {
        "api",
        "operation",
        "endpoint",
        "method",
        "path",
        "docs_url",
        "models_docs_url",
        "success_statuses",
        "error_statuses",
        "response_builder",
    }


def test_registry_supports_current_runtime_operations() -> None:
    """Registry exposes method support without reading runtime YAML files."""
    assert SpecRegistry.supports_method(NxtEndpoint.Enrichment, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.DataManagement, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.Act, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.RemoteActions, "GET") is True
    assert SpecRegistry.supports_method(NxtEndpoint.RemoteActionsDetails, "GET") is True
    assert SpecRegistry.supports_method(NxtEndpoint.Engage, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.Workflow, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.WorkflowV2, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.WorkflowThinkletTrigger, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.Workflows, "GET") is True
    assert SpecRegistry.supports_method(NxtEndpoint.WorkflowDetails, "GET") is True
    assert SpecRegistry.supports_method(NxtEndpoint.SparkHandoff, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.Nql, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.NqlV2, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.NqlExport, "POST") is True
    assert SpecRegistry.supports_method(NxtEndpoint.NqlExport, "GET") is True
    assert SpecRegistry.supports_method(NxtEndpoint.NqlStatus, "GET") is True


def test_registry_runtime_contract_matches_supported_operations() -> None:
    """Registry keeps the supported runtime operation surface explicit."""
    expected_contract = {
        (NxtEndpoint.Act, "POST", "executeRA", "remote_actions"),
        (NxtEndpoint.RemoteActions, "GET", "getAllRemoteActions", "remote_actions"),
        (NxtEndpoint.RemoteActionsDetails, "GET", "getRemoteActionByNqlId", "remote_actions"),
        (NxtEndpoint.Engage, "POST", "triggerCampaign", "campaigns"),
        (NxtEndpoint.Workflow, "POST", "executeEA", "workflows"),
        (NxtEndpoint.WorkflowV2, "POST", "executeEAWithExternalIds", "workflows"),
        (NxtEndpoint.WorkflowThinkletTrigger, "POST", "triggerThinklet", "workflows"),
        (NxtEndpoint.Workflows, "GET", "getAllWorkflows", "workflows"),
        (NxtEndpoint.WorkflowDetails, "GET", "getWorkflow", "workflows"),
        (NxtEndpoint.SparkHandoff, "POST", "handleHandoffRequest", "spark"),
        (NxtEndpoint.DataManagement, "POST", "deleteDevices", "data_management"),
        (NxtEndpoint.Enrichment, "POST", "enrichmentDataFields", "enrichment"),
        (NxtEndpoint.Nql, "POST", "execute", "nql"),
        (NxtEndpoint.NqlV2, "POST", "executeV2", "nql"),
        (NxtEndpoint.NqlExport, "POST", "export", "nql"),
        (NxtEndpoint.NqlExport, "GET", "export", "nql"),
        (NxtEndpoint.NqlStatus, "GET", "status", "nql"),
        (NxtEndpoint.Token, "POST", "getToken", "token"),
    }
    actual_contract = {
        (spec.endpoint, spec.method, spec.operation, spec.response_builder)
        for spec in SpecRegistry.all()
    }

    assert actual_contract == expected_contract


def test_registry_token_operation_uses_official_oauth_path() -> None:
    """Auth registry metadata points to the official OAuth token path."""
    spec = SpecRegistry.find(NxtEndpoint.Token, "POST")

    assert spec is not None
    assert spec.path == "/oauth2/default/v1/token"
    assert spec.docs_url == "https://docs.nexthink.com/api/getting-authentication-token.md"


def test_every_endpoint_constant_used_by_current_facade_is_registered() -> None:
    """Compatibility facade endpoints are all backed by registry entries."""
    registered_endpoints = {spec.endpoint for spec in SpecRegistry.all()}

    assert {
        NxtEndpoint.Act,
        NxtEndpoint.Engage,
        NxtEndpoint.Workflow,
        NxtEndpoint.WorkflowV2,
        NxtEndpoint.WorkflowThinkletTrigger,
        NxtEndpoint.WorkflowDetails,
        NxtEndpoint.Workflows,
        NxtEndpoint.SparkHandoff,
        NxtEndpoint.RemoteActions,
        NxtEndpoint.RemoteActionsDetails,
        NxtEndpoint.DataManagement,
        NxtEndpoint.Enrichment,
        NxtEndpoint.Nql,
        NxtEndpoint.NqlV2,
        NxtEndpoint.NqlExport,
        NxtEndpoint.NqlStatus,
        NxtEndpoint.Token,
    } <= registered_endpoints


def test_every_registry_method_path_pair_is_unique() -> None:
    """An operation is uniquely identified by its HTTP method and path."""
    method_path_pairs = [(spec.method, spec.path) for spec in SpecRegistry.all()]

    assert [pair for pair, count in Counter(method_path_pairs).items() if count > 1] == []


def test_shared_registry_paths_are_explicit() -> None:
    """Shared paths are allowed only when different methods intentionally share them."""
    allowed_shared_paths = {NxtEndpoint.NqlExport.value}
    path_counts = Counter(spec.path for spec in SpecRegistry.all())
    shared_paths = {path for path, count in path_counts.items() if count > 1}

    assert shared_paths == allowed_shared_paths


def test_registry_rejects_unsupported_methods() -> None:
    """Registry rejects methods that are not declared for an endpoint."""
    assert SpecRegistry.supports_method(NxtEndpoint.Enrichment, "GET") is False
    assert SpecRegistry.supports_method(NxtEndpoint.DataManagement, "GET") is False
    assert SpecRegistry.supports_method(NxtEndpoint.Engage, "GET") is False
    assert SpecRegistry.supports_method(NxtEndpoint.Workflow, "GET") is False
    assert SpecRegistry.supports_method(NxtEndpoint.SparkHandoff, "GET") is False
    assert SpecRegistry.supports_method(NxtEndpoint.Nql, "GET") is False


def test_registry_normalizes_method_case() -> None:
    """Registry accepts lower-case method names from callers."""
    assert SpecRegistry.supports_method(NxtEndpoint.DataManagement, "post") is True


def test_every_registry_entry_has_traceability_urls() -> None:
    """Registered runtime operations keep a link to their documentation source."""
    for spec in SpecRegistry.all():
        assert spec.docs_url.startswith("https://docs.nexthink.com/api/")
        if spec.api != "Authentication":
            assert spec.models_docs_url is not None
            assert spec.models_docs_url.startswith("https://docs.nexthink.com/api/")


def test_every_registry_entry_has_response_builder() -> None:
    """No registered runtime operation is allowed to point to a missing builder."""
    supported_builders = {
        "campaigns",
        "data_management",
        "enrichment",
        "nql",
        "remote_actions",
        "spark",
        "token",
        "workflows",
    }

    for spec in SpecRegistry.all():
        assert spec.response_builder in supported_builders


def test_every_registry_entry_has_valid_runtime_invariants() -> None:
    """Runtime specs contain coherent method, path and status metadata."""
    supported_methods = {"GET", "POST"}

    for spec in SpecRegistry.all():
        assert spec.api
        assert spec.operation
        assert spec.method in supported_methods
        if spec.endpoint == NxtEndpoint.Token:
            assert spec.path.startswith("/")
        else:
            assert spec.path.startswith(spec.endpoint.value)
        assert spec.success_statuses
        assert spec.error_statuses
        assert set(spec.success_statuses).isdisjoint(spec.error_statuses)
        assert all(HTTP_SUCCESS_MIN <= int(status) < HTTP_SUCCESS_MAX for status in spec.success_statuses)
        assert all(HTTP_ERROR_MIN <= int(status) < HTTP_ERROR_MAX for status in spec.error_statuses)


def test_implemented_api_runtime_code_does_not_depend_on_yaml_parser() -> None:
    """Implemented API domains do not import the historical YAML parser."""
    root = _project_root()
    production_api_paths = [
        root / "src/nexthink_api/Clients",
        root / "src/nexthink_api/Campaigns",
        root / "src/nexthink_api/DataManagement",
        root / "src/nexthink_api/Enrichment",
        root / "src/nexthink_api/Nql",
        root / "src/nexthink_api/RemoteActions",
        root / "src/nexthink_api/Spark",
        root / "src/nexthink_api/Workflows",
    ]

    for production_path in production_api_paths:
        for source_file in production_path.glob("*.py"):
            source = source_file.read_text(encoding="utf-8")
            assert "NxtYamlParser" not in source
            assert "nxt_yaml_parser" not in source


def test_package_no_longer_contains_runtime_yaml_artifacts() -> None:
    """Runtime package no longer ships historical YAML or PKL artifacts."""
    package_root = _project_root() / "src/nexthink_api"

    assert not (package_root / "yaml").exists()
    assert not (package_root / "Pkl").exists()
    assert not (package_root / "Utils/nxt_yaml_parser.py").exists()

    for artifact in package_root.rglob("*"):
        if artifact.is_file():
            assert artifact.suffix not in {".yaml", ".yml", ".pkl"}
            assert "nxt_yaml_parser" not in artifact.name
