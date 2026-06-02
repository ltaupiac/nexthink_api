"""Unit tests for Data Management device deletion responses."""

import pytest
from pydantic import ValidationError

from nexthink_api.DataManagement import (
    NxtDataManagementBatchStatus,
    NxtDataManagementDeviceStatus,
    NxtDeviceDeletionResponse,
    NxtDeviceStatus,
)


class TestNxtDeviceDeletionResponse:
    """Test NxtDeviceDeletionResponse."""

    def test_device_deletion_response_accepts_success_payload(self) -> None:
        """Device deletion response accepts success payload."""
        device = NxtDeviceStatus(
            uid="00000000-0000-0000-0000-000000000000",
            name="DEVICE-1",
            status=NxtDataManagementDeviceStatus.SCHEDULED,
        )
        response = NxtDeviceDeletionResponse(
            scheduledCount=1,
            status=NxtDataManagementBatchStatus.ACCEPTED,
            devices=[device],
        )

        assert response.scheduledCount == 1
        assert response.status == NxtDataManagementBatchStatus.ACCEPTED
        assert response.devices == [device]
        assert response.request_id is None

    def test_device_deletion_response_accepts_request_id(self) -> None:
        """Device deletion response accepts response request id."""
        response = NxtDeviceDeletionResponse(
            scheduledCount=1,
            status=NxtDataManagementBatchStatus.ACCEPTED,
            devices=[],
            request_id="11111111-1111-1111-1111-111111111111",
        )

        assert response.request_id == "11111111-1111-1111-1111-111111111111"

    def test_device_deletion_response_parses_string_statuses(self) -> None:
        """Device deletion response parses string statuses."""
        response = NxtDeviceDeletionResponse(
            scheduledCount=1,
            status="ACCEPTED",
            devices=[
                {
                    "uid": "00000000-0000-0000-0000-000000000000",
                    "name": "DEVICE-1",
                    "status": "SCHEDULED",
                },
                {
                    "uid": "not-a-uuid",
                    "name": "DEVICE-2",
                    "status": "INVALID",
                },
                {
                    "uid": "00000000-0000-0000-0000-000000000002",
                    "name": "DEVICE-3",
                    "status": "FAILED",
                }
            ],
        )

        assert response.status == NxtDataManagementBatchStatus.ACCEPTED
        assert response.devices[0].status == NxtDataManagementDeviceStatus.SCHEDULED
        assert response.devices[1].status == NxtDataManagementDeviceStatus.INVALID
        assert response.devices[2].status == NxtDataManagementDeviceStatus.FAILED

    def test_device_deletion_response_rejects_negative_scheduled_count(self) -> None:
        """Device deletion response rejects negative scheduled count."""
        with pytest.raises(ValidationError):
            NxtDeviceDeletionResponse(scheduledCount=-1, status="ACCEPTED", devices=[])
