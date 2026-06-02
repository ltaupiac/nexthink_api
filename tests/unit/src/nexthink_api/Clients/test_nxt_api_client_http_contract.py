"""Characterization tests for the current NxtApiClient HTTP contract."""

from http import HTTPStatus

import pytest

from nexthink_api import (
    NxtApiClient,
    NxtEndpoint,
    NxtLegacyApiWarning,
    NxtNqlApiExportResponse,
    NxtNqlApiStatusResponse,
    NxtNqlStatus,
    NxtRegionName,
    NxtTokenResponse,
)
from nexthink_api.Clients.nxt_http_transport import NxtHttpTransport


def _legacy_client(*args: object, **kwargs: object) -> NxtApiClient:
    """Create the historical facade while asserting its deprecation warning."""
    with pytest.warns(NxtLegacyApiWarning, match="`NxtApiClient` is deprecated"):
        return NxtApiClient(*args, **kwargs)


def _legacy_call(callable_object: object, *args: object, **kwargs: object) -> object:
    """Call a legacy facade method while asserting its deprecation warning."""
    with pytest.warns(NxtLegacyApiWarning, match="is deprecated"):
        return callable_object(*args, **kwargs)


def _client_without_token(mocker: object, proxies: dict[str, str] | None = None) -> NxtApiClient:
    mocker.patch.object(NxtApiClient, "init_token", return_value=None)
    client = _legacy_client(
        "tenant",
        NxtRegionName.eu,
        client_id="client-id",
        client_secret="client-secret",
        proxies=proxies,
    )
    client.headers = {
        "Authorization": "Bearer token",
        "Content-Type": "application/json",
        "Accept": "application/json, text/csv",
    }
    return client


def _response(mocker: object, endpoint: NxtEndpoint, status_code: int = HTTPStatus.OK) -> object:
    response = mocker.Mock()
    response.status_code = status_code
    response.url = endpoint.value
    return response


def test_client_initializes_transport_with_http_settings(mocker: object) -> None:
    """Client owns a transport configured from tenant base URL, proxies and timeout."""
    proxies = {"https": "http://proxy.example:8080"}
    mocker.patch.object(NxtApiClient, "init_token", return_value=None)

    client = _legacy_client(
        "tenant",
        NxtRegionName.eu,
        client_id="client-id",
        client_secret="client-secret",
        proxies=proxies,
    )

    assert isinstance(client.transport, NxtHttpTransport)
    assert client.transport.base_url == "https://tenant.api.eu.nexthink.cloud/"
    assert client.transport.proxies == proxies
    assert client.transport.timeout == 300


def test_get_delegates_endpoint_headers_and_params_to_transport(mocker: object) -> None:
    """Generic GET delegates endpoint path, headers and query params to the transport."""
    client = _client_without_token(mocker)
    response = _response(mocker, NxtEndpoint.Enrichment)
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_api_client.NxtResponse.from_response", return_value=parsed_response)
    client.transport = mocker.Mock()
    client.transport.get.return_value = response

    value = client.get(NxtEndpoint.Enrichment, params={"device": "abc"})

    assert value is parsed_response
    client.transport.get.assert_called_once_with(
        NxtEndpoint.Enrichment.value,
        headers=client.headers,
        params={"device": "abc"},
    )


def test_post_delegates_payload_and_per_call_headers_to_transport(mocker: object) -> None:
    """Generic POST keeps base headers and per-call headers separate for the transport."""
    client = _client_without_token(mocker)
    response = _response(mocker, NxtEndpoint.DataManagement, status_code=HTTPStatus.ACCEPTED)
    parsed_response = object()
    request = mocker.Mock()
    request.model_dump.return_value = {"devices": [{"uid": "device-uid"}]}
    mocker.patch("nexthink_api.Clients.nxt_api_client.NxtResponse.from_response", return_value=parsed_response)
    client.transport = mocker.Mock()
    client.transport.post.return_value = response

    value = client.post(
        NxtEndpoint.DataManagement,
        request,
        headers={"x-request-id": "request-id"},
    )

    assert value is parsed_response
    client.transport.post.assert_called_once_with(
        NxtEndpoint.DataManagement.value,
        headers=client.headers,
        extra_headers={"x-request-id": "request-id"},
        json={"devices": [{"uid": "device-uid"}]},
    )


