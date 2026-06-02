"""Domain response builders for Nexthink API responses."""

from http import HTTPStatus
from typing import TypeAlias, Union
from urllib.parse import urlparse

from requests.models import Response

from nexthink_api.Campaigns.nxt_campaign_trigger_error_response import NxtCampaignTriggerErrorResponse
from nexthink_api.Campaigns.nxt_campaign_trigger_success_response import NxtCampaignTriggerSuccessResponse
from nexthink_api.DataManagement.nxt_data_management_error_response import NxtDataManagementErrorResponse
from nexthink_api.DataManagement.nxt_device_deletion_response import NxtDeviceDeletionResponse
from nexthink_api.Enrichment.nxt_bad_request_response import NxtBadRequestResponse
from nexthink_api.Enrichment.nxt_forbidden_response import NxtForbiddenResponse
from nexthink_api.Enrichment.nxt_partial_success_response import NxtPartialSuccessResponse
from nexthink_api.Enrichment.nxt_success_response import NxtSuccessResponse
from nexthink_api.Exceptions.nxt_api_exception import NxtApiException
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Models.nxt_invalid_token_request import NxtInvalidTokenRequest
from nexthink_api.Models.nxt_token_response import NxtTokenResponse
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse
from nexthink_api.Nql.nxt_nql_api_execute_response import NxtNqlApiExecuteResponse
from nexthink_api.Nql.nxt_nql_api_execute_v2_response import NxtNqlApiExecuteV2Response
from nexthink_api.Nql.nxt_nql_api_export_response import NxtNqlApiExportResponse
from nexthink_api.Nql.nxt_nql_api_status_response import NxtNqlApiStatusResponse
from nexthink_api.RemoteActions.nxt_remote_action_error_response import NxtRemoteActionErrorResponse
from nexthink_api.RemoteActions.nxt_remote_action_execution_response import NxtRemoteActionExecutionResponse
from nexthink_api.RemoteActions.nxt_remote_action_models import NxtRemoteAction
from nexthink_api.Spark.nxt_spark_error_response import NxtSparkErrorResponse
from nexthink_api.Spark.nxt_spark_handoff_success_response import NxtSparkHandoffSuccessResponse
from nexthink_api.Workflows.nxt_workflow_error_response import NxtWorkflowErrorResponse
from nexthink_api.Workflows.nxt_workflow_execution_response import NxtWorkflowExecutionResponse
from nexthink_api.Workflows.nxt_workflow_models import NxtWorkflow
from nexthink_api.Workflows.nxt_workflow_thinklet_trigger_response import NxtWorkflowThinkletTriggerResponse

__all__ = [
    "ActResponseType",
    "CampaignResponseType",
    "CampaignsResponseBuilder",
    "DataManagementResponseBuilder",
    "DataManagementResponseType",
    "EnrichmentResponseBuilder",
    "EnrichmentResponseType",
    "NqlResponseBuilder",
    "NqlResponseType",
    "RemoteActionsResponseBuilder",
    "RemoteActionsResponseType",
    "ResponseApiType",
    "SparkResponseBuilder",
    "SparkResponseType",
    "TokenResponseBuilder",
    "WorkflowResponseType",
    "WorkflowsResponseBuilder",
]

EnrichmentResponseType: TypeAlias = Union[
    NxtSuccessResponse,
    NxtPartialSuccessResponse,
    NxtBadRequestResponse,
    NxtInvalidTokenRequest,
    NxtForbiddenResponse,
]

RemoteActionsResponseType: TypeAlias = Union[
    NxtRemoteActionExecutionResponse,
    NxtRemoteActionErrorResponse,
    NxtInvalidTokenRequest,
    NxtRemoteAction,
    list[NxtRemoteAction],
]

# Backward-compatible alias for the historical Act name.
ActResponseType: TypeAlias = RemoteActionsResponseType

NqlResponseType: TypeAlias = Union[
    NxtNqlApiExecuteResponse,
    NxtNqlApiExecuteV2Response,
    NxtNqlApiExportResponse,
    NxtNqlApiStatusResponse,
    NxtErrorResponse,
    NxtInvalidTokenRequest,
]

CampaignResponseType: TypeAlias = Union[
    NxtCampaignTriggerSuccessResponse,
    NxtCampaignTriggerErrorResponse,
    NxtInvalidTokenRequest,
]

