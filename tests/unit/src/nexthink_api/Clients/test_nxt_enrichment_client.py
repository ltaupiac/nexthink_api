"""Unit tests for the internal Enrichment client helpers."""

import pytest

from nexthink_api import NxtEndpoint
from nexthink_api.Clients.nxt_enrichment_client import NxtEnrichmentClient


def test_run_enrichment_posts_request(mocker: object) -> None:
    """Enrichment execution validates POST support, updates headers and delegates POST."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = True
    api_client.post.return_value = object()
    request = mocker.Mock()
    client = NxtEnrichmentClient(api_client)

    value = client.run_enrichment(NxtEndpoint.Enrichment, request)

    assert value is api_client.post.return_value
    api_client.check_method.assert_called_once_with(NxtEndpoint.Enrichment, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Enrichment)
    api_client.post.assert_called_once_with(NxtEndpoint.Enrichment, request)


def test_run_uses_enrichment_endpoint(mocker: object) -> None:
    """Short Enrichment operation owns its endpoint."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = True
    api_client.post.return_value = object()
    request = mocker.Mock()
    client = NxtEnrichmentClient(api_client)

    value = client.run(request)

    assert value is api_client.post.return_value
    api_client.check_method.assert_called_once_with(NxtEndpoint.Enrichment, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Enrichment)
    api_client.post.assert_called_once_with(NxtEndpoint.Enrichment, request)


def test_run_enrichment_rejects_unsupported_post_method(mocker: object) -> None:
    """Enrichment execution fails before sending HTTP when POST is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    request = mocker.Mock()
    client = NxtEnrichmentClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.run_enrichment(NxtEndpoint.Enrichment, request)

    api_client.update_header.assert_not_called()
    api_client.post.assert_not_called()