def test_get_bearer_token_delegates_to_token_provider(mocker: object) -> None:
    """Token retrieval delegates OAuth details to the token provider."""
    client = _client_without_token(mocker)
    parsed_token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="access-token",
        scope="service:integration",
    )
    client.token_provider = mocker.Mock()
    client.token_provider.get_token.return_value = parsed_token

    assert client.get_bearer_token() is True
    assert client.token is parsed_token
    client.token_provider.get_token.assert_called_once_with()


def test_get_status_export_delegates_status_path_and_headers_to_transport(mocker: object) -> None:
    """NQL status polling delegates the relative status path and headers to the transport."""
    client = _client_without_token(mocker)
    response = _response(mocker, NxtEndpoint.NqlStatus)
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_api_client.NxtResponse.from_response", return_value=parsed_response)
    client.transport = mocker.Mock()
    client.transport.get.return_value = response

    value = _legacy_call(client.get_status_export, NxtNqlApiExportResponse(exportId="export-123"))

    assert value is parsed_response
    client.transport.get.assert_called_once_with(
        "/api/v1/nql/status/export-123",
        headers=client.headers,
    )


def test_download_export_delegates_absolute_url_and_timeout_to_transport(mocker: object) -> None:
    """Raw export download delegates the absolute result URL and caller timeout to the transport."""
    client = _client_without_token(mocker)
    raw_response = mocker.Mock()
    client.transport = mocker.Mock()
    client.transport.get_url.return_value = raw_response
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    value = _legacy_call(client.download_export, status, timeout=42)

    assert value is raw_response
    client.transport.get_url.assert_called_once_with(
        str(status.resultsFileUrl),
        timeout=42,
    )


def test_check_method_delegates_to_static_spec_registry(mocker: object) -> None:
    """Method checks use the static registry instead of parsing runtime YAML files."""
    client = _client_without_token(mocker)
    supports_method = mocker.patch(
        "nexthink_api.Clients.nxt_api_client.SpecRegistry.supports_method",
        return_value=True,
    )

    assert client.check_method(NxtEndpoint.DataManagement, "POST") is True
    supports_method.assert_called_once_with(NxtEndpoint.DataManagement, "POST")


