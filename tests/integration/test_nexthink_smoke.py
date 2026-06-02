"""Optional smoke tests against a real Nexthink tenant."""

from __future__ import annotations

import os
from dataclasses import dataclass

import pytest

from nexthink_api import (
    NexthinkClient,
    NxtErrorResponse,
    NxtNqlApiExecuteRequest,
    NxtNqlApiExecuteResponse,
    NxtNqlApiExecuteV2Response,
    NxtRegionName,
    NxtRemoteAction,
    NxtRemoteActionErrorResponse,
    NxtWorkflow,
    NxtWorkflowDependency,
    NxtWorkflowErrorResponse,
    NxtWorkflowTriggerMethod,
    enable_truststore,
)

RUN_INTEGRATION_ENV = "NEXTHINK_API_RUN_INTEGRATION"
NQL_QUERY_ID_ENV = "NEXTHINK_API_INTEGRATION_NQL_QUERY_ID"

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv(RUN_INTEGRATION_ENV) != "yes",
        reason=f"Set {RUN_INTEGRATION_ENV}=yes to run real Nexthink integration tests.",
    ),
]


@dataclass(frozen=True)
class NexthinkIntegrationSettings:
    """Settings required to connect to a real Nexthink tenant."""

    tenant: str
    region: NxtRegionName
    client_id: str
    client_secret: str


def _env(*names: str) -> str | None:
    """Return the first non-empty environment value for the provided names."""
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


@pytest.fixture(scope="session")
def integration_settings() -> NexthinkIntegrationSettings:
    """Return integration settings or fail with a clear configuration message."""
    missing = []
    tenant = _env("NEXTHINK_API_TENANT", "nexthink_tenant", "nxt_instance")
    client_id = _env("NEXTHINK_API_CLIENT_ID", "client_id")
    client_secret = _env("NEXTHINK_API_CLIENT_SECRET", "client_secret")
    region = _env("NEXTHINK_API_REGION", "nexthink_region") or NxtRegionName.eu.value

    if tenant is None:
        missing.append("NEXTHINK_API_TENANT or nexthink_tenant or nxt_instance")
    if client_id is None:
        missing.append("NEXTHINK_API_CLIENT_ID or client_id")
    if client_secret is None:
        missing.append("NEXTHINK_API_CLIENT_SECRET or client_secret")
    if missing:
        pytest.fail(f"Missing integration environment variables: {', '.join(missing)}")

    return NexthinkIntegrationSettings(
        tenant=tenant,
        region=NxtRegionName(region),
        client_id=client_id,
        client_secret=client_secret,
    )


@pytest.fixture(scope="session")
def nexthink_client(integration_settings: NexthinkIntegrationSettings) -> NexthinkClient:
    """Return an authenticated Nexthink API client for integration tests."""
    enable_truststore()
    return NexthinkClient(
        integration_settings.tenant,
        integration_settings.region,
        client_id=integration_settings.client_id,
        client_secret=integration_settings.client_secret,
    )


def test_token_retrieval(nexthink_client: NexthinkClient) -> None:
    """The package can retrieve a real OAuth token."""
    assert nexthink_client.token is not None
    assert nexthink_client.token.access_token


def test_nql_read_only_query(nexthink_client: NexthinkClient) -> None:
    """The package can execute a configured read-only NQL query."""
    query_id = _env(NQL_QUERY_ID_ENV, "nexthink_integration_nql_query_id")
    if query_id is None:
        pytest.skip(f"Set {NQL_QUERY_ID_ENV} to run the NQL smoke test.")

    response = nexthink_client.nql.execute(
        NxtNqlApiExecuteRequest(queryId=query_id),
        version="v2",
    )

    assert not isinstance(response, NxtErrorResponse)
    assert isinstance(response, NxtNqlApiExecuteResponse | NxtNqlApiExecuteV2Response)
    assert isinstance(response.rows, int)
    assert isinstance(response.data, list)


def test_remote_actions_list(nexthink_client: NexthinkClient) -> None:
    """The package can list Remote Actions without executing one."""
    response = nexthink_client.remote_actions.list()

    assert not isinstance(response, NxtRemoteActionErrorResponse)
    assert isinstance(response, list)
    assert all(isinstance(remote_action, NxtRemoteAction) for remote_action in response)


def test_workflows_list(nexthink_client: NexthinkClient) -> None:
    """The package can list API-triggerable Workflows without executing one."""
    response = nexthink_client.workflows.list(
        dependency=NxtWorkflowDependency.NONE,
        trigger_method=NxtWorkflowTriggerMethod.API,
        fetch_only_active_workflows=True,
    )

    assert not isinstance(response, NxtWorkflowErrorResponse)
    assert isinstance(response, list)
    assert all(isinstance(workflow, NxtWorkflow) for workflow in response)
