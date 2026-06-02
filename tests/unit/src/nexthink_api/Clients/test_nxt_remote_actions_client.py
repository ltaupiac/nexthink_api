"""Unit tests for the internal Remote Actions client."""

import pytest

from nexthink_api import NxtEndpoint, NxtRemoteActionExecutionRequest
from nexthink_api.Clients.nxt_remote_actions_client import NxtRemoteActionsClient


def _request() -> NxtRemoteActionExecutionRequest:
    """Return a minimal valid Remote Actions execution request."""
    return NxtRemoteActionExecutionRequest(remoteActionId="#restart_service", devices=["collector-1"])


def test_execute_posts_remote_action_request(mocker: object) -> None:
    """Remote Actions execution validates POST support and delegates transport POST."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.post.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_remote_actions_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtRemoteActionsClient(api_client)

    value = client.execute(_request())

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.Act, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Act)
    api_client.transport.post.assert_called_once_with(
        "/api/v1/act/execute",
        headers=api_client.headers,
        json={"remoteActionId": "#restart_service", "devices": ["collector-1"]},
    )


def test_execute_rejects_unsupported_post_method(mocker: object) -> None:
    """Remote Actions execution fails before sending HTTP when POST is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    client = NxtRemoteActionsClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.execute(_request())

    api_client.transport.post.assert_not_called()


def test_list_gets_remote_actions(mocker: object) -> None:
    """Remote Actions list operation owns the list endpoint."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.get.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_remote_actions_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtRemoteActionsClient(api_client)

    value = client.list()

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.RemoteActions, "GET")
    api_client.update_header.assert_called_once_with(NxtEndpoint.RemoteActions)
    api_client.transport.get.assert_called_once_with(
        "/api/v1/act/remote-action",
        headers=api_client.headers,
    )


def test_get_fetches_remote_action_details_by_nql_id(mocker: object) -> None:
    """Remote Actions get operation sends the documented nql-id query parameter."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.get.return_value = object()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_remote_actions_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtRemoteActionsClient(api_client)

    value = client.get("#restart_service")

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.RemoteActionsDetails, "GET")
    api_client.update_header.assert_called_once_with(NxtEndpoint.RemoteActionsDetails)
    api_client.transport.get.assert_called_once_with(
        "/api/v1/act/remote-action/details",
        headers=api_client.headers,
        params={"nql-id": "#restart_service"},
    )
