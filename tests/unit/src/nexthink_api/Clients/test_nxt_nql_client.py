"""Unit tests for the internal NQL client helpers."""

from http import HTTPStatus

import pytest

from nexthink_api import (
    NxtEndpoint,
    NxtNqlApiExecuteRequest,
    NxtNqlApiExportResponse,
    NxtNqlApiStatusResponse,
    NxtNqlStatus,
)
from nexthink_api.Clients.nxt_nql_client import NxtNqlClient
from nexthink_api.Exceptions.nxt_export_exception import NxtExportException
from nexthink_api.Exceptions.nxt_status_exception import NxtStatusException
from nexthink_api.Exceptions.nxt_timeout_exception import NxtStatusTimeoutException
from nexthink_api.Nql.nxt_error_response import NxtErrorResponse

EXPECTED_STATUS_POLLS = 2


def _request() -> NxtNqlApiExecuteRequest:
    """Return a minimal valid NQL execute request."""
    return NxtNqlApiExecuteRequest(queryId="#query", parameters={})


def test_run_nql_posts_by_default(mocker: object) -> None:
    """NQL execution validates POST support, updates headers and delegates POST."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = True
    api_client.post.return_value = object()
    client = NxtNqlClient(api_client)

    value = client.run_nql(NxtEndpoint.Nql, _request())

    assert value is api_client.post.return_value
    api_client.check_method.assert_called_once_with(NxtEndpoint.Nql, "POST")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Nql)
    api_client.post.assert_called_once_with(NxtEndpoint.Nql, _request())
    api_client.get.assert_not_called()


def test_execute_defaults_to_nql_v2(mocker: object) -> None:
    """Explicit NQL execute operation defaults to the v2 endpoint."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    run_nql = mocker.patch.object(client, "run_nql", return_value=object())

    value = client.execute(_request())

    assert value is run_nql.return_value
    run_nql.assert_called_once_with(NxtEndpoint.NqlV2, _request())


def test_execute_accepts_nql_v1(mocker: object) -> None:
    """Explicit NQL execute operation keeps v1 available."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    run_nql = mocker.patch.object(client, "run_nql", return_value=object())

    value = client.execute(_request(), version="v1")

    assert value is run_nql.return_value
    run_nql.assert_called_once_with(NxtEndpoint.Nql, _request())


def test_execute_rejects_unknown_version(mocker: object) -> None:
    """Explicit NQL execute operation rejects unsupported versions."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)

    with pytest.raises(ValueError, match="Unsupported NQL execute version"):
        client.execute(_request(), version="v3")


def test_export_uses_nql_export_endpoint(mocker: object) -> None:
    """Explicit NQL export operation owns the export endpoint."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    run_nql = mocker.patch.object(client, "run_nql", return_value=object())

    value = client.export(_request())

    assert value is run_nql.return_value
    run_nql.assert_called_once_with(NxtEndpoint.NqlExport, _request())


def test_run_nql_get_delegates_to_facade_get(mocker: object) -> None:
    """NQL execution keeps the historical GET branch."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = True
    api_client.get.return_value = object()
    client = NxtNqlClient(api_client)

    value = client.run_nql(NxtEndpoint.Nql, _request(), method="GET")

    assert value is api_client.get.return_value
    api_client.check_method.assert_called_once_with(NxtEndpoint.Nql, "GET")
    api_client.update_header.assert_called_once_with(NxtEndpoint.Nql)
    api_client.get.assert_called_once_with(NxtEndpoint.Nql, _request())
    api_client.post.assert_not_called()


def test_run_nql_rejects_unsupported_method(mocker: object) -> None:
    """NQL execution fails before sending HTTP when the method is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    client = NxtNqlClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.run_nql(NxtEndpoint.Nql, _request())

    api_client.update_header.assert_not_called()
    api_client.post.assert_not_called()
    api_client.get.assert_not_called()


def test_get_status_export_delegates_status_path_and_headers(mocker: object) -> None:
    """NQL status polling builds the export status path and parses the response."""
    api_client = mocker.Mock()
    api_client.headers = {"Authorization": "Bearer token"}
    api_client.check_method.return_value = True
    api_client.transport.get.return_value = mocker.Mock()
    parsed_response = object()
    mocker.patch("nexthink_api.Clients.nxt_nql_client.NxtResponse.from_response", return_value=parsed_response)
    client = NxtNqlClient(api_client)

    value = client.get_status_export(NxtNqlApiExportResponse(exportId="export-123"))

    assert value is parsed_response
    api_client.check_method.assert_called_once_with(NxtEndpoint.NqlStatus, "GET")
    api_client.update_header.assert_called_once_with(NxtEndpoint.NqlStatus)
    api_client.transport.get.assert_called_once_with(
        "/api/v1/nql/status/export-123",
        headers=api_client.headers,
    )


def test_get_status_export_rejects_unsupported_get_method(mocker: object) -> None:
    """NQL status polling fails before sending HTTP when GET is unsupported."""
    api_client = mocker.Mock()
    api_client.check_method.return_value = False
    client = NxtNqlClient(api_client)

    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.get_status_export(NxtNqlApiExportResponse(exportId="export-123"))

    api_client.check_method.assert_called_once_with(NxtEndpoint.NqlStatus, "GET")
    api_client.update_header.assert_not_called()
    api_client.transport.get.assert_not_called()


def test_wait_status_polls_until_completed(mocker: object) -> None:
    """NQL status polling repeats until the export is no longer in progress."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    in_progress = NxtNqlApiStatusResponse(status=NxtNqlStatus.IN_PROGRESS)
    completed = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )
    get_status = mocker.patch.object(client, "get_status_export", side_effect=[in_progress, completed])
    sleep = mocker.patch("nexthink_api.Clients.nxt_nql_client.time.sleep")

    value = client.wait_status(NxtNqlApiExportResponse(exportId="export-123"))

    assert value == completed
    assert get_status.call_count == EXPECTED_STATUS_POLLS
    assert sleep.call_args_list == [mocker.call(1), mocker.call(1)]