WorkflowResponseType: TypeAlias = Union[
    NxtWorkflowExecutionResponse,
    NxtWorkflowErrorResponse,
    NxtInvalidTokenRequest,
    NxtWorkflow,
    list[NxtWorkflow],
    list[NxtWorkflowThinkletTriggerResponse],
]

SparkResponseType: TypeAlias = Union[
    NxtSparkHandoffSuccessResponse,
    NxtSparkErrorResponse,
    NxtInvalidTokenRequest,
]

DataManagementResponseType: TypeAlias = Union[
    NxtDeviceDeletionResponse,
    NxtDataManagementErrorResponse,
    NxtInvalidTokenRequest,
]

ResponseApiType: TypeAlias = Union[
    NxtTokenResponse,
    EnrichmentResponseType,
    ActResponseType,
    NqlResponseType,
    CampaignResponseType,
    WorkflowResponseType,
    SparkResponseType,
    DataManagementResponseType,
]


def get_json_or_raise(response: Response, api_name: str, extra_context: str | None = None) -> dict | list:
    """Return JSON payload or raise a useful API exception."""
    try:
        return response.json()
    except ValueError as error:
        body = response.text[:500] if response.text else "<empty body>"
        context = f", {extra_context}" if extra_context else ""
        raise NxtApiException(
            f"{api_name} response body is not valid JSON. "
            f"status_code={response.status_code}{context}, body={body!r}"
        ) from error


class EnrichmentResponseBuilder:
    """Build Enrichment API responses."""

    def build(self, response: Response) -> EnrichmentResponseType:
        """Create Enrichment response based on the provided response object."""
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            return NxtSuccessResponse()
        if status_code == HTTPStatus.MULTI_STATUS:
            data = self.get_json(response)
            return NxtPartialSuccessResponse.model_validate(data)
        if status_code == HTTPStatus.BAD_REQUEST:
            data = self.get_json(response)
            return NxtBadRequestResponse(errors=data["errors"])
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        if status_code == HTTPStatus.FORBIDDEN:
            return NxtForbiddenResponse(message=response.reason)
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def get_json(response: Response) -> dict | list:
        """Return Enrichment JSON payload or raise a useful API exception."""
        return get_json_or_raise(response, "Enrichment")


class RemoteActionsResponseBuilder:
    """Build Remote Actions API responses."""

    def build(self, response: Response) -> RemoteActionsResponseType:
        """Create Remote Actions response based on the provided response object."""
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            url = urlparse(response.url)
            api = NxtEndpoint.get_api_name(url.path)
            data = self.get_json(response)
            if api == NxtEndpoint.Act.name:
                return NxtRemoteActionExecutionResponse.model_validate(data)
            if api == NxtEndpoint.RemoteActions.name:
                return [NxtRemoteAction.model_validate(item) for item in data]
            if api == NxtEndpoint.RemoteActionsDetails.name:
                return NxtRemoteAction.model_validate(data)
            raise NxtApiException(f"Can't find API for {url.path}")
        if status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
        }:
            return NxtRemoteActionErrorResponse.model_validate(self.get_json(response))
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def get_json(response: Response) -> dict | list:
        """Return Remote Actions JSON payload or raise a useful API exception."""
        return get_json_or_raise(response, "Remote Actions")


class WorkflowsResponseBuilder:
    """Build Workflows API responses."""

    def build(self, response: Response) -> WorkflowResponseType:
        """Create Workflows response based on the provided response object."""
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            url = urlparse(response.url)
            api = NxtEndpoint.get_api_name(url.path)
            return self.build_success_response(api, self.get_json(response), url.path)
        if status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.FORBIDDEN,
        }:
            return NxtWorkflowErrorResponse.model_validate(self.get_json(response))
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def build_success_response(api: str | None, data: dict | list, path: str) -> WorkflowResponseType:
        """Build a Workflows success response for the resolved endpoint."""
        if api in {NxtEndpoint.Workflow.name, NxtEndpoint.WorkflowV2.name}:
            return NxtWorkflowExecutionResponse.model_validate(data)
        if api == NxtEndpoint.WorkflowThinkletTrigger.name:
            return [NxtWorkflowThinkletTriggerResponse.model_validate(item) for item in data]
        if api == NxtEndpoint.Workflows.name:
            return [NxtWorkflow.model_validate(item) for item in data]
        if api == NxtEndpoint.WorkflowDetails.name:
            if isinstance(data, list):
                return [NxtWorkflow.model_validate(item) for item in data]
            return NxtWorkflow.model_validate(data)
        raise NxtApiException(f"Can't find API for {path}")

    @staticmethod
    def get_json(response: Response) -> dict | list:
        """Return Workflows JSON payload or raise a useful API exception."""
        return get_json_or_raise(response, "Workflows")


