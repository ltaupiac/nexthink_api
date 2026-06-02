"""Unit tests for Campaigns response parsing."""

from http import HTTPStatus

from nexthink_api import (
    NxtCampaignTriggerErrorResponse,
    NxtCampaignTriggerSuccessResponse,
    NxtInvalidTokenRequest,
)
from nexthink_api.Clients import NxtResponse


def test_trigger_response_parses_success_response(mocker: object) -> None:
    """Campaigns 200 response parses trigger success details."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/euf/campaign/trigger"
    response.status_code = HTTPStatus.OK
    response.json.return_value = {
        "requests": [
            {"requestId": "request-1", "userSid": "S-1-5-21-1"},
            {"userSid": "S-1-5-21-2", "message": "Campaign not enabled"},
        ],
    }

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtCampaignTriggerSuccessResponse)
    assert value.requests[0].requestId == "request-1"
    assert value.requests[1].message == "Campaign not enabled"


def test_trigger_response_accepts_created_success_response(mocker: object) -> None:
    """Campaigns live API may return 201 even though the docs describe 200."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/euf/campaign/trigger"
    response.status_code = HTTPStatus.CREATED
    response.json.return_value = {
        "requests": [
            {"requestId": "request-1", "userSid": "S-1-5-21-1"},
        ],
    }

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtCampaignTriggerSuccessResponse)
    assert value.requests[0].requestId == "request-1"


def test_error_response_parses_campaign_error(mocker: object) -> None:
    """Campaigns error response parses documented error schema."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/euf/campaign/trigger"
    response.status_code = HTTPStatus.BAD_REQUEST
    response.json.return_value = {"code": "INVALID_REQUEST", "message": "Invalid request"}

    value = NxtResponse().from_response(response)

    assert isinstance(value, NxtCampaignTriggerErrorResponse)
    assert value.code == "INVALID_REQUEST"


def test_unauthorized_response_returns_invalid_token(mocker: object) -> None:
    """Campaigns 401 response keeps the existing invalid token model."""
    response = mocker.Mock()
    response.url = "https://tenant.api.eu.nexthink.cloud/api/v1/euf/campaign/trigger"
    response.status_code = HTTPStatus.UNAUTHORIZED

    assert isinstance(NxtResponse().from_response(response), NxtInvalidTokenRequest)
