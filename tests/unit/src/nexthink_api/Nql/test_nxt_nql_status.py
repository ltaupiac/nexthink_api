"""Unit test file for nexthink_api."""

from nexthink_api import (
    NxtNqlStatus,
)


class TestNxtNqlStatus:  # pylint: disable=too-few-public-methods
    """Test NQL status enum values."""

    def test_nql_status_response_values(self) -> None:
        """NQL status values stay aligned with the supported NQL model contract."""
        expected_statuses = {"SUBMITTED", "IN_PROGRESS", "ERROR", "COMPLETED"}
        enum_values = {member.value for member in NxtNqlStatus}
        assert enum_values == expected_statuses
