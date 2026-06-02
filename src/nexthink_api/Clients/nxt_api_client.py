"""Class used to send requests and build responses from the Nexthink Enrichment API."""

import warnings
from typing import Optional, Union
import pandas as pd
import requests


from nexthink_api.Exceptions.nxt_legacy_api_warning import NxtLegacyApiWarning
from nexthink_api.Models.nxt_settings import NxtSettings
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Models.nxt_region_name import NxtRegionName
from nexthink_api.Models.nxt_token_request import NxtTokenRequest
from nexthink_api.Models.nxt_token_response import NxtTokenResponse
from nexthink_api.DataManagement.nxt_device_deletion_request import NxtDeviceDeletionRequest
from nexthink_api.DataManagement.nxt_device_entry import NxtDeviceEntry
from nexthink_api.DataManagement.nxt_uid_validation_mode import NxtUidValidationMode
from nexthink_api.Enrichment.nxt_enrichment_request import NxtEnrichmentRequest
from nexthink_api.Nql.nxt_nql_api_execute_request import NxtNqlApiExecuteRequest
from nexthink_api.Nql.nxt_nql_api_status_response import NxtNqlApiStatusResponse
from nexthink_api.Nql.nxt_nql_api_export_response import NxtNqlApiExportResponse
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse
from nexthink_api.Utils.nxt_spec_registry import SpecRegistry
from nexthink_api.Clients.nxt_campaigns_client import NxtCampaignsClient
from nexthink_api.Clients.nxt_data_management_client import NxtDataManagementClient
from nexthink_api.Clients.nxt_enrichment_client import NxtEnrichmentClient
from nexthink_api.Clients.nxt_http_transport import NxtHttpTransport
from nexthink_api.Clients.nxt_nql_client import NxtNqlClient
from nexthink_api.Clients.nxt_remote_actions_client import NxtRemoteActionsClient
from nexthink_api.Clients.nxt_spark_client import NxtSparkClient
from nexthink_api.Clients.nxt_token_provider import NxtTokenProvider
from nexthink_api.Clients.nxt_workflows_client import NxtWorkflowsClient
from nexthink_api.Clients.nxt_response import (
    ResponseApiType,
    NxtResponse,
    DataManagementResponseType,
    EnrichmentResponseType,
    NqlResponseType,
)

__all__ = ["NxtApiClient"]


LEGACY_CLIENT_MESSAGE = (
    "`NxtApiClient` is deprecated as the public entrypoint. "
    "Use `NexthinkClient` for new code."
)

LEGACY_METHOD_REPLACEMENTS = {
    "run_enrichment": "Use `client.enrichment.run(data)` instead.",
    "run_nql": "Use `client.nql.execute(data)` or `client.nql.export(data)` instead.",
    "delete_devices": "Use `client.data_management.delete_devices(...)` instead.",
    "wait_status": "Use `client.nql.wait(value, timeout=...)` instead.",
    "get_status_export": "Use `client.nql.get_status_export(value)` instead.",
    "download_export": "Use `client.nql.download(value, timeout=...)` instead.",
    "download_export_as_df": "Use `client.nql.download_dataframe(value, timeout=...)` instead.",
}


