"""Unit tests for Campaigns trigger request model."""

import pytest
from pydantic import ValidationError

from nexthink_api import NxtCampaignTriggerRequest


def test_trigger_request_accepts_valid_payload() -> None:
    """Trigger request accepts the documented payload shape."""
    request = NxtCampaignTriggerRequest(
        campaignNqlId="#it_satisfaction",
        userSid=["S-1-5-21-1"],
        expiresInMinutes=60,
        parameters={"ticket": "INC001"},
    )

    assert request.model_dump(exclude_none=True) == {
        "campaignNqlId": "#it_satisfaction",
        "userSid": ["S-1-5-21-1"],
        "expiresInMinutes": 60,
        "parameters": {"ticket": "INC001"},
    }


def test_trigger_request_rejects_empty_user_sid_list() -> None:
    """Trigger request requires at least one target user SID."""
    with pytest.raises(ValidationError):
        NxtCampaignTriggerRequest(
            campaignNqlId="#it_satisfaction",
            userSid=[],
            expiresInMinutes=60,
        )


def test_trigger_request_rejects_expiration_below_api_minimum() -> None:
    """Trigger request follows the documented expiration lower bound."""
    with pytest.raises(ValidationError):
        NxtCampaignTriggerRequest(
            campaignNqlId="#it_satisfaction",
            userSid=["S-1-5-21-1"],
            expiresInMinutes=0,
        )


def test_trigger_request_rejects_too_many_parameters() -> None:
    """Trigger request follows the documented maximum number of parameters."""
    with pytest.raises(ValidationError):
        NxtCampaignTriggerRequest(
            campaignNqlId="#it_satisfaction",
            userSid=["S-1-5-21-1"],
            expiresInMinutes=60,
            parameters={f"parameter_{index}": "value" for index in range(31)},
        )