def test_get_bearer_token_posts_token_payload_with_current_http_contract(mocker: object) -> None:
    """Token bootstrap posts OAuth form data to the login endpoint."""
    proxies = {"https": "http://proxy.example:8080"}
    mocker.patch.object(NxtApiClient, "init_token", return_value=None)
    client = _legacy_client(
        "tenant",
        NxtRegionName.eu,
        client_id="client-id",
        client_secret="client-secret",
        proxies=proxies,
    )
    token_response = _response(mocker, NxtEndpoint.Token)
    parsed_token = NxtTokenResponse(
        token_type="Bearer",
        expires_in=900,
        access_token="access-token",
        scope="service:integration",
    )
    mocker.patch("nexthink_api.Clients.nxt_token_provider.NxtResponse.build_nxt_token_response", return_value=parsed_token)
    post = mocker.patch("requests.sessions.Session.request", return_value=token_response)

    assert client.get_bearer_token() is True
    assert client.token is parsed_token
    post.assert_called_once_with(
        "POST",
        "https://tenant-login.eu.nexthink.cloud/oauth2/default/v1/token",
        headers={
            "Authorization": "Basic Y2xpZW50LWlkOmNsaWVudC1zZWNyZXQ=",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={
            "grant_type": "client_credentials",
            "scope": "service:integration",
        },
        proxies=proxies,
        timeout=300,
    )
    assert "verify" not in post.call_args.kwargs
    assert "cert" not in post.call_args.kwargs


def test_get_sends_url_headers_params_proxies_and_timeout(mocker: object) -> None:
    """Generic GET forwards the current headers, query params, proxies and timeout."""
    proxies = {"https": "http://proxy.example:8080"}
    client = _client_without_token(mocker, proxies=proxies)
    response = _response(mocker, NxtEndpoint.Enrichment)
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_nql_client.NxtResponse.from_response", return_value=parsed_response)
    get = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = client.get(NxtEndpoint.Enrichment, params={"device": "abc"})

    assert value is parsed_response
    get.assert_called_once_with(
        "GET",
        "https://tenant.api.eu.nexthink.cloud/api/v1/enrichment/data/fields",
        headers=client.headers,
        params={"device": "abc"},
        proxies=proxies,
        timeout=300,
    )
    assert "verify" not in get.call_args.kwargs
    assert "cert" not in get.call_args.kwargs


def test_post_sends_merged_headers_json_payload_proxies_and_timeout(mocker: object) -> None:
    """Generic POST merges per-call headers without mutating the client headers."""
    proxies = {"https": "http://proxy.example:8080"}
    client = _client_without_token(mocker, proxies=proxies)
    response = _response(mocker, NxtEndpoint.DataManagement, status_code=HTTPStatus.ACCEPTED)
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_nql_client.NxtResponse.from_response", return_value=parsed_response)
    post = mocker.patch("requests.sessions.Session.request", return_value=response)
    request = mocker.Mock()
    request.model_dump.return_value = {"devices": [{"uid": "device-uid"}]}

    value = client.post(
        NxtEndpoint.DataManagement,
        request,
        headers={"x-request-id": "request-id"},
    )

    assert value is parsed_response
    post.assert_called_once_with(
        "POST",
        "https://tenant.api.eu.nexthink.cloud/api/v1/data-management/device/deletions",
        headers={
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
            "Accept": "application/json, text/csv",
            "x-request-id": "request-id",
        },
        json={"devices": [{"uid": "device-uid"}]},
        proxies=proxies,
        timeout=300,
    )
    assert client.headers == {
        "Authorization": "Bearer token",
        "Content-Type": "application/json",
        "Accept": "application/json, text/csv",
    }
    assert "verify" not in post.call_args.kwargs
    assert "cert" not in post.call_args.kwargs


def test_get_status_export_sends_nql_status_url_headers_proxies_and_timeout(mocker: object) -> None:
    """NQL status polling appends the export id and parses the raw response."""
    proxies = {"https": "http://proxy.example:8080"}
    client = _client_without_token(mocker, proxies=proxies)
    response = _response(mocker, NxtEndpoint.NqlStatus)
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_api_client.NxtResponse.from_response", return_value=parsed_response)
    get = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = _legacy_call(client.get_status_export, NxtNqlApiExportResponse(exportId="export-123"))

    assert value is parsed_response
    get.assert_called_once_with(
        "GET",
        "https://tenant.api.eu.nexthink.cloud/api/v1/nql/status/export-123",
        headers=client.headers,
        proxies=proxies,
        timeout=300,
    )


def test_download_export_returns_raw_response_with_results_url_proxies_and_timeout(mocker: object) -> None:
    """NQL export download returns the raw requests.Response and sends no explicit headers."""
    proxies = {"https": "http://proxy.example:8080"}
    client = _client_without_token(mocker, proxies=proxies)
    raw_response = mocker.Mock()
    get = mocker.patch("requests.sessions.Session.request", return_value=raw_response)
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    value = _legacy_call(client.download_export, status, timeout=42)

    assert value is raw_response
    get.assert_called_once_with(
        "GET",
        str(status.resultsFileUrl),
        proxies=proxies,
        timeout=42,
    )
    assert "headers" not in get.call_args.kwargs
    assert "verify" not in get.call_args.kwargs
    assert "cert" not in get.call_args.kwargs
