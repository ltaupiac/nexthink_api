"""Device entry request object for the Nexthink Data Management API."""

from pydantic import BaseModel, Field

__all__ = ["NxtDeviceEntry"]


class NxtDeviceEntry(BaseModel):
    """Identify a device scheduled for deletion.

    Attributes
    ----------
        uid : str
            UID of the device as reported by the Nexthink Collector.
        name : str
            Name of the device as reported by the Nexthink Collector.

    """

    uid: str = Field(min_length=1)
    name: str = Field(min_length=1)
