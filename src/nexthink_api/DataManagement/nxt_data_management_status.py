"""Data Management response status values."""

from enum import Enum

__all__ = [
    "NxtDataManagementBatchStatus",
    "NxtDataManagementDeviceStatus",
]


class NxtDataManagementBatchStatus(str, Enum):
    """Data Management batch status."""

    ACCEPTED = "ACCEPTED"


class NxtDataManagementDeviceStatus(str, Enum):
    """Data Management per-device status."""

    SCHEDULED = "SCHEDULED"
    INVALID = "INVALID"
    FAILED = "FAILED"
