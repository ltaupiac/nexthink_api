"""Device deletion response object for the Nexthink Data Management API."""
# ruff: noqa: N815 - Naming conforme to Nexthink Data Management API schema.

from pydantic import BaseModel, NonNegativeInt

from nexthink_api.DataManagement.nxt_data_management_status import NxtDataManagementBatchStatus
from nexthink_api.DataManagement.nxt_device_status import NxtDeviceStatus

__all__ = ["NxtDeviceDeletionResponse"]


class NxtDeviceDeletionResponse(BaseModel):
    """Scheduling result for a device deletion batch.

    Attributes
    ----------
        scheduledCount : NonNegativeInt
            Number of devices successfully queued for deletion.
        status : NxtDataManagementBatchStatus
            Overall batch status.
        devices : list[NxtDeviceStatus]
            Per-device scheduling outcome, in the same order as the request.
        request_id : str | None
            Optional response correlation identifier from the x-request-id header.

    """

    scheduledCount: NonNegativeInt
    status: NxtDataManagementBatchStatus
    devices: list[NxtDeviceStatus]
    request_id: str | None = None
