"""Tests for the public NexthinkClient API."""

import inspect

import pytest

from nexthink_api import (
    NexthinkClient,
    NxtApiClient,
    NxtEndpoint,
    NxtLegacyApiWarning,
    NxtRegionName,
    NxtUidValidationMode,
)
from nexthink_api.Clients import NexthinkClient as ClientsNexthinkClient
from nexthink_api.Clients.nxt_campaigns_client import NxtCampaignsClient
from nexthink_api.Clients.nxt_data_management_client import NxtDataManagementClient
from nexthink_api.Clients.nxt_enrichment_client import NxtEnrichmentClient
from nexthink_api.Clients.nxt_nql_client import NxtNqlClient
from nexthink_api.Clients.nxt_remote_actions_client import NxtRemoteActionsClient
from nexthink_api.Clients.nxt_spark_client import NxtSparkClient
from nexthink_api.Clients.nxt_workflows_client import NxtWorkflowsClient


def _client(mocker: object) -> NexthinkClient:
    """Return a NexthinkClient without performing token retrieval."""
    mocker.patch.object(NexthinkClient, "init_token", return_value=None)
    return NexthinkClient(
        "tenant",
        NxtRegionName.eu,
        client_id="client-id",
        client_secret="client-secret",
    )


def test_nexthink_client_is_public_root_client() -> None:
    """NexthinkClient is exported as the new public root client."""
    assert ClientsNexthinkClient is NexthinkClient
    assert issubclass(NexthinkClient, NxtApiClient)


def test_nexthink_client_initializes_domain_clients(mocker: object) -> None:
    """Root client initializes every supported domain client."""
    client = _client(mocker)

    assert isinstance(client.enrichment, NxtEnrichmentClient)
    assert isinstance(client.nql, NxtNqlClient)
    assert isinstance(client.data_management, NxtDataManagementClient)
    assert isinstance(client.remote_actions, NxtRemoteActionsClient)
    assert isinstance(client.campaigns, NxtCampaignsClient)
    assert isinstance(client.workflows, NxtWorkflowsClient)
    assert isinstance(client.spark, NxtSparkClient)


def test_domain_methods_do_not_require_endpoint_parameters(mocker: object) -> None:
    """Common domain methods own their endpoints."""
    client = _client(mocker)
    methods = [
        client.enrichment.run,
        client.nql.execute,
        client.nql.export,
        client.data_management.delete_devices,
        client.remote_actions.execute,
        client.campaigns.trigger,
        client.workflows.execute,
        client.spark.handoff,
    ]

    for method in methods:
        assert "endpoint" not in inspect.signature(method).parameters


def test_enrichment_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes Enrichment through its domain property."""
    client = _client(mocker)
    client._enrichment_client = mocker.Mock(spec=NxtEnrichmentClient)
    request = object()

    value = client.enrichment.run(request)

    assert value is client._enrichment_client.run.return_value
    client._enrichment_client.run.assert_called_once_with(request)


def test_nql_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes NQL through its domain property."""
    client = _client(mocker)
    client._nql_client = mocker.Mock(spec=NxtNqlClient)
    request = object()

    execute = client.nql.execute(request, version="v2")
    export = client.nql.export(request)

    assert execute is client._nql_client.execute.return_value
    assert export is client._nql_client.export.return_value
    client._nql_client.execute.assert_called_once_with(request, version="v2")
    client._nql_client.export.assert_called_once_with(request)


def test_data_management_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes Data Management through its domain property."""
    client = _client(mocker)
    client._data_management_client = mocker.Mock(spec=NxtDataManagementClient)
    devices = [object()]

    value = client.data_management.delete_devices(
        devices=devices,
        request_id="request-id",
        uid_validation=NxtUidValidationMode.PERMISSIVE,
    )

    assert value is client._data_management_client.delete_devices.return_value
    client._data_management_client.delete_devices.assert_called_once_with(
        devices=devices,
        request_id="request-id",
        uid_validation=NxtUidValidationMode.PERMISSIVE,
    )


def test_remote_actions_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes Remote Actions through its domain property."""
    client = _client(mocker)
    client._remote_actions_client = mocker.Mock(spec=NxtRemoteActionsClient)
    request = object()

    execute = client.remote_actions.execute(request)
    remote_actions = client.remote_actions.list()
    detail = client.remote_actions.get("#restart_service")

    assert execute is client._remote_actions_client.execute.return_value
    assert remote_actions is client._remote_actions_client.list.return_value
    assert detail is client._remote_actions_client.get.return_value
    client._remote_actions_client.execute.assert_called_once_with(request)
    client._remote_actions_client.list.assert_called_once_with()
    client._remote_actions_client.get.assert_called_once_with("#restart_service")


