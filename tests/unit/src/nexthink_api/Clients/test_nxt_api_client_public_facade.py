"""Compatibility tests for the historical NxtApiClient public facade."""

import inspect
from typing import Union

import pandas as pd
import pytest
import requests
from nexthink_api import NxtApiClient, NxtEndpoint, NxtLegacyApiWarning, NxtUidValidationMode
from nexthink_api.Clients.nxt_campaigns_client import NxtCampaignsClient
from nexthink_api.Clients.nxt_data_management_client import NxtDataManagementClient
from nexthink_api.Clients.nxt_enrichment_client import NxtEnrichmentClient
from nexthink_api.Clients.nxt_nql_client import NxtNqlClient
from nexthink_api.Clients.nxt_remote_actions_client import NxtRemoteActionsClient
from nexthink_api.Clients.nxt_spark_client import NxtSparkClient
from nexthink_api.Clients.nxt_workflows_client import NxtWorkflowsClient
from nexthink_api.Clients.nxt_response import DataManagementResponseType, EnrichmentResponseType, NqlResponseType
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse
from nexthink_api.Nql.nxt_nql_api_status_response import NxtNqlApiStatusResponse

DEFAULT_EXPORT_TIMEOUT = 300


def _legacy_call(callable_object: object, *args: object, **kwargs: object) -> object:
    """Call a legacy facade method while asserting its deprecation warning."""
    with pytest.warns(NxtLegacyApiWarning, match="is deprecated"):
        return callable_object(*args, **kwargs)


def _parameter_names(method_name: str) -> list[str]:
    """Return public method parameter names in declaration order."""
    return list(inspect.signature(getattr(NxtApiClient, method_name)).parameters)


def test_domain_facade_methods_remain_on_nxt_api_client() -> None:
    """Domain methods remain available from the historical public facade."""
    for method_name in [
        "run_enrichment",
        "run_nql",
        "delete_devices",
        "wait_status",
        "get_status_export",
        "download_export",
        "download_export_as_df",
    ]:
        assert callable(getattr(NxtApiClient, method_name))


def test_domain_facade_method_parameters_remain_compatible() -> None:
    """Domain facade methods keep their public parameter names and ordering."""
    assert _parameter_names("run_enrichment") == ["self", "endpoint", "data"]
    assert _parameter_names("run_nql") == ["self", "endpoint", "data", "method"]
    assert _parameter_names("delete_devices") == ["self", "devices", "request_id", "uid_validation"]
    assert _parameter_names("wait_status") == ["self", "value", "timeout"]
    assert _parameter_names("get_status_export") == ["self", "value"]
    assert _parameter_names("download_export") == ["self", "value", "timeout"]
    assert _parameter_names("download_export_as_df") == ["self", "value", "timeout"]


def test_domain_facade_method_defaults_remain_compatible() -> None:
    """Domain facade methods keep their historical default values."""
    run_nql = inspect.signature(NxtApiClient.run_nql)
    delete_devices = inspect.signature(NxtApiClient.delete_devices)
    wait_status = inspect.signature(NxtApiClient.wait_status)
    download_export = inspect.signature(NxtApiClient.download_export)
    download_export_as_df = inspect.signature(NxtApiClient.download_export_as_df)

    assert run_nql.parameters["method"].default is None
    assert delete_devices.parameters["request_id"].default is None
    assert delete_devices.parameters["uid_validation"].default == NxtUidValidationMode.WARN
    assert wait_status.parameters["timeout"].default == DEFAULT_EXPORT_TIMEOUT
    assert download_export.parameters["timeout"].default == DEFAULT_EXPORT_TIMEOUT
    assert download_export_as_df.parameters["timeout"].default == DEFAULT_EXPORT_TIMEOUT


def test_domain_facade_return_annotations_remain_compatible() -> None:
    """Domain facade methods keep their historical return annotations."""
    assert inspect.signature(NxtApiClient.run_enrichment).return_annotation == EnrichmentResponseType
    assert inspect.signature(NxtApiClient.run_nql).return_annotation == NqlResponseType
    assert inspect.signature(NxtApiClient.delete_devices).return_annotation == DataManagementResponseType
    assert inspect.signature(NxtApiClient.wait_status).return_annotation == Union[
        NxtNqlApiStatusResponse,
        NxtErrorResponse,
    ]
    assert inspect.signature(NxtApiClient.get_status_export).return_annotation == NqlResponseType
    assert inspect.signature(NxtApiClient.download_export).return_annotation == requests.models.Response
    assert inspect.signature(NxtApiClient.download_export_as_df).return_annotation == pd.DataFrame


def test_generic_facade_methods_remain_on_nxt_api_client() -> None:
    """Generic GET/POST facade methods remain available for compatibility."""
    assert _parameter_names("get") == ["self", "endpoint", "params"]
    assert _parameter_names("post") == ["self", "endpoint", "data", "headers"]
    assert inspect.signature(NxtApiClient.get).parameters["params"].default is None
    assert inspect.signature(NxtApiClient.post).parameters["headers"].default is None


