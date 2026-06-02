"""Static Nexthink API operation registry."""

from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from nexthink_api.Models.nxt_endpoint import NxtEndpoint

__all__ = ["EndpointSpec", "SpecRegistry"]


@dataclass(frozen=True)
class EndpointSpec:
    """Static description of one supported API operation."""

    api: str
    operation: str
    endpoint: NxtEndpoint
    method: str
    path: str
    docs_url: str
    models_docs_url: Optional[str]
    success_statuses: tuple[int, ...]
    error_statuses: tuple[int, ...]
    response_builder: Optional[str]


class SpecRegistry:
    """Static registry for the endpoint data used by the client at runtime."""

    _SPECS: tuple[EndpointSpec, ...] = (
        EndpointSpec(
            api="Remote Actions",
            operation="executeRA",
            endpoint=NxtEndpoint.Act,
            method="POST",
            path=NxtEndpoint.Act.value,
            docs_url="https://docs.nexthink.com/api/remote-actions/remote-actions-api.md",
            models_docs_url="https://docs.nexthink.com/api/remote-actions/models.md",
            success_statuses=(HTTPStatus.OK, HTTPStatus.CREATED),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="remote_actions",
        ),
        EndpointSpec(
            api="Remote Actions",
            operation="getAllRemoteActions",
            endpoint=NxtEndpoint.RemoteActions,
            method="GET",
            path=NxtEndpoint.RemoteActions.value,
            docs_url="https://docs.nexthink.com/api/remote-actions/remote-actions-api.md",
            models_docs_url="https://docs.nexthink.com/api/remote-actions/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="remote_actions",
        ),
        EndpointSpec(
            api="Remote Actions",
            operation="getRemoteActionByNqlId",
            endpoint=NxtEndpoint.RemoteActionsDetails,
            method="GET",
            path=NxtEndpoint.RemoteActionsDetails.value,
            docs_url="https://docs.nexthink.com/api/remote-actions/remote-actions-api.md",
            models_docs_url="https://docs.nexthink.com/api/remote-actions/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND),
            response_builder="remote_actions",
        ),
        EndpointSpec(
            api="Campaigns",
            operation="triggerCampaign",
            endpoint=NxtEndpoint.Engage,
            method="POST",
            path=NxtEndpoint.Engage.value,
            docs_url="https://docs.nexthink.com/api/campaigns/trigger-a-campaign.md",
            models_docs_url="https://docs.nexthink.com/api/campaigns/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="campaigns",
        ),
        EndpointSpec(
            api="Workflows",
            operation="executeEA",
            endpoint=NxtEndpoint.Workflow,
            method="POST",
            path=NxtEndpoint.Workflow.value,
            docs_url="https://docs.nexthink.com/api/workflows/trigger-a-workflow.md",
            models_docs_url="https://docs.nexthink.com/api/workflows/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="workflows",
        ),
        EndpointSpec(
            api="Workflows",
            operation="executeEAWithExternalIds",
            endpoint=NxtEndpoint.WorkflowV2,
            method="POST",
            path=NxtEndpoint.WorkflowV2.value,
            docs_url="https://docs.nexthink.com/api/workflows/trigger-a-workflow-v2.md",
            models_docs_url="https://docs.nexthink.com/api/workflows/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="workflows",
        ),
        EndpointSpec(
            api="Workflows",
            operation="triggerThinklet",
            endpoint=NxtEndpoint.WorkflowThinkletTrigger,
            method="POST",
            path=f"{NxtEndpoint.WorkflowThinkletTrigger.value}/{{workflowUuid}}/execution/{{executionUuid}}/trigger",
            docs_url="https://docs.nexthink.com/api/workflows/trigger-wait-for-event.md",
            models_docs_url="https://docs.nexthink.com/api/workflows/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="workflows",
        ),
        EndpointSpec(
            api="Workflows",
            operation="getAllWorkflows",
            endpoint=NxtEndpoint.Workflows,
            method="GET",
            path=NxtEndpoint.Workflows.value,
            docs_url="https://docs.nexthink.com/api/workflows/list-workflows.md",
            models_docs_url="https://docs.nexthink.com/api/workflows/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="workflows",
        ),
        EndpointSpec(
            api="Workflows",
            operation="getWorkflow",
            endpoint=NxtEndpoint.WorkflowDetails,
            method="GET",
            path=NxtEndpoint.WorkflowDetails.value,
            docs_url="https://docs.nexthink.com/api/workflows/get-workflow.md",
            models_docs_url="https://docs.nexthink.com/api/workflows/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="workflows",
        ),
        EndpointSpec(
            api="Spark",
            operation="handleHandoffRequest",
            endpoint=NxtEndpoint.SparkHandoff,
            method="POST",
            path=NxtEndpoint.SparkHandoff.value,
            docs_url="https://docs.nexthink.com/api/spark/handoff-api.md",
            models_docs_url="https://docs.nexthink.com/api/spark/models.md",
            success_statuses=(HTTPStatus.OK, HTTPStatus.NO_CONTENT),
            error_statuses=(
                HTTPStatus.BAD_REQUEST,
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ),
            response_builder="spark",
        ),
        EndpointSpec(
            api="Data management",
            operation="deleteDevices",
            endpoint=NxtEndpoint.DataManagement,
            method="POST",
            path=NxtEndpoint.DataManagement.value,
            docs_url="https://docs.nexthink.com/api/data-management/schedule-device-deletions.md",
            models_docs_url="https://docs.nexthink.com/api/data-management/models.md",
            success_statuses=(HTTPStatus.ACCEPTED,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="data_management",
        ),
        EndpointSpec(
            api="Enrichment",
            operation="enrichmentDataFields",
            endpoint=NxtEndpoint.Enrichment,
            method="POST",
            path=NxtEndpoint.Enrichment.value,
            docs_url="https://docs.nexthink.com/api/enrichment/enrich-fields-for-given-objects.md",
            models_docs_url="https://docs.nexthink.com/api/enrichment/models.md",
            success_statuses=(HTTPStatus.OK, HTTPStatus.MULTI_STATUS),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN),
            response_builder="enrichment",
        ),
        EndpointSpec(
            api="NQL",
            operation="execute",
            endpoint=NxtEndpoint.Nql,
            method="POST",
            path=NxtEndpoint.Nql.value,
            docs_url="https://docs.nexthink.com/api/nql/execute-an-nql.md",
            models_docs_url="https://docs.nexthink.com/api/nql/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ),
            response_builder="nql",
        ),
        EndpointSpec(
            api="NQL",
            operation="executeV2",
            endpoint=NxtEndpoint.NqlV2,
            method="POST",
            path=NxtEndpoint.NqlV2.value,
            docs_url="https://docs.nexthink.com/api/nql/execute-an-nql.md",
            models_docs_url="https://docs.nexthink.com/api/nql/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ),
            response_builder="nql",
        ),
        EndpointSpec(
            api="NQL",
            operation="export",
            endpoint=NxtEndpoint.NqlExport,
            method="POST",
            path=NxtEndpoint.NqlExport.value,
            docs_url="https://docs.nexthink.com/api/nql/export-an-nql.md",
            models_docs_url="https://docs.nexthink.com/api/nql/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ),
            response_builder="nql",
        ),
        EndpointSpec(
            api="NQL",
            operation="export",
            endpoint=NxtEndpoint.NqlExport,
            method="GET",
            path=NxtEndpoint.NqlExport.value,
            docs_url="https://docs.nexthink.com/api/nql/export-an-nql.md",
            models_docs_url="https://docs.nexthink.com/api/nql/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ),
            response_builder="nql",
        ),
        EndpointSpec(
            api="NQL",
            operation="status",
            endpoint=NxtEndpoint.NqlStatus,
            method="GET",
            path=f"{NxtEndpoint.NqlStatus.value}/{{exportId}}",
            docs_url="https://docs.nexthink.com/api/nql/export-an-nql.md",
            models_docs_url="https://docs.nexthink.com/api/nql/models.md",
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(
                HTTPStatus.UNAUTHORIZED,
                HTTPStatus.FORBIDDEN,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ),
            response_builder="nql",
        ),
        EndpointSpec(
            api="Authentication",
            operation="getToken",
            endpoint=NxtEndpoint.Token,
            method="POST",
            path="/oauth2/default/v1/token",
            docs_url="https://docs.nexthink.com/api/getting-authentication-token.md",
            models_docs_url=None,
            success_statuses=(HTTPStatus.OK,),
            error_statuses=(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED),
            response_builder="token",
        ),
    )

    @classmethod
    def all(cls) -> tuple[EndpointSpec, ...]:
        """Return every registered endpoint operation."""
        return cls._SPECS

    @classmethod
    def find(cls, endpoint: NxtEndpoint, method: str) -> EndpointSpec | None:
        """Return the registry entry for an endpoint and method when supported."""
        method = method.upper()
        return next(
            (spec for spec in cls._SPECS if spec.endpoint == endpoint and spec.method == method),
            None,
        )

    @classmethod
    def supports_method(cls, endpoint: NxtEndpoint, method: str) -> bool:
        """Return whether an endpoint supports an HTTP method."""
        return cls.find(endpoint, method) is not None
