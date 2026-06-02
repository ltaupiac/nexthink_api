"""Nexthink API response router."""

from urllib.parse import urlparse

from requests.models import Response
from pydantic import BaseModel, Field, ConfigDict

from nexthink_api.Exceptions.nxt_api_exception import NxtApiException
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Models.nxt_token_response import NxtTokenResponse
from nexthink_api.Clients.nxt_response_builders import (
    ActResponseType,
    CampaignResponseType,
    CampaignsResponseBuilder,
    DataManagementResponseBuilder,
    DataManagementResponseType,
    EnrichmentResponseBuilder,
    EnrichmentResponseType,
    NqlResponseBuilder,
    NqlResponseType,
    RemoteActionsResponseBuilder,
    RemoteActionsResponseType,
    ResponseApiType,
    SparkResponseBuilder,
    SparkResponseType,
    TokenResponseBuilder,
    WorkflowResponseType,
    WorkflowsResponseBuilder,
)


__all__ = [
    'NxtResponse',
    'ResponseApiType',
    'EnrichmentResponseType',
    'ActResponseType',
    'RemoteActionsResponseType',
    'NqlResponseType',
    'CampaignResponseType',
    'WorkflowResponseType',
    'SparkResponseType',
    'DataManagementResponseType',
]


class NxtResponse(BaseModel):
    """Build different types of Nexthink API responses based on the provided Response object.

    Parameters
    ----------
        response : Response
            The response object to build the response from.

    Returns
    -------
        ResponseType

    Raises
    ------
        NxtApiException
            If the status code is not one of the expected values.

    """

    response: ResponseApiType = Field(alias='value', default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    @property
    def value(self) -> ResponseApiType:
        """Returns the value of the 'response' attribute."""
        return self.response

    def from_response(self, response: Response) -> ResponseApiType:
        """Build a Nexthink API response based on the provided Response object.

        Parameters
        ----------
            response : Response
                The response object to build the response from.

        Returns
        -------
            ResponseAPIType
                The built response.

        Raises
        ------
            NxtApiException
                If the status code is not one of the expected values.

        """
        endpoint = urlparse(response.url).path
        api = NxtEndpoint.get_api_name(endpoint)
        response_builders = {
            NxtEndpoint.Enrichment.name: self.build_nxt_enrichment_response,
            NxtEndpoint.Act.name: self.build_nxt_act_response,
            NxtEndpoint.RemoteActions.name: self.build_nxt_act_response,
            NxtEndpoint.RemoteActionsDetails.name: self.build_nxt_act_response,
            NxtEndpoint.Engage.name: self.build_nxt_engage_response,
            NxtEndpoint.Workflow.name: self.build_nxt_workflow_response,
            NxtEndpoint.WorkflowV2.name: self.build_nxt_workflow_response,
            NxtEndpoint.WorkflowThinkletTrigger.name: self.build_nxt_workflow_response,
            NxtEndpoint.WorkflowDetails.name: self.build_nxt_workflow_response,
            NxtEndpoint.Workflows.name: self.build_nxt_workflow_response,
            NxtEndpoint.SparkHandoff.name: self.build_nxt_spark_response,
            NxtEndpoint.DataManagement.name: self.build_nxt_data_management_response,
            NxtEndpoint.Nql.name: self.build_nxt_nql_response,
            NxtEndpoint.NqlV2.name: self.build_nxt_nql_response,
            NxtEndpoint.NqlExport.name: self.build_nxt_nql_response,
            NxtEndpoint.NqlStatus.name: self.build_nxt_nql_response,
            NxtEndpoint.Token.name: self.build_nxt_token_response,
        }
        if api in response_builders:
            return response_builders[api](response)
        raise NxtApiException(f"Can't create response for the API: '{api}'")

    def build_nxt_enrichment_response(self, response: Response) -> EnrichmentResponseType:
        """Build an Enrichment response through the domain builder."""
        return EnrichmentResponseBuilder().build(response)

    def build_nxt_act_response(self, response: Response) -> RemoteActionsResponseType:
        """Build a Remote Actions response through the domain builder."""
        return RemoteActionsResponseBuilder().build(response)

    @staticmethod
    def get_remote_actions_json(response: Response) -> dict | list:
        """Return Remote Actions JSON through the domain builder."""
        return RemoteActionsResponseBuilder.get_json(response)

    def build_nxt_workflow_response(self, response: Response) -> WorkflowResponseType:
        """Build a Workflows response through the domain builder."""
        return WorkflowsResponseBuilder().build(response)

    @staticmethod
    def build_nxt_workflow_success_response(api: str | None, data: dict | list, path: str) -> WorkflowResponseType:
        """Build a Workflows success response through the domain builder."""
        return WorkflowsResponseBuilder.build_success_response(api, data, path)

    @staticmethod
    def get_workflows_json(response: Response) -> dict | list:
        """Return Workflows JSON through the domain builder."""
        return WorkflowsResponseBuilder.get_json(response)

    def build_nxt_data_management_response(self, response: Response) -> DataManagementResponseType:
        """Build a Data Management response through the domain builder."""
        return DataManagementResponseBuilder().build(response)

    def build_nxt_spark_response(self, response: Response) -> SparkResponseType:
        """Build a Spark response through the domain builder."""
        return SparkResponseBuilder().build(response)

    @staticmethod
    def get_spark_error_json(response: Response) -> dict:
        """Return Spark error JSON through the domain builder."""
        return SparkResponseBuilder.get_error_json(response)

    @staticmethod
    def get_data_management_json(response: Response, request_id: str | None) -> dict:
        """Return Data Management JSON through the domain builder."""
        return DataManagementResponseBuilder.get_json(response, request_id)

    def build_nxt_engage_response(self, response: Response) -> CampaignResponseType:
        """Build a Campaigns response through the domain builder."""
        return CampaignsResponseBuilder().build(response)

    @staticmethod
    def get_campaigns_json(response: Response) -> dict:
        """Return Campaigns JSON through the domain builder."""
        return CampaignsResponseBuilder.get_json(response)

    def build_nxt_nql_response(self, response: Response) -> NqlResponseType:
        """Build an NQL response through the domain builder."""
        return NqlResponseBuilder().build(response)

    def build_nxt_token_response(self, response: Response) -> NxtTokenResponse:
        """Build a token response through the domain builder."""
        return TokenResponseBuilder().build(response)
