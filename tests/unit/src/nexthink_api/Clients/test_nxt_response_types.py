"""Unit tests for response type exports."""

from http import HTTPStatus
import inspect

import pytest

from nexthink_api import Clients, NxtApiException, NxtEndpoint
from nexthink_api.Clients import DataManagementResponseType, NxtResponse
from nexthink_api.Clients.nxt_response_builders import (
    CampaignsResponseBuilder,
    DataManagementResponseBuilder,
    EnrichmentResponseBuilder,
    NqlResponseBuilder,
    RemoteActionsResponseBuilder,
    SparkResponseBuilder,
    TokenResponseBuilder,
    WorkflowsResponseBuilder,
)
from nexthink_api import NxtSuccessResponse


class TestNxtResponseTypes:
    """Test response type exports."""

    def test_data_management_response_type_is_exported(self) -> None:
        """Data Management response type alias is exported from Clients."""
        assert Clients.DataManagementResponseType is DataManagementResponseType

    def test_data_management_response_routes_to_data_management_builder(self, mocker: object) -> None:
        """Data Management response routes to Data Management builder."""
        response = mocker.Mock()
        response.url = "/api/v1/data-management/device/deletions"
        nxt_response = NxtResponse()
        expected = NxtSuccessResponse()
        builder = mocker.patch.object(
            NxtResponse,
            "build_nxt_data_management_response",
            return_value=expected,
        )

        assert nxt_response.from_response(response) is expected
        builder.assert_called_once_with(response)

    def test_response_builders_do_not_keep_stub_implementations(self) -> None:
        """Response builders must not silently return None or keep pass stubs."""
        facade_builder_names = [
            "build_nxt_act_response",
            "build_nxt_data_management_response",
            "build_nxt_engage_response",
            "build_nxt_enrichment_response",
            "build_nxt_nql_response",
            "build_nxt_spark_response",
            "build_nxt_token_response",
            "build_nxt_workflow_response",
        ]
        domain_builder_classes = [
            CampaignsResponseBuilder,
            DataManagementResponseBuilder,
            EnrichmentResponseBuilder,
            NqlResponseBuilder,
            RemoteActionsResponseBuilder,
            SparkResponseBuilder,
            TokenResponseBuilder,
            WorkflowsResponseBuilder,
        ]

        for builder_name in facade_builder_names:
            source = inspect.getsource(getattr(NxtResponse, builder_name))
            assert "\n        pass\n" not in source
            assert "return None" not in source

        for builder_class in domain_builder_classes:
            source = inspect.getsource(builder_class.build)
            assert "\n        pass\n" not in source
            assert "return None" not in source

    @pytest.mark.parametrize(
        ("builder_class", "url"),
        [
            (CampaignsResponseBuilder, NxtEndpoint.Engage.value),
            (DataManagementResponseBuilder, NxtEndpoint.DataManagement.value),
            (EnrichmentResponseBuilder, NxtEndpoint.Enrichment.value),
            (NqlResponseBuilder, NxtEndpoint.Nql.value),
            (RemoteActionsResponseBuilder, NxtEndpoint.Act.value),
            (SparkResponseBuilder, NxtEndpoint.SparkHandoff.value),
            (TokenResponseBuilder, NxtEndpoint.Token.value),
            (WorkflowsResponseBuilder, NxtEndpoint.Workflow.value),
        ],
    )
    def test_response_builders_raise_on_unknown_status_code(
            self,
            mocker: object,
            builder_class: type,
            url: str,
    ) -> None:
        """Response builders must raise explicitly instead of returning None."""
        response = mocker.Mock()
        response.url = url
        response.status_code = HTTPStatus.IM_A_TEAPOT
        response.reason = "teapot"
        response.text = '{"message": "teapot"}'
        response.json.return_value = {"message": "teapot"}

        with pytest.raises(NxtApiException, match="Unknown status response code"):
            builder_class().build(response)

    def test_unknown_endpoint_raises_api_exception(self, mocker: object) -> None:
        """Unknown endpoints must not be converted into typed API errors."""
        response = mocker.Mock()
        response.url = "/api/v1/unknown"

        with pytest.raises(NxtApiException, match="Can't create response"):
            NxtResponse().from_response(response)

    def test_unknown_status_raises_api_exception(self, mocker: object) -> None:
        """Unsupported statuses must not be converted into typed API errors."""
        response = mocker.Mock()
        response.url = NxtEndpoint.Enrichment.value
        response.status_code = HTTPStatus.IM_A_TEAPOT

        with pytest.raises(NxtApiException, match="Unknown status response code"):
            NxtResponse().from_response(response)
