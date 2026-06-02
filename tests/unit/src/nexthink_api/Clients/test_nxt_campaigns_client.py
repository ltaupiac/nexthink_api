"""Unit tests for the internal Campaigns client."""

import pytest

from nexthink_api import NxtCampaignTriggerRequest, NxtEndpoint
from nexthink_api.Clients.nxt_campaigns_client import NxtCampaignsClient


def _request() -> NxtCampaignTriggerRequest:
    """Return a minimal valid Campaigns trigger request."""
    return NxtCampaignTriggerRequest(
        campaignNqlId="#it_satisfaction",
        userSid=["S-1-5-21-1"],
        expiresInMinutes=60,
    )


def test_trigger_posts_campaign_request(mocker: object) -> None:
    """Campaigns trigger validates POST support and delegates transport POST."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.post.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_campaigns_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtCampaignsClient(api_client)

    value = client.trigger(_request())

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.Engage, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Engage)
    api_client.transport.post.assert_called_once_with(
        "/api/v1/euf/campaign/trigger",
        headers=api_client.headers,
        json={
            "campaignNqlId": "#it_satisfaction",
            "userSid": ["S-1-5-21-1"],
            "expiresInMinutes": 60,
        },
    )


def test_trigger_rejects_unsupported_post_method(mocker: object) -> None:
    """Campaigns trigger fails before sending HTTP when POST is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    client = NxtCampaignsClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.trigger(_request())

    api_client.transport.post.assert_not_called()