def test_enrichment_public_facade_delegates_to_internal_client(mocker: object) -> None:
    """Historical Enrichment facade delegates behavior to the internal client."""
    client = object.__new__(NxtApiClient)
    client._enrichment_client = mocker.Mock()
    client._enrichment_client.run_enrichment.return_value = object()
    request = object()

    value = _legacy_call(client.run_enrichment, NxtEndpoint.Enrichment, request)

    assert value is client._enrichment_client.run_enrichment.return_value
    client._enrichment_client.run_enrichment.assert_called_once_with(NxtEndpoint.Enrichment, request)


def test_enrichment_domain_property_returns_internal_client(mocker: object) -> None:
    """New Enrichment domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._enrichment_client = mocker.Mock(spec=NxtEnrichmentClient)

    assert client.enrichment is client._enrichment_client


def test_data_management_public_facade_delegates_to_internal_client(mocker: object) -> None:
    """Historical Data Management facade delegates behavior to the internal client."""
    client = object.__new__(NxtApiClient)
    client._data_management_client = mocker.Mock()
    client._data_management_client.delete_devices.return_value = object()
    devices = [object()]

    value = _legacy_call(
        client.delete_devices,
        devices,
        request_id="request-id",
        uid_validation=NxtUidValidationMode.PERMISSIVE,
    )

    assert value is client._data_management_client.delete_devices.return_value
    client._data_management_client.delete_devices.assert_called_once_with(
        devices=devices,
        request_id="request-id",
        uid_validation=NxtUidValidationMode.PERMISSIVE,
    )


def test_data_management_domain_property_returns_internal_client(mocker: object) -> None:
    """New Data Management domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._data_management_client = mocker.Mock(spec=NxtDataManagementClient)

    assert client.data_management is client._data_management_client


def test_nql_public_facade_delegates_execution_to_internal_client(mocker: object) -> None:
    """Historical NQL execution facade delegates behavior to the internal client."""
    client = object.__new__(NxtApiClient)
    client._nql_client = mocker.Mock()
    client._nql_client.run_nql.return_value = object()
    request = object()

    value = _legacy_call(client.run_nql, NxtEndpoint.Nql, request, method="GET")

    assert value is client._nql_client.run_nql.return_value
    client._nql_client.run_nql.assert_called_once_with(NxtEndpoint.Nql, request, "GET")


def test_nql_domain_property_returns_internal_client(mocker: object) -> None:
    """New NQL domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._nql_client = mocker.Mock(spec=NxtNqlClient)

    assert client.nql is client._nql_client


def test_remote_actions_domain_property_returns_internal_client(mocker: object) -> None:
    """New Remote Actions domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._remote_actions_client = mocker.Mock(spec=NxtRemoteActionsClient)

    assert client.remote_actions is client._remote_actions_client


def test_campaigns_domain_property_returns_internal_client(mocker: object) -> None:
    """New Campaigns domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._campaigns_client = mocker.Mock(spec=NxtCampaignsClient)

    assert client.campaigns is client._campaigns_client


def test_workflows_domain_property_returns_internal_client(mocker: object) -> None:
    """New Workflows domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._workflows_client = mocker.Mock(spec=NxtWorkflowsClient)

    assert client.workflows is client._workflows_client


def test_spark_domain_property_returns_internal_client(mocker: object) -> None:
    """New Spark domain property exposes the domain client."""
    client = object.__new__(NxtApiClient)
    client._spark_client = mocker.Mock(spec=NxtSparkClient)

    assert client.spark is client._spark_client


def test_nql_public_facade_delegates_export_helpers_to_internal_client(mocker: object) -> None:
    """Historical NQL export helper facades delegate behavior to the internal client."""
    client = object.__new__(NxtApiClient)
    client._nql_client = mocker.Mock()
    export_response = object()
    status_response = object()

    assert _legacy_call(client.wait_status, export_response, timeout=42) is client._nql_client.wait_status.return_value
    client._nql_client.wait_status.assert_called_once_with(export_response, 42)

    assert _legacy_call(client.get_status_export, export_response) is client._nql_client.get_status_export.return_value
    client._nql_client.get_status_export.assert_called_once_with(export_response)

    assert _legacy_call(
        client.download_export,
        status_response,
        timeout=43,
    ) is client._nql_client.download_export.return_value
    client._nql_client.download_export.assert_called_once_with(status_response, 43)

    assert _legacy_call(
        client.download_export_as_df,
        status_response,
        timeout=44,
    ) is client._nql_client.download_export_as_df.return_value
    client._nql_client.download_export_as_df.assert_called_once_with(status_response, 44)
