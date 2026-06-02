"""Nexthink API Call Point List."""

from typing import Final, Optional
from enum import Enum


class NxtEndpoint(str, Enum):
    """Endpoint list of the Nexthink API."""

    Enrichment: Final[str] = '/api/v1/enrichment/data/fields'
    Act: Final[str] = '/api/v1/act/execute'
    Engage: Final[str] = '/api/v1/euf/campaign/trigger'
    Workflow: Final[str] = '/api/v1/workflows/execute'
    WorkflowV2: Final[str] = '/api/v2/workflows/execute'
    WorkflowThinkletTrigger: Final[str] = '/api/v1/workflows/workflows'
    WorkflowDetails: Final[str] = '/api/v1/workflows/details'
    Workflows: Final[str] = '/api/v1/workflows'
    SparkHandoff: Final[str] = '/api/v1/spark/handoff'
    DataManagement: Final[str] = '/api/v1/data-management/device/deletions'
    RemoteActionsDetails: Final[str] = '/api/v1/act/remote-action/details'
    RemoteActions: Final[str] = '/api/v1/act/remote-action'
    Nql: Final[str] = '/api/v1/nql/execute'
    NqlV2: Final[str] = '/api/v2/nql/execute'
    NqlExport: Final[str] = '/api/v1/nql/export'
    NqlStatus: Final[str] = '/api/v1/nql/status'
    Token: Final[str] = '/api/v1/token'

    @classmethod
    def get_api_name(cls, path: str) -> Optional[str]:
        """Get the API name from the path.

        Parameters
        ----------
            path : str
                path to the API.

        Returns
        -------
            Optional[str]
                The name of the API or None if path is not in the Endpoints list.

        """
        matching_endpoints = [endpoint for endpoint in cls if path.startswith(endpoint.value)]
        if not matching_endpoints:
            return None
        return max(matching_endpoints, key=lambda endpoint: len(endpoint.value)).name
