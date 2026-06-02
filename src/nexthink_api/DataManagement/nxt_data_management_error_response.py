"""Error response object for the Nexthink Data Management API."""

from pydantic import BaseModel

from nexthink_api.DataManagement.nxt_data_management_error_code import NxtDataManagementErrorCode

__all__ = ["NxtDataManagementErrorResponse"]


class NxtDataManagementErrorResponse(BaseModel):
    """Error details returned with Data Management 4xx and 5xx responses.

    Attributes
    ----------
        code : NxtDataManagementErrorCode
            Stable machine-readable error code identifying the failure reason.
        message : str
            Human-readable description of the error.
        request_id : str | None
            Optional response correlation identifier from the x-request-id header.

    """

    code: NxtDataManagementErrorCode
    message: str
    request_id: str | None = None
