"""Internal NQL domain client."""

import time
from http import HTTPStatus
from io import StringIO
from typing import Optional, Union
from urllib.parse import urljoin

import pandas as pd
import requests

from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.Clients.nxt_response import NqlResponseType, NxtResponse
from nexthink_api.Exceptions.nxt_export_exception import NxtExportException
from nexthink_api.Exceptions.nxt_status_exception import NxtStatusException
from nexthink_api.Exceptions.nxt_timeout_exception import NxtStatusTimeoutException
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse
from nexthink_api.Nql.nxt_nql_api_execute_request import NxtNqlApiExecuteRequest
from nexthink_api.Nql.nxt_nql_api_export_response import NxtNqlApiExportResponse
from nexthink_api.Nql.nxt_nql_api_status_response import NxtNqlApiStatusResponse
from nexthink_api.Nql.nxt_nql_status import NxtNqlStatus

__all__ = ["NxtNqlClient"]


class NxtNqlClient:
    """Internal delegate for NQL behavior.

    Auth, persistent headers, settings, and transport lifecycle remain owned by
    ``NxtApiClient`` during this phase. This client owns NQL request orchestration
    and delegates HTTP execution back to the facade.
    """

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal NQL client."""
        self._api_client = api_client

    def execute(
            self,
            data: NxtNqlApiExecuteRequest,
            version: str = "v2",
    ) -> NqlResponseType:
        """Execute an NQL query with the requested NQL API version."""
        endpoint_by_version = {
            "v1": NxtEndpoint.Nql,
            "v2": NxtEndpoint.NqlV2,
        }
        try:
            endpoint = endpoint_by_version[version]
        except KeyError as error:
            raise ValueError("Unsupported NQL execute version") from error
        return self.run_nql(endpoint, data)

    def export(self, data: NxtNqlApiExecuteRequest) -> NqlResponseType:
        """Start an NQL export request."""
        return self.run_nql(NxtEndpoint.NqlExport, data)

    def wait(
            self,
            value: NxtNqlApiExportResponse,
            timeout: int = 300,
    ) -> Union[NxtNqlApiStatusResponse, NxtErrorResponse]:
        """Wait for an NQL export request to complete."""
        return self.wait_status(value, timeout)

    def download(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> requests.models.Response:
        """Download an NQL export file."""
        return self.download_export(value, timeout)

    def download_dataframe(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> pd.DataFrame:
        """Download an NQL export file as a pandas DataFrame."""
        return self.download_export_as_df(value, timeout)

    def run_nql(
            self,
            endpoint: NxtEndpoint,
            data: NxtNqlApiExecuteRequest,
            method: Optional[str] = None,
    ) -> NqlResponseType:
        """Run an NQL query on the specified endpoint using the provided data."""
        method = method or 'POST'
        if not self._api_client.check_method(endpoint, method):
            raise ValueError('Unsupported HTTP method')
        self._api_client.update_header(endpoint)
        if method == 'POST':
            return self._api_client.post(endpoint, data)
        return self._api_client.get(endpoint, data)

    def wait_status(
            self,
            value: NxtNqlApiExportResponse,
            timeout: int = 300,
    ) -> Union[NxtNqlApiStatusResponse, NxtErrorResponse]:
        """Wait for the status of an NQL API export request to complete."""
        start = time.time()
        status = NxtNqlApiStatusResponse(status=NxtNqlStatus.SUBMITTED)
        while status.status in {NxtNqlStatus.SUBMITTED, NxtNqlStatus.IN_PROGRESS}:
            status = self.get_status_export(value)
            if isinstance(status, NxtErrorResponse):
                return status
            if time.time() - start > timeout:
                raise NxtStatusTimeoutException("Status not completed before timeout")
            time.sleep(1)
        return status

    def get_status_export(self, value: NxtNqlApiExportResponse) -> NqlResponseType:
        """Retrieve the status of an export based on the provided export response."""
        endpoint = NxtEndpoint.NqlStatus
        if not self._api_client.check_method(endpoint, "GET"):
            raise ValueError('Unsupported HTTP method')
        self._api_client.update_header(endpoint)
        export_status_path = urljoin(NxtEndpoint.NqlStatus.value + '/', value.exportId)
        response = self._api_client.transport.get(export_status_path, headers=self._api_client.headers)
        nxt_response = NxtResponse()
        response_status = nxt_response.from_response(response=response)
        return response_status

    def download_export(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> requests.models.Response:
        """Download an export file based on the NQL status response."""
        if value.status != NxtNqlStatus.COMPLETED:
            raise NxtStatusException("Try do download an export not completed")
        return self._api_client.transport.get_url(str(value.resultsFileUrl), timeout=timeout)

    def download_export_as_df(self, value: NxtNqlApiStatusResponse, timeout: int = 300) -> pd.DataFrame:
        """Download an export file as a pandas DataFrame."""
        response = self.download_export(value, timeout)
        if response.status_code == HTTPStatus.OK:
            return pd.read_csv(StringIO(response.text))
        raise NxtExportException(f'Failed to download export:Status code {response.status_code}')
