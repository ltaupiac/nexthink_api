"""Unit tests for Nexthink client settings."""

import pytest

from nexthink_api import NxtRegionName, NxtSettings


def test_settings_build_api_and_login_urls() -> None:
    """Settings separate API base URL from OAuth login token URL."""
    settings = NxtSettings(instance="tenant", region=NxtRegionName.eu, proxies=False)

    assert str(settings.infinity_base_uri) == "https://tenant.api.eu.nexthink.cloud/"
    assert str(settings.token_url) == "https://tenant-login.eu.nexthink.cloud/oauth2/default/v1/token"


@pytest.mark.parametrize("region", list(NxtRegionName))
def test_settings_build_login_token_url_per_region(region: NxtRegionName) -> None:
    """Settings build the official OAuth login token URL for every region."""
    settings = NxtSettings(instance="tenant", region=region, proxies=False)

    assert str(settings.token_url) == f"https://tenant-login.{region.value}.nexthink.cloud/oauth2/default/v1/token"


def test_settings_build_urls_when_region_is_raw_string() -> None:
    """Settings build URLs before Pydantic coerces raw string regions."""
    settings = NxtSettings(instance="tenant", region="eu", proxies=False)

    assert settings.region == NxtRegionName.eu
    assert str(settings.infinity_base_uri) == "https://tenant.api.eu.nexthink.cloud/"
    assert str(settings.token_url) == "https://tenant-login.eu.nexthink.cloud/oauth2/default/v1/token"
