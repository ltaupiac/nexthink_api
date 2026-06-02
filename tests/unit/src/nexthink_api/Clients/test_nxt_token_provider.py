"""Unit tests for the internal OAuth token provider."""

import base64

import pytest
import requests

from nexthink_api import NxtRegionName
from nexthink_api.Clients.nxt_http_transport import NxtHttpTransport
from nexthink_api.Exceptions.nxt_api_exception import NxtApiException
from nexthink_api.Clients.nxt_token_provider import NxtTokenProvider
from nexthink_api.Exceptions.nxt_token_exception import NxtTokenException
from nexthink_api.Models.nxt_settings import NxtSettings
from nexthink_api.Models.nxt_token_response import NxtTokenResponse

TOKEN_NOW = 1000.0
EXPECTED_EXPIRES_AT = 1900.0


def _provider() -> NxtTokenProvider:
    """Return a token provider with deterministic settings."""
    settings = NxtSettings(instance="tenant", region=NxtRegionName.eu, proxies=False)
    transport = NxtHttpTransport(str(settings.infinity_base_uri), proxies=settings.proxies)
    return NxtTokenProvider(
        settings=settings,
        transport=transport,
        client_id="client-id",
        client_secret="client-secret",
        now=lambda: TOKEN_NOW,
    )


def test_basic_auth_headers_match_official_oauth_contract() -> None:
    """Provider builds Basic auth and form content headers."""
    provider = _provider()
    expected_credentials = base64.b64encode(b"client-id:client-secret").decode()

    assert provider.basic_auth_headers() == {
        "Authorization": f"Basic {expected_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }


def test_request_token_posts_form_payload_to_login_endpoint(mocker: object) -> None:
    """Provider posts OAuth form data to the login token endpoint."""
    provider = _provider()
    response = mocker.Mock()
    response.status_code = 200
    parsed_token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="access-token",
        scope="service:integration",
    )
    provider.transport = mocker.Mock()
    provider.transport.post_url.return_value = response
    build_token = mocker.patch(
        "nexthink_api.Clients.nxt_token_provider.NxtResponse.build_nxt_token_response",
        return_value=parsed_token,
    )

    assert provider.request_token() == parsed_token
    provider.transport.post_url.assert_called_once_with(
        "https://tenant-login.eu.nexthink.cloud/oauth2/default/v1/token",
        headers=provider.basic_auth_headers(),
        data={
            "grant_type": "client_credentials",
            "scope": "service:integration",
        },
    )
    build_token.assert_called_once_with(response=response)
    assert provider.token == parsed_token
    assert provider.expires_at == EXPECTED_EXPIRES_AT


def test_get_token_reuses_cached_token_before_refresh_margin() -> None:
    """Provider reuses cached tokens that are not close to expiration."""
    provider = _provider()
    token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="cached-token",
        scope="service:integration",
    )
    provider.token = token
    provider.expires_at = 1200.0

    assert provider.get_token() == token


def test_get_token_refreshes_when_token_is_close_to_expiration(mocker: object) -> None:
    """Provider refreshes cached tokens inside the refresh margin."""
    provider = _provider()
    provider.token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="old-token",
        scope="service:integration",
    )
    provider.expires_at = 1059.0
    new_token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="new-token",
        scope="service:integration",
    )
    request_token = mocker.patch.object(provider, "request_token", return_value=new_token)

    assert provider.get_token() == new_token
    request_token.assert_called_once_with()


def test_authorization_header_returns_bearer_value(mocker: object) -> None:
    """Provider exposes a bearer authorization header value."""
    provider = _provider()
    token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="access-token",
        scope="service:integration",
    )
    mocker.patch.object(provider, "get_token", return_value=token)

    assert provider.authorization_header() == "Bearer access-token"


def test_request_token_wraps_http_errors(mocker: object) -> None:
    """HTTP status errors remain explicit token exceptions."""
    provider = _provider()
    provider.transport = mocker.Mock()
    provider.transport.post_url.side_effect = requests.exceptions.HTTPError("boom")

    with pytest.raises(NxtTokenException, match="Error during token retrieval"):
        provider.request_token()


def test_request_token_keeps_non_http_transport_errors(mocker: object) -> None:
    """Non-HTTP transport failures are not swallowed or converted into None."""
    provider = _provider()
    provider.transport = mocker.Mock()
    provider.transport.post_url.side_effect = requests.exceptions.ConnectionError("network down")

    with pytest.raises(requests.exceptions.ConnectionError, match="network down"):
        provider.request_token()


def test_request_token_rejects_non_json_body(mocker: object) -> None:
    """Token JSON responses reject non-JSON bodies with context."""
    provider = _provider()
    response = mocker.Mock()
    response.status_code = 200
    response.text = "<html>proxy error</html>"
    response.json.side_effect = ValueError("Invalid JSON")
    provider.transport = mocker.Mock()
    provider.transport.post_url.return_value = response

    with pytest.raises(NxtApiException) as error:
        provider.request_token()

    message = str(error.value)
    assert "Token response body is not valid JSON" in message
    assert "status_code=200" in message
    assert "<html>proxy error</html>" in message
