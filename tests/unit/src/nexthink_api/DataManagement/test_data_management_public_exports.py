"""Unit tests for Data Management public exports."""

import nexthink_api
from nexthink_api import (
    NxtDataManagementBatchStatus,
    NxtDataManagementDeviceStatus,
    NxtDataManagementErrorCode,
    NxtDataManagementErrorResponse,
    NxtDeviceDeletionRequest,
    NxtDeviceDeletionResponse,
    NxtDeviceEntry,
    NxtDeviceStatus,
    NxtUidValidationMode,
)


class TestDataManagementPublicExports:
    """Test Data Management root package exports."""

    def test_data_management_classes_are_exported_from_root_package(self) -> None:
        """Data Management classes are exported from nexthink_api."""
        assert nexthink_api.NxtDataManagementBatchStatus is NxtDataManagementBatchStatus
        assert nexthink_api.NxtDataManagementDeviceStatus is NxtDataManagementDeviceStatus
        assert nexthink_api.NxtDataManagementErrorCode is NxtDataManagementErrorCode
        assert nexthink_api.NxtDataManagementErrorResponse is NxtDataManagementErrorResponse
        assert nexthink_api.NxtDeviceDeletionRequest is NxtDeviceDeletionRequest
        assert nexthink_api.NxtDeviceDeletionResponse is NxtDeviceDeletionResponse
        assert nexthink_api.NxtDeviceEntry is NxtDeviceEntry
        assert nexthink_api.NxtDeviceStatus is NxtDeviceStatus
        assert nexthink_api.NxtUidValidationMode is NxtUidValidationMode
