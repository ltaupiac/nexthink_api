"""UID validation modes for Data Management device deletion requests."""

from enum import Enum

__all__ = ["NxtUidValidationMode"]


class NxtUidValidationMode(str, Enum):
    """UID validation mode for Data Management device deletion calls."""

    STRICT = "strict"
    WARN = "warn"
    PERMISSIVE = "permissive"
