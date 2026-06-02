"""Unit tests for Campaigns public package exports."""

import nexthink_api
from nexthink_api.Campaigns import (
    NxtCampaignTriggerErrorResponse,
    NxtCampaignTriggerRequest,
    NxtCampaignTriggerResponseDetails,
    NxtCampaignTriggerSuccessResponse,
)


def test_campaigns_models_are_exported_from_domain_package() -> None:
    """Campaigns models are importable from the domain package."""
    assert NxtCampaignTriggerErrorResponse.__name__ == "NxtCampaignTriggerErrorResponse"
    assert NxtCampaignTriggerRequest.__name__ == "NxtCampaignTriggerRequest"
    assert NxtCampaignTriggerResponseDetails.__name__ == "NxtCampaignTriggerResponseDetails"
    assert NxtCampaignTriggerSuccessResponse.__name__ == "NxtCampaignTriggerSuccessResponse"


def test_campaigns_models_are_exported_from_root_package() -> None:
    """Campaigns models are available from the historical root package."""
    assert nexthink_api.NxtCampaignTriggerErrorResponse is NxtCampaignTriggerErrorResponse
    assert nexthink_api.NxtCampaignTriggerRequest is NxtCampaignTriggerRequest
    assert nexthink_api.NxtCampaignTriggerResponseDetails is NxtCampaignTriggerResponseDetails
    assert nexthink_api.NxtCampaignTriggerSuccessResponse is NxtCampaignTriggerSuccessResponse
