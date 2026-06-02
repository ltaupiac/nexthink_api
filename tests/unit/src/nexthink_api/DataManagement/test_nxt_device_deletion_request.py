"""Unit tests for Data Management device deletion requests."""

import pytest
from pydantic import ValidationError

from nexthink_api.DataManagement import NxtDeviceDeletionRequest, NxtDeviceEntry

MAX_DEVICES = 100


class TestNxtDeviceDeletionRequest:
    """Test NxtDeviceDeletionRequest."""

    def test_device_deletion_request_accepts_one_device(self) -> None:
        """Device deletion request accepts one device."""
        device = NxtDeviceEntry(uid="00000000-0000-0000-0000-000000000000", name="DEVICE-1")
        request = NxtDeviceDeletionRequest(devices=[device])

        assert request.devices == [device]

    def test_device_deletion_request_accepts_100_devices(self) -> None:
        """Device deletion request accepts 100 devices."""
        devices = [
            NxtDeviceEntry(uid=f"00000000-0000-0000-0000-{index:012d}", name=f"DEVICE-{index}")
            for index in range(MAX_DEVICES)
        ]
        request = NxtDeviceDeletionRequest(devices=devices)

        assert len(request.devices) == MAX_DEVICES

    def test_device_deletion_request_rejects_empty_devices(self) -> None:
        """Device deletion request rejects empty devices list."""
        with pytest.raises(ValidationError):
            NxtDeviceDeletionRequest(devices=[])

    def test_device_deletion_request_requires_devices(self) -> None:
        """Device deletion request requires devices."""
        with pytest.raises(ValidationError):
            NxtDeviceDeletionRequest()

    def test_device_deletion_request_rejects_more_than_100_devices(self) -> None:
        """Device deletion request rejects more than 100 devices."""
        devices = [
            NxtDeviceEntry(uid=f"00000000-0000-0000-0000-{index:012d}", name=f"DEVICE-{index}")
            for index in range(MAX_DEVICES + 1)
        ]

        with pytest.raises(ValidationError):
            NxtDeviceDeletionRequest(devices=devices)
