"""Unit tests for Data Management status values."""

from nexthink_api.DataManagement import NxtDataManagementBatchStatus, NxtDataManagementDeviceStatus


class TestNxtDataManagementStatus:
    """Test Data Management status enums."""

    def test_batch_status_matches_documented_values(self) -> None:
        """Batch status enum matches documented values."""
        values = {status.value for status in NxtDataManagementBatchStatus}

        assert values == {"ACCEPTED"}

    def test_device_status_matches_documented_values(self) -> None:
        """Device status enum matches documented values."""
        values = {status.value for status in NxtDataManagementDeviceStatus}

        assert values == {"SCHEDULED", "INVALID", "FAILED"}