class NxtApiClient:  # noqa: PLR0904 - historical compatibility facade exposes legacy and domain methods.
    """Initializes a new instance of the NxtApiClient class.

    Parameters
    ----------
        instance : str
            The name of the Nexthink instance.
        region : NxtRegionName
            The region of the Nexthink instance.
        client_id : str
            The client ID for authentication.
        client_secret : str
            The client secret for authentication.
        proxies : Optional[dict]
            A dictionary of proxies to use for the requests. Defaults to None.

    > ### Note.
    >   - if proxy are not provided, it will try to detect proxies from environment variables
    >   - if no proxy are detected, it will disable the proxy
    >   - false value disable the proxy

    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 instance: str,
                 region: NxtRegionName,
                 client_id: str,
                 client_secret: str,
                 proxies=None):  # noqa: ANN001
        """Initialize a new instance of the NxtApiClient class.

        Parameters
        ----------
            instance : str
                The name of the Nexthink instance.
            region : NxtRegionName
                The region of the Nexthink instance.
            client_id : str
                The client ID for authentication.
            client_secret : str
                The client secret for authentication.
            proxies : Optional[dict]
                A dictionary of proxies to use for the requests. Defaults to None.

            > ### Note.
            >   - if proxy are not provided, it will try to detect proxies from environment variables
            >   - if no proxy are detected, it will disable the proxy
            >   - false value disable the proxy


        """
        if type(self) is NxtApiClient:
            warnings.warn(LEGACY_CLIENT_MESSAGE, NxtLegacyApiWarning, stacklevel=2)
        self.settings = NxtSettings(instance=instance, region=region, proxies=proxies)
        self.transport = NxtHttpTransport(
            base_url=str(self.settings.infinity_base_uri),
            proxies=self.settings.proxies,
            timeout=300,
        )
        self.token_provider = NxtTokenProvider(
            settings=self.settings,
            transport=self.transport,
            client_id=client_id,
            client_secret=client_secret,
        )
        self._data_management_client = NxtDataManagementClient(self)
        self._enrichment_client = NxtEnrichmentClient(self)
        self._nql_client = NxtNqlClient(self)
        self._remote_actions_client = NxtRemoteActionsClient(self)
        self._campaigns_client = NxtCampaignsClient(self)
        self._workflows_client = NxtWorkflowsClient(self)
        self._spark_client = NxtSparkClient(self)
        self.endpoint: NxtEndpoint
        self.token: Union[NxtTokenResponse, None] = None
        self.headers = {}
        self.init_token(client_id, client_secret)

    def init_token(self, client_id: str, client_secret: str) -> None:
        """Initialize the token using the provided client ID and client secret.

        Parameters
        ----------
            client_id : str
                The client ID.
            client_secret : str
                The client secret.

        Returns
        -------
            None

        """
        self.create_autorisation(client_id, client_secret)
        if self.get_bearer_token():
            self.update_header()

    def update_header(self, endpoint: NxtEndpoint = None) -> None:
        """Update header for subsequent requests based on the given endpoint.

        Parameters
        ----------
            endpoint : NxtEndpoint, optional
                The endpoint type for which to update the header. Defaults to None.

        Returns
        -------
            None

        """
        # Update header for subsequent requests
        access_token = getattr(self.token, 'access_token', None)
        if endpoint in {None, NxtEndpoint.NqlExport, NxtEndpoint.NqlStatus}:
            self.headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/csv",
            }
        else:
            self.headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

    def create_autorisation(self, client_id: str, client_secret: str) -> None:
        """Create authorization using client ID and client secret.

        Parameters
        ----------
            client_id : str
                The client ID.
            client_secret :str
                The client secret.

        Returns
        -------
            None

        """
        if self.token is None:
            self.token_provider.client_id = client_id
            self.token_provider.client_secret = client_secret
            self.headers = self.token_provider.basic_auth_headers()

    def get_bearer_token(self) -> bool:
        """Retrieve a bearer token from the server.

        Returns
        -------
            bool
                True if the token was successfully retrieved, False otherwise.

        Raises
        ------
            NxtTokenException
                If an error occurs during the token retrieval.

        """
        token = self.token_provider.get_token()
        self.token = token
        return token is not None

    @property
    def enrichment(self) -> NxtEnrichmentClient:
        """Return the Enrichment domain client."""
        return self._enrichment_client

    @property
    def nql(self) -> NxtNqlClient:
        """Return the NQL domain client."""
        return self._nql_client

    @property
    def data_management(self) -> NxtDataManagementClient:
        """Return the Data Management domain client."""
        return self._data_management_client

    @property
    def remote_actions(self) -> NxtRemoteActionsClient:
        """Return the Remote Actions domain client."""
        return self._remote_actions_client

    @property
    def campaigns(self) -> NxtCampaignsClient:
        """Return the Campaigns domain client."""
        return self._campaigns_client

    @property
    def workflows(self) -> NxtWorkflowsClient:
        """Return the Workflows domain client."""
        return self._workflows_client

    @property
    def spark(self) -> NxtSparkClient:
        """Return the Spark domain client."""
        return self._spark_client

    def run_enrichment(self, endpoint: NxtEndpoint, data: NxtEnrichmentRequest) -> EnrichmentResponseType:
        """Run an enrichment request on the specified endpoint using the provided data.

        Parameter
        ----
            endpoint : NxtEndpoint
                The endpoint to run the enrichment request on.
            data : NxtEnrichmentRequest
                The data containing the enrichment request.

        Raises
        ------
            ValueError
                If the specified HTTP method is not supported.

        Returns
        -------
            EnrichmentResponseType
                The EnrichmentResponseType object containing the response from the API call.

        """
        self._warn_legacy_method("run_enrichment")
        return self._enrichment_client.run_enrichment(endpoint, data)

    def run_nql(self,
                endpoint: NxtEndpoint,
                data: NxtNqlApiExecuteRequest,
                method: Optional[str] = None) -> NqlResponseType:
        """Run an NQL query on the specified endpoint using the provided data.

        Parameters
        ----------
            endpoint : NxtEndpoint
                The endpoint to run the NQL query on.
            data NxtNqlApiExecuteRequest
                The data containing the NQL query.
            method : Optional[str], optional
                The HTTP method to use for the request. Defaults to 'POST'.

        Raises
        ------
            ValueError
                If the specified HTTP method is not supported.

        Returns
        -------
            NqlResponseType
                The nql response object containing the response from the API call.

        """
        self._warn_legacy_method("run_nql")
        return self._nql_client.run_nql(endpoint, data, method)

    def delete_devices(
            self,
            devices: list[NxtDeviceEntry],
            request_id: Optional[str] = None,
            uid_validation: NxtUidValidationMode = NxtUidValidationMode.WARN,
    ) -> DataManagementResponseType:
        """Schedule device deletions through the Data Management API.

        Parameters
        ----------
            devices : list[NxtDeviceEntry]
                Devices to delete from the Nexthink inventory.
            request_id : Optional[str], optional
                Optional x-request-id correlation UUID. Defaults to None.
            uid_validation : NxtUidValidationMode, optional
                Local UID validation mode. Defaults to WARN.

        Returns
        -------
            DataManagementResponseType
                Data Management response object returned by the API.

        Raises
        ------
            ValueError
                If POST is not supported or STRICT UID validation detects malformed UIDs.

        """
        self._warn_legacy_method("delete_devices")
        return self._data_management_client.delete_devices(
            devices=devices,
            request_id=request_id,
            uid_validation=uid_validation,
        )

    @staticmethod
    def validate_device_uids(
            devices: list[NxtDeviceEntry],
            uid_validation: NxtUidValidationMode,
    ) -> None:
        """Validate Data Management device UIDs according to the provided mode."""
        NxtDataManagementClient.validate_device_uids(devices, uid_validation)

    @staticmethod
    def is_valid_uuid(value: str) -> bool:
        """Return True if value is a valid UUID."""
        return NxtDataManagementClient.is_valid_uuid(value)

    def wait_status(
            self,
            value: NxtNqlApiExportResponse,
            timeout: int = 300
    ) -> Union[NxtNqlApiStatusResponse, NxtErrorResponse]:
        """Wait for the status of an NQL API export request to complete.

        Parameters
        ----------
            value : NxtNqlApiExportResponse
                The export request to check the status of.
            timeout : int, optional
                The maximum time to wait for the status to complete. Defaults to 300.

        Returns
        -------
            Union[NxtNqlApiStatusResponse, NxtErrorResponse]
                The final status response of the export request.

        """
        self._warn_legacy_method("wait_status")
        return self._nql_client.wait_status(value, timeout)

    def get_status_export(self, value: NxtNqlApiExportResponse) -> NqlResponseType:
        """Retrieve the status of an export based on the provided NxtNqlApiExportResponse value.

        Constructs the export status URL and makes a GET request to fetch the status.
        Converts the response to a NxtNqlStatus object and returns it.

        Parameters
        ----------
            value : NxtNqlApiExportResponse
                The export response object containing export ID.

        Returns
        -------
            NqlResponseType
                The status of the export operation.

        """
        self._warn_legacy_method("get_status_export")
        return self._nql_client.get_status_export(value)

    def download_export(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> requests.models.Response:
        """Download an export file based on the NxtNqlApiStatusResponse value and a timeout period.

        Parameters
        ----------
            value : NxtNqlApiStatusResponse
                The status response object containing the export details.
            timeout : int, optional
                The timeout period for the download request in seconds. Defaults to 300.

        Returns
        -------
            requests.models.Response
                The response object from the download request.

        """
        self._warn_legacy_method("download_export")
        return self._nql_client.download_export(value, timeout)

    def download_export_as_df(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> pd.DataFrame:
        """Download an export file as a pandas DataFrame based on the NxtNqlApiStatusResponse and a timeout period.

        Parameters
        ----------
            value : NxtNqlApiStatusResponse
                The status response object containing the export details.
            timeout : int, optional
                The timeout period for the download request in seconds. Defaults to 300.

        Returns
        -------
            pd.DataFrame
                The downloaded dataframe.

        """
        self._warn_legacy_method("download_export_as_df")
        return self._nql_client.download_export_as_df(value, timeout)

    # noinspection PyMethodMayBeStatic
    def check_method(self, endpoint: NxtEndpoint, method: str) -> bool:
        """Check if a given method is supported for a specific endpoint.

        Parameters
        ----------
            endpoint : NxtEndpoint
                The endpoint to check the method for.
            method : str
                The method to check.

        Returns
        -------
            bool
                True if the method is supported, False otherwise.

        """
        return SpecRegistry.supports_method(endpoint, method)

    def get(self,
            endpoint: NxtEndpoint,
            params=None) -> ResponseApiType:  # noqa: ANN001
        """Send a GET request to the specified endpoint with optional query parameters.

        Parameters
        ----------
            endpoint : NxtEndpoint
                The endpoint to send the request to.
            params : Optional[Dict[str, Any]]
                Query parameters to include in the request. Defaults to None.

        Returns
        -------
            ResponseAPIType
                The response object containing the status of the request.

        Raises
        ------
            requests.exceptions.RequestException
                If there was an error sending the request.

        """
        response = self.transport.get(endpoint.value, headers=self.headers, params=params)
        nxt_response = NxtResponse()
        response_status = nxt_response.from_response(response=response)
        return response_status

    def post(self,
             endpoint: NxtEndpoint,
             data: Union[
                 NxtTokenRequest,
                 NxtEnrichmentRequest,
                 NxtNqlApiExecuteRequest,
                 NxtDeviceDeletionRequest,
             ],
             headers: Optional[dict[str, str]] = None) -> ResponseApiType:
        """Send a POST request to the specified endpoint with the provided data.

        Parameters
        ----------
            endpoint : (NxtEndpoint
                The endpoint to send the request to.
            data : Union[NxtTokenRequest, NxtEnrichmentRequest, NxtNqlApiExecuteRequest, NxtDeviceDeletionRequest])
                The data to be sent in the request.
            headers : Optional[dict[str, str]]
                Extra headers for this request. Defaults to None.

        Returns
        -------
             ResponseAPIType
                The response object containing the status of the POST request.

        """
        response = self.transport.post(
            endpoint.value,
            headers=self.headers,
            extra_headers=headers,
            json=data.model_dump(),
        )
        nxt_response = NxtResponse()
        response_status = nxt_response.from_response(response=response)
        return response_status

    @staticmethod
    def _warn_legacy_method(method_name: str) -> None:
        """Warn when a historical facade method is used."""
        replacement = LEGACY_METHOD_REPLACEMENTS[method_name]
        warnings.warn(
            f"`NxtApiClient.{method_name}()` is deprecated. {replacement}",
            NxtLegacyApiWarning,
            stacklevel=3,
        )
