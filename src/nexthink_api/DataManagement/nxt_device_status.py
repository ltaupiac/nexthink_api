"""Device deletion status response object for the Nexthink Data Management API."""

from pydantic import BaseModel

from nexthink_api.DataManagement.nxt_data_management_status import NxtDataManagementDeviceStatus

__all__ = ["NxtDeviceStatus"]


class NxtDeviceStatus(BaseModel):
    """Scheduling outcome for a single device.

    Attributes
    ----------
        uid : str
            UID of the device as submitted.
        name : str
            Name of the device as submitted.
        status : NxtDataManagementDeviceStatus
            Per-device scheduling outcome.

    """

    uid: str
    name: str
    status: NxtDataManagementDeviceStatus
