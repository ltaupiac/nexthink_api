"""Unit tests for the internal HTTP transport."""

from nexthink_api.Clients.nxt_http_transport import NxtHttpTransport


def test_build_url_joins_base_url_and_endpoint_path() -> None:
    """Transport builds absolute URLs from API endpoint paths."""
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud")

    assert transport.build_url("/api/v1/token") == "https://tenant.api.eu.nexthink.cloud/api/v1/token"


def test_get_executes_session_request_with_default_contract(mocker: object) -> None:
    """GET forwards headers, params, proxies and the default timeout."""
    proxies = {"https": "http://proxy.example:8080"}
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud", proxies=proxies)
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = transport.get(
        "/api/v1/enrichment/data/fields",
        headers={"Authorization": "Bearer token"},
        params={"device": "abc"},
    )

    assert value is response
    request.assert_called_once_with(
        "GET",
        "https://tenant.api.eu.nexthink.cloud/api/v1/enrichment/data/fields",
        headers={"Authorization": "Bearer token"},
        params={"device": "abc"},
        proxies=proxies,
        timeout=300,
    )
    assert "verify" not in request.call_args.kwargs
    assert "cert" not in request.call_args.kwargs


def test_post_executes_session_request_with_json_payload(mocker: object) -> None:
    """POST forwards headers, JSON payload, proxies and the default timeout."""
    proxies = {"https": "http://proxy.example:8080"}
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud", proxies=proxies)
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = transport.post(
        "/api/v1/data-management/device/deletions",
        headers={"Authorization": "Bearer token"},
        json={"devices": [{"uid": "device-uid"}]},
    )

    assert value is response
    request.assert_called_once_with(
        "POST",
        "https://tenant.api.eu.nexthink.cloud/api/v1/data-management/device/deletions",
        headers={"Authorization": "Bearer token"},
        json={"devices": [{"uid": "device-uid"}]},
        proxies=proxies,
        timeout=300,
    )


def test_post_merges_extra_headers_without_mutating_base_headers(mocker: object) -> None:
    """POST merges per-call headers while keeping the caller-owned headers unchanged."""
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud")
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)
    headers = {"Authorization": "Bearer token"}
    extra_headers = {"x-request-id": "request-id"}

    value = transport.post(
        "/api/v1/data-management/device/deletions",
        headers=headers,
        extra_headers=extra_headers,
        json={"devices": []},
    )

    assert value is response
    request.assert_called_once_with(
        "POST",
        "https://tenant.api.eu.nexthink.cloud/api/v1/data-management/device/deletions",
        headers={
            "Authorization": "Bearer token",
            "x-request-id": "request-id",
        },
        json={"devices": []},
        proxies=None,
        timeout=300,
    )
    assert headers == {"Authorization": "Bearer token"}
    assert extra_headers == {"x-request-id": "request-id"}


def test_get_url_executes_session_request_against_absolute_url_with_override_timeout(mocker: object) -> None:
    """GET URL supports raw downloads where the URL is not relative to the tenant base URL."""
    proxies = {"https": "http://proxy.example:8080"}
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud", proxies=proxies)
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = transport.get_url("https://download.example/export.csv", timeout=42)

    assert value is response
    request.assert_called_once_with(
        "GET",
        "https://download.example/export.csv",
        proxies=proxies,
        timeout=42,
    )


def test_post_url_executes_session_request_against_absolute_url_with_form_data(mocker: object) -> None:
    """POST URL supports auth calls where the URL is not relative to the API base URL."""
    proxies = {"https": "http://proxy.example:8080"}
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud", proxies=proxies)
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = transport.post_url(
        "https://tenant-login.eu.nexthink.cloud/oauth2/default/v1/token",
        headers={"Authorization": "Basic token"},
        data={"grant_type": "client_credentials"},
    )

    assert value is response
    request.assert_called_once_with(
        "POST",
        "https://tenant-login.eu.nexthink.cloud/oauth2/default/v1/token",
        headers={"Authorization": "Basic token"},
        data={"grant_type": "client_credentials"},
        proxies=proxies,
        timeout=300,
    )


def test_transport_can_pass_explicit_tls_request_options(mocker: object) -> None:
    """Explicit TLS options are supported without making truststore injection implicit."""
    transport = NxtHttpTransport(
        "https://tenant.api.eu.nexthink.cloud",
        verify="/path/to/corporate-ca.pem",
        cert=("/path/to/client-cert.pem", "/path/to/client-key.pem"),
    )
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = transport.get("/api/v1/token")

    assert value is response
    request.assert_called_once_with(
        "GET",
        "https://tenant.api.eu.nexthink.cloud/api/v1/token",
        proxies=None,
        timeout=300,
        verify="/path/to/corporate-ca.pem",
        cert=("/path/to/client-cert.pem", "/path/to/client-key.pem"),
    )


def test_transport_mounts_truststore_adapter_when_ssl_context_is_enabled(mocker: object) -> None:
    """Transport scopes truststore through a dedicated requests adapter."""
    ssl_context = mocker.Mock()
    adapter = mocker.Mock()
    mocker.patch("nexthink_api.Clients.nxt_http_transport._nxt_ssl_context", return_value=ssl_context)
    adapter_class = mocker.patch("nexthink_api.Clients.nxt_http_transport.NxtTruststoreHttpAdapter", return_value=adapter)
    mount = mocker.patch("requests.sessions.Session.mount")
    transport = NxtHttpTransport("https://tenant.api.eu.nexthink.cloud")
    response = mocker.Mock()
    request = mocker.patch("requests.sessions.Session.request", return_value=response)

    value = transport.get("/api/v1/token")

    assert value is response
    adapter_class.assert_called_once_with(ssl_context)
    mount.assert_any_call("https://", adapter)
    request.assert_called_once()
