"""Unit tests for Data Management device status responses."""

import pytest
from pydantic import ValidationError

from nexthink_api.DataManagement import NxtDataManagementDeviceStatus, NxtDeviceStatus


class TestNxtDeviceStatus:
    """Test NxtDeviceStatus."""

    def test_device_status_accepts_scheduled_status(self) -> None:
        """Device status accepts SCHEDULED status."""
        status = NxtDeviceStatus(
            uid="00000000-0000-0000-0000-000000000000",
            name="DEVICE-1",
            status=NxtDataManagementDeviceStatus.SCHEDULED,
        )

        assert status.status == NxtDataManagementDeviceStatus.SCHEDULED

    def test_device_status_parses_invalid_status(self) -> None:
        """Device status parses INVALID status from string."""
        status = NxtDeviceStatus(
            uid="not-a-uuid",
            name="DEVICE-1",
            status="INVALID",
        )

        assert status.status == NxtDataManagementDeviceStatus.INVALID

    def test_device_status_parses_failed_status(self) -> None:
        """Device status parses FAILED status from string."""
        status = NxtDeviceStatus(
            uid="00000000-0000-0000-0000-000000000000",
            name="DEVICE-1",
            status="FAILED",
        )

        assert status.status == NxtDataManagementDeviceStatus.FAILED

    def test_device_status_rejects_unknown_status(self) -> None:
        """Device status rejects unknown status."""
        with pytest.raises(ValidationError):
            NxtDeviceStatus(uid="not-a-uuid", name="DEVICE-1", status="UNKNOWN")
