"""Data Management error response code values."""

from enum import Enum

__all__ = ["NxtDataManagementErrorCode"]


class NxtDataManagementErrorCode(str, Enum):
    """Data Management error response code."""

    EMPTY_REQUEST = "EMPTY_REQUEST"
    BATCH_SIZE_EXCEEDED = "BATCH_SIZE_EXCEEDED"
    INVALID_REQUEST = "INVALID_REQUEST"
    EMPTY_TENANT = "EMPTY_TENANT"
    FEATURE_NOT_ENABLED = "FEATURE_NOT_ENABLED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