def test_wait_delegates_to_wait_status(mocker: object) -> None:
    """Explicit NQL wait operation keeps the existing polling behavior."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    export_response = NxtNqlApiExportResponse(exportId="export-123")
    wait_status = mocker.patch.object(client, "wait_status", return_value=object())

    value = client.wait(export_response, timeout=42)

    assert value is wait_status.return_value
    wait_status.assert_called_once_with(export_response, 42)


def test_wait_status_returns_error_response(mocker: object) -> None:
    """NQL status polling returns API errors without retrying."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    error = NxtErrorResponse(message="Invalid query", code=400)
    get_status = mocker.patch.object(client, "get_status_export", return_value=error)
    sleep = mocker.patch("nexthink_api.Clients.nxt_nql_client.time.sleep")

    value = client.wait_status(NxtNqlApiExportResponse(exportId="export-123"))

    assert value == error
    get_status.assert_called_once()
    sleep.assert_not_called()


def test_wait_status_raises_on_timeout(mocker: object) -> None:
    """NQL status polling keeps the historical timeout behavior."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    in_progress = NxtNqlApiStatusResponse(status=NxtNqlStatus.IN_PROGRESS)
    mocker.patch.object(client, "get_status_export", return_value=in_progress)
    mocker.patch("nexthink_api.Clients.nxt_nql_client.time.time", side_effect=[0, 301])

    with pytest.raises(NxtStatusTimeoutException, match="Status not completed before timeout"):
        client.wait_status(NxtNqlApiExportResponse(exportId="export-123"), timeout=300)


def test_download_export_delegates_completed_export_url(mocker: object) -> None:
    """NQL export download delegates the result URL to the facade transport."""
    api_client = mocker.Mock()
    api_client.transport.get_url.return_value = object()
    from_response = mocker.patch("nexthink_api.Clients.nxt_nql_client.NxtResponse.from_response")
    client = NxtNqlClient(api_client)
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    value = client.download_export(status, timeout=42)

    assert value is api_client.transport.get_url.return_value
    api_client.transport.get_url.assert_called_once_with(
        str(status.resultsFileUrl),
        timeout=42,
    )
    from_response.assert_not_called()


def test_download_delegates_to_download_export(mocker: object) -> None:
    """Explicit NQL download operation keeps the existing download behavior."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    download_export = mocker.patch.object(client, "download_export", return_value=object())
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    value = client.download(status, timeout=42)

    assert value is download_export.return_value
    download_export.assert_called_once_with(status, 42)


def test_download_export_rejects_unfinished_status(mocker: object) -> None:
    """NQL export download only accepts completed exports."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    status = NxtNqlApiStatusResponse(status=NxtNqlStatus.IN_PROGRESS)

    with pytest.raises(NxtStatusException, match="Try do download an export not completed"):
        client.download_export(status)

    api_client.transport.get_url.assert_not_called()


def test_download_export_as_df_parses_csv(mocker: object) -> None:
    """NQL CSV downloads are parsed into a dataframe."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    raw_response = mocker.Mock(status_code=HTTPStatus.OK, text="name,count\nalpha,1\n")
    mocker.patch.object(client, "download_export", return_value=raw_response)
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    value = client.download_export_as_df(status)

    assert value.to_dict(orient="records") == [{"name": "alpha", "count": 1}]


def test_download_dataframe_delegates_to_download_export_as_df(mocker: object) -> None:
    """Explicit NQL dataframe download operation keeps the existing dataframe behavior."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    download_export_as_df = mocker.patch.object(client, "download_export_as_df", return_value=object())
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    value = client.download_dataframe(status, timeout=42)

    assert value is download_export_as_df.return_value
    download_export_as_df.assert_called_once_with(status, 42)


def test_download_export_as_df_raises_on_non_ok_download(mocker: object) -> None:
    """NQL CSV downloads keep the historical non-200 error."""
    api_client = mocker.Mock()
    client = NxtNqlClient(api_client)
    raw_response = mocker.Mock(status_code=HTTPStatus.BAD_GATEWAY, text="")
    mocker.patch.object(client, "download_export", return_value=raw_response)
    status = NxtNqlApiStatusResponse(
        status=NxtNqlStatus.COMPLETED,
        resultsFileUrl="https://download.example/export.csv",
    )

    with pytest.raises(NxtExportException, match="Failed to download export:Status code 502"):
        client.download_export_as_df(status)