def test_campaigns_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes Campaigns through its domain property."""
    client = _client(mocker)
    client._campaigns_client = mocker.Mock(spec=NxtCampaignsClient)
    request = object()

    value = client.campaigns.trigger(request)

    assert value is client._campaigns_client.trigger.return_value
    client._campaigns_client.trigger.assert_called_once_with(request)


def test_workflows_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes Workflows through its domain property."""
    client = _client(mocker)
    client._workflows_client = mocker.Mock(spec=NxtWorkflowsClient)
    request = object()
    dependency = object()
    trigger_method = object()

    execute = client.workflows.execute(request, source="source")
    execute_v2 = client.workflows.execute_with_external_ids(request, source="source")
    thinklet = client.workflows.trigger_thinklet(
        "workflow-uuid",
        "execution-uuid",
        request,
        source="source",
    )
    workflows = client.workflows.list(
        dependency=dependency,
        trigger_method=trigger_method,
        fetch_only_active_workflows=True,
        source="source",
    )
    detail = client.workflows.get("#workflow", source="source")

    assert execute is client._workflows_client.execute.return_value
    assert execute_v2 is client._workflows_client.execute_with_external_ids.return_value
    assert thinklet is client._workflows_client.trigger_thinklet.return_value
    assert workflows is client._workflows_client.list.return_value
    assert detail is client._workflows_client.get.return_value
    client._workflows_client.execute.assert_called_once_with(request, source="source")
    client._workflows_client.execute_with_external_ids.assert_called_once_with(request, source="source")
    client._workflows_client.trigger_thinklet.assert_called_once_with(
        "workflow-uuid",
        "execution-uuid",
        request,
        source="source",
    )
    client._workflows_client.list.assert_called_once_with(
        dependency=dependency,
        trigger_method=trigger_method,
        fetch_only_active_workflows=True,
        source="source",
    )
    client._workflows_client.get.assert_called_once_with("#workflow", source="source")


def test_spark_works_through_nexthink_client_public_api(mocker: object) -> None:
    """Public root client routes Spark through its domain property."""
    client = _client(mocker)
    client._spark_client = mocker.Mock(spec=NxtSparkClient)
    request = object()

    value = client.spark.handoff(
        request,
        user_principal_name="user@example.com",
        timezone="Europe/Paris",
    )

    assert value is client._spark_client.handoff.return_value
    client._spark_client.handoff.assert_called_once_with(
        request,
        user_principal_name="user@example.com",
        timezone="Europe/Paris",
    )


def test_legacy_facade_methods_remain_available_and_delegate(mocker: object) -> None:
    """Historical facade methods remain available while NexthinkClient is introduced."""
    client = object.__new__(NexthinkClient)
    client._enrichment_client = mocker.Mock()
    request = object()

    with pytest.warns(NxtLegacyApiWarning, match="run_enrichment"):
        value = client.run_enrichment(NxtEndpoint.Enrichment, request)

    assert value is client._enrichment_client.run_enrichment.return_value
    client._enrichment_client.run_enrichment.assert_called_once_with(NxtEndpoint.Enrichment, request)


def test_nexthink_client_method_checks_use_spec_registry(mocker: object) -> None:
    """Method validation does not depend on runtime YAML parsing."""
    client = object.__new__(NexthinkClient)
    supports_method = mocker.patch(
        "nexthink_api.Clients.nxt_api_client.SpecRegistry.supports_method",
        return_value=True,
    )

    assert client.check_method(NxtEndpoint.Nql, "POST") is True
    supports_method.assert_called_once_with(NxtEndpoint.Nql, "POST")
