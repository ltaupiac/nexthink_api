"""Unit tests for explicit TLS helpers."""

import ssl

import pytest

from nexthink_api import enable_truststore
from nexthink_api.Clients import nxt_tls


@pytest.fixture(autouse=True)
def reset_truststore_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep truststore opt-in state isolated between tests."""
    monkeypatch.setattr(nxt_tls, "_truststore_enabled", False)


def test_enable_truststore_sets_internal_flag_without_global_injection(mocker: object) -> None:
    """The public helper only enables Nexthink-scoped truststore usage."""
    inject_into_ssl = mocker.patch("truststore.inject_into_ssl")

    assert not nxt_tls.is_truststore_enabled()

    enable_truststore()

    assert nxt_tls.is_truststore_enabled()
    inject_into_ssl.assert_not_called()


def test_nxt_ssl_context_is_none_when_truststore_is_disabled(mocker: object) -> None:
    """Nexthink requests do not create a truststore SSL context by default."""
    inject_into_ssl = mocker.patch("truststore.inject_into_ssl")
    ssl_context = mocker.patch("truststore.SSLContext")

    assert nxt_tls._nxt_ssl_context() is None

    inject_into_ssl.assert_not_called()
    ssl_context.assert_not_called()


def test_nxt_ssl_context_returns_truststore_context_without_global_injection(mocker: object) -> None:
    """Enabled truststore returns a dedicated SSL context for the transport."""
    enable_truststore()
    inject_into_ssl = mocker.patch("truststore.inject_into_ssl")
    context = mocker.Mock()
    ssl_context = mocker.patch("truststore.SSLContext", return_value=context)

    assert nxt_tls._nxt_ssl_context() is context

    ssl_context.assert_called_once_with(ssl.PROTOCOL_TLS_CLIENT)
    inject_into_ssl.assert_not_called()
