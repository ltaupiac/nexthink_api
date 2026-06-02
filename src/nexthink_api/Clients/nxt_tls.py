"""Explicit TLS helpers for corporate proxy environments."""

import ssl

__all__ = ["enable_truststore", "is_truststore_enabled"]

_truststore_enabled = False


def enable_truststore() -> None:
    """Enable OS trust store usage for Nexthink HTTP calls.

    This is useful when a corporate proxy performs TLS inspection and its CA is
    trusted by the operating system but not by certifi.

    The function only toggles an internal flag. Nexthink HTTP transports create
    request-local truststore SSL contexts without monkey patching Python SSL.
    """
    _load_truststore()
    global _truststore_enabled  # noqa: PLW0603 - public opt-in flag by design.
    _truststore_enabled = True


def is_truststore_enabled() -> bool:
    """Return whether Nexthink HTTP calls should use the OS trust store."""
    return _truststore_enabled


def _nxt_ssl_context() -> ssl.SSLContext | None:
    """Return a truststore SSL context for Nexthink HTTP requests when enabled."""
    if not _truststore_enabled:
        return None

    truststore = _load_truststore()
    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _load_truststore() -> object:
    """Import truststore lazily so package import does not alter TLS behavior."""
    try:
        import truststore  # noqa: PLC0415
    except ModuleNotFoundError as exc:
        msg = "truststore is not installed. Run: pip install truststore"
        raise ModuleNotFoundError(msg) from exc
    return truststore