class DataManagementResponseBuilder:
    """Build Data Management API responses."""

    def build(self, response: Response) -> DataManagementResponseType:
        """Create Data Management response based on the provided response object."""
        status_code = response.status_code
        request_id = getattr(response, "headers", {}).get("x-request-id")
        if status_code == HTTPStatus.ACCEPTED:
            data = self.get_json(response, request_id)
            return NxtDeviceDeletionResponse.model_validate(data)
        if status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        }:
            data = self.get_json(response, request_id)
            return NxtDataManagementErrorResponse.model_validate(data)
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def get_json(response: Response, request_id: str | None) -> dict:
        """Return Data Management JSON payload enriched with the response request id."""
        data = get_json_or_raise(response, "Data Management", f"request_id={request_id}")
        return data | {"request_id": request_id}


class SparkResponseBuilder:
    """Build Spark API responses."""

    def build(self, response: Response) -> SparkResponseType:
        """Create Spark response based on the provided response object."""
        status_code = response.status_code
        if status_code in {HTTPStatus.OK, HTTPStatus.NO_CONTENT}:
            return NxtSparkHandoffSuccessResponse()
        if status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
        }:
            return NxtSparkErrorResponse.model_validate(self.get_error_json(response))
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def get_error_json(response: Response) -> dict:
        """Return Spark error JSON or synthesize a useful error payload."""
        try:
            return response.json()
        except ValueError:
            message = response.text[:500] if response.text else response.reason
            return {"message": message or f"HTTP {response.status_code}"}


class CampaignsResponseBuilder:
    """Build Campaigns API responses."""

    def build(self, response: Response) -> CampaignResponseType:
        """Create Campaigns response based on the provided response object."""
        status_code = response.status_code
        if status_code in {HTTPStatus.OK, HTTPStatus.CREATED}:
            return NxtCampaignTriggerSuccessResponse.model_validate(self.get_json(response))
        if status_code in {
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.FORBIDDEN,
        }:
            return NxtCampaignTriggerErrorResponse.model_validate(self.get_json(response))
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def get_json(response: Response) -> dict:
        """Return Campaigns JSON payload or raise a useful API exception."""
        return get_json_or_raise(response, "Campaigns")


class NqlResponseBuilder:
    """Build NQL API responses."""

    def build(self, response: Response) -> NqlResponseType:
        """Create NQL response based on the provided response object."""
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            url = urlparse(response.url)
            api = NxtEndpoint.get_api_name(url.path)
            data = self.get_json(response)
            success_models = {
                NxtEndpoint.Nql.name: NxtNqlApiExecuteResponse,
                NxtEndpoint.NqlV2.name: NxtNqlApiExecuteV2Response,
                NxtEndpoint.NqlExport.name: NxtNqlApiExportResponse,
                NxtEndpoint.NqlStatus.name: NxtNqlApiStatusResponse,
            }
            if api in success_models:
                return success_models[api].model_validate(data)
            return NxtErrorResponse(message=f"Can't find API for {url.path}", code=HTTPStatus.IM_A_TEAPOT)
        if status_code == HTTPStatus.UNAUTHORIZED:
            return NxtInvalidTokenRequest()
        if status_code in {
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
            HTTPStatus.NOT_ACCEPTABLE,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.SERVICE_UNAVAILABLE,
        }:
            return NxtErrorResponse(message=response.reason, code=status_code)
        raise NxtApiException(f"Unknown status response code: {status_code}")

    @staticmethod
    def get_json(response: Response) -> dict | list:
        """Return NQL JSON payload or raise a useful API exception."""
        return get_json_or_raise(response, "NQL")


class TokenResponseBuilder:
    """Build token API responses."""

    def build(self, response: Response) -> NxtTokenResponse:
        """Create a Token response based on the provided response object."""
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            return NxtTokenResponse.model_validate(get_json_or_raise(response, "Token"))
        raise NxtApiException(f"Unknown status response code: {status_code}")
