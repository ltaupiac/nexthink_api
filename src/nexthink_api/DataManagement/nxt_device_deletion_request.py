"""Device deletion request object for the Nexthink Data Management API."""

from pydantic import BaseModel, conlist

from nexthink_api.DataManagement.nxt_device_entry import NxtDeviceEntry

__all__ = ["NxtDeviceDeletionRequest"]


class NxtDeviceDeletionRequest(BaseModel):
    """Batch of devices to be deleted from the Nexthink inventory.

    Attributes
    ----------
        devices : list[NxtDeviceEntry]
            Non-empty list of devices to delete. Maximum 100 devices per request.

    """

    devices: conlist(NxtDeviceEntry, min_length=1, max_length=100)
