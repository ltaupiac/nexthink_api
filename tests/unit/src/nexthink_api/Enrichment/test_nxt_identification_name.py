"""Unit tests for enrichment identification names."""

from nexthink_api import NxtIdentificationName


class TestNxtIdentificationName:  # pylint: disable=too-few-public-methods
    """Test identification name enum values."""

    def test_nxt_identification_name_values(self) -> None:
        """Identification names stay aligned with the supported Enrichment model contract."""
        expected_identifications = {
            "device/device/name",
            "device/device/uid",
            "user/user/sid",
            "user/user/uid",
            "user/user/upn",
            "binary/binary/uid",
            "package/package/uid",
        }
        enum_values = {member.value for member in NxtIdentificationName}
        assert enum_values == expected_identifications
