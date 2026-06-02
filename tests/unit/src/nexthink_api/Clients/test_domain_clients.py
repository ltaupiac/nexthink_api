"""Unit tests for internal domain client shells."""

import nexthink_api
from nexthink_api.Clients.nxt_campaigns_client import NxtCampaignsClient
from nexthink_api.Clients.nxt_data_management_client import NxtDataManagementClient
from nexthink_api.Clients.nxt_enrichment_client import NxtEnrichmentClient
from nexthink_api.Clients.nxt_nql_client import NxtNqlClient
from nexthink_api.Clients.nxt_remote_actions_client import NxtRemoteActionsClient
from nexthink_api.Clients.nxt_spark_client import NxtSparkClient
from nexthink_api.Clients.nxt_workflows_client import NxtWorkflowsClient


def test_internal_domain_clients_keep_facade_reference() -> None:
    """Domain clients are internal delegates around the existing facade."""
    facade = object()

    assert NxtDataManagementClient(facade)._api_client is facade
    assert NxtCampaignsClient(facade)._api_client is facade
    assert NxtEnrichmentClient(facade)._api_client is facade
    assert NxtNqlClient(facade)._api_client is facade
    assert NxtRemoteActionsClient(facade)._api_client is facade
    assert NxtSparkClient(facade)._api_client is facade
    assert NxtWorkflowsClient(facade)._api_client is facade


def test_domain_clients_are_not_exported_from_root_package() -> None:
    """Domain clients are not public root exports during this phase."""
    assert not hasattr(nexthink_api, "NxtDataManagementClient")
    assert not hasattr(nexthink_api, "NxtCampaignsClient")
    assert not hasattr(nexthink_api, "NxtEnrichmentClient")
    assert not hasattr(nexthink_api, "NxtNqlClient")
    assert not hasattr(nexthink_api, "NxtRemoteActionsClient")
    assert not hasattr(nexthink_api, "NxtSparkClient")
    assert not hasattr(nexthink_api, "NxtWorkflowsClient")
