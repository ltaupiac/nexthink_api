"""Internal Workflows domain client."""

from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.Clients.nxt_response import NxtResponse, WorkflowResponseType
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Workflows.nxt_workflow_execution_request import NxtWorkflowExecutionRequest
from nexthink_api.Workflows.nxt_workflow_external_ids_execution_request import NxtWorkflowExternalIdsExecutionRequest
from nexthink_api.Workflows.nxt_workflow_models import NxtWorkflowDependency, NxtWorkflowTriggerMethod
from nexthink_api.Workflows.nxt_workflow_thinklet_trigger_request import NxtWorkflowThinkletTriggerRequest

__all__ = ["NxtWorkflowsClient"]


class NxtWorkflowsClient:
    """Internal delegate for Workflows behavior."""

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal Workflows client."""
        self._api_client = api_client

    def execute(self, data: NxtWorkflowExecutionRequest, source: str | None = None) -> WorkflowResponseType:
        """Execute a workflow with collector UUIDs or user SIDs."""
        endpoint = NxtEndpoint.Workflow
        return self._post_json(endpoint, data.model_dump(exclude_none=True), source=source)

    def execute_with_external_ids(
            self,
            data: NxtWorkflowExternalIdsExecutionRequest,
            source: str | None = None,
    ) -> WorkflowResponseType:
        """Execute a workflow with external device or user identifiers."""
        endpoint = NxtEndpoint.WorkflowV2
        return self._post_json(endpoint, data.model_dump(exclude_none=True), source=source)

    def trigger_thinklet(
            self,
            workflow_uuid: str,
            execution_uuid: str,
            data: NxtWorkflowThinkletTriggerRequest | None = None,
            source: str | None = None,
    ) -> WorkflowResponseType:
        """Trigger a waiting workflow execution."""
        endpoint = NxtEndpoint.WorkflowThinkletTrigger
        path = f"{endpoint.value}/{workflow_uuid}/execution/{execution_uuid}/trigger"
        payload = data or NxtWorkflowThinkletTriggerRequest()
        return self._post_json(endpoint, payload.model_dump(exclude_none=True), path=path, source=source)

    def list(
            self,
            dependency: NxtWorkflowDependency,
            trigger_method: NxtWorkflowTriggerMethod,
            fetch_only_active_workflows: bool | None = None,
            source: str | None = None,
    ) -> WorkflowResponseType:
        """Return workflow configuration metadata."""
        endpoint = NxtEndpoint.Workflows
        if not self._api_client.check_method(endpoint, "GET"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        params: dict[str, str | bool] = {
            "dependency": dependency.value,
            "triggerMethod": trigger_method.value,
        }
        if fetch_only_active_workflows is not None:
            params["fetchOnlyActiveWorkflows"] = fetch_only_active_workflows
        response = self._api_client.transport.get(
            endpoint.value,
            headers=self._headers(source),
            params=params,
        )
        return NxtResponse().from_response(response=response)

    def get(self, nql_id: str, source: str | None = None) -> WorkflowResponseType:
        """Return one workflow configuration by NQL ID."""
        endpoint = NxtEndpoint.WorkflowDetails
        if not self._api_client.check_method(endpoint, "GET"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.get(
            endpoint.value,
            headers=self._headers(source),
            params={"nqlId": nql_id},
        )
        return NxtResponse().from_response(response=response)

    def _post_json(
            self,
            endpoint: NxtEndpoint,
            payload: dict,
            path: str | None = None,
            source: str | None = None,
    ) -> WorkflowResponseType:
        """POST JSON to a Workflows endpoint and parse the response."""
        if not self._api_client.check_method(endpoint, "POST"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.post(
            path or endpoint.value,
            headers=self._headers(source),
            json=payload,
        )
        return NxtResponse().from_response(response=response)

    def _headers(self, source: str | None) -> dict:
        """Return request headers with optional Workflows Source metadata."""
        headers = dict(self._api_client.headers)
        if source is not None:
            headers["Source"] = source
        return headers
