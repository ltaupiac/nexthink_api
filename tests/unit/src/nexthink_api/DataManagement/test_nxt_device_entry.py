"""Unit tests for Data Management device entries."""

import pytest
from pydantic import ValidationError

from nexthink_api.DataManagement import NxtDeviceEntry


class TestNxtDeviceEntry:
    """Test NxtDeviceEntry."""

    def test_device_entry_accepts_required_fields(self) -> None:
        """Device entry accepts uid and name."""
        entry = NxtDeviceEntry(uid="not-a-uuid", name="DEVICE-1")

        assert entry.uid == "not-a-uuid"
        assert entry.name == "DEVICE-1"

    def test_device_entry_rejects_blank_uid(self) -> None:
        """Device entry rejects blank uid."""
        with pytest.raises(ValidationError):
            NxtDeviceEntry(uid="", name="DEVICE-1")

    def test_device_entry_requires_uid(self) -> None:
        """Device entry requires uid."""
        with pytest.raises(ValidationError):
            NxtDeviceEntry(name="DEVICE-1")

    def test_device_entry_rejects_blank_name(self) -> None:
        """Device entry rejects blank name."""
        with pytest.raises(ValidationError):
            NxtDeviceEntry(uid="00000000-0000-0000-0000-000000000000", name="")

    def test_device_entry_requires_name(self) -> None:
        """Device entry requires name."""
        with pytest.raises(ValidationError):
            NxtDeviceEntry(uid="00000000-0000-0000-0000-000000000000")
