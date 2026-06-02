"""Unit tests for Campaigns trigger success response models."""

import pytest
from pydantic import ValidationError

from nexthink_api import NxtCampaignTriggerResponseDetails, NxtCampaignTriggerSuccessResponse


def test_trigger_success_response_accepts_created_and_failed_user_results() -> None:
    """Success response contains one result per returned user SID."""
    response = NxtCampaignTriggerSuccessResponse(
        requests=[
            NxtCampaignTriggerResponseDetails(userSid="S-1-5-21-1", requestId="request-1"),
            NxtCampaignTriggerResponseDetails(userSid="S-1-5-21-2", message="Campaign not enabled"),
        ],
    )

    assert response.requests[0].requestId == "request-1"
    assert response.requests[1].message == "Campaign not enabled"


def test_trigger_success_response_rejects_empty_request_list() -> None:
    """Success response requires at least one request detail."""
    with pytest.raises(ValidationError):
        NxtCampaignTriggerSuccessResponse(requests=[])
