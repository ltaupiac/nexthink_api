"""Unit test file for nexthink_api."""

from nexthink_api import NxtFieldName


class TestNxtFieldName:  # pylint: disable=too-few-public-methods
    """Test field name enum values."""

    def test_nxt_field_name_values(self) -> None:
        """Field names stay aligned with the supported Enrichment model contract."""
        expected_fields = {
            "device/device/virtualization/desktop_pool",
            "device/device/virtualization/hostname",
            "device/device/virtualization/hypervisor_name",
            "device/device/virtualization/type",
            "device/device/virtualization/environment_name",
            "device/device/virtualization/desktop_broker",
            "device/device/virtualization/disk_image",
            "device/device/virtualization/last_update",
            "device/device/#{}",
            "user/user/#{}",
            "binary/binary/#{}",
            "package/package/#{}",
        }
        enum_values = {member.value for member in NxtFieldName}
        assert enum_values == expected_fields
