"""Unit tests for Data Management client helpers."""

import logging
from http import HTTPStatus

import pytest

from nexthink_api import (
    NxtApiClient,
    NxtDataManagementBatchStatus,
    NxtDataManagementDeviceStatus,
    NxtDeviceDeletionRequest,
    NxtDeviceDeletionResponse,
    NxtDeviceEntry,
    NxtEndpoint,
    NxtLegacyApiWarning,
    NxtRegionName,
    NxtUidValidationMode,
)
from nexthink_api.Clients.nxt_data_management_client import NxtDataManagementClient


class TestNxtDataManagementClient:
    """Test Data Management client helper behavior."""

    @staticmethod
    def _client(mocker: object) -> NxtApiClient:
        mocker.patch.object(NxtApiClient, "init_token", return_value=None)
        with pytest.warns(NxtLegacyApiWarning, match="`NxtApiClient` is deprecated"):
            client = NxtApiClient(
                "tenant",
                NxtRegionName.eu,
                client_id="client-id",
                client_secret="client-secret",
            )
        client.headers = {"Authorization": "Bearer token"}
        return client

    @staticmethod
    def _legacy_call(callable_object: object, *args: object, **kwargs: object) -> object:
        """Call a legacy facade method while asserting its deprecation warning."""
        with pytest.warns(NxtLegacyApiWarning, match="delete_devices"):
            return callable_object(*args, **kwargs)

    @staticmethod
    def _device(uid: str = "11111111-1111-1111-1111-111111111111") -> NxtDeviceEntry:
        return NxtDeviceEntry(uid=uid, name="DEVICE-1")

    def test_internal_data_management_client_posts_request(self, mocker: object) -> None:
        """Internal Data Management client owns request construction behavior."""
        api_client = mocker.Mock()
        api_client.check_method.return_value = True
        api_client.post.return_value = object()
        client = NxtDataManagementClient(api_client)
        device = self._device()

        value = client.delete_devices(
            [device],
            request_id="22222222-2222-2222-2222-222222222222",
            uid_validation=NxtUidValidationMode.PERMISSIVE,
        )

        assert value is api_client.post.return_value
        api_client.check_method.assert_called_once_with(NxtEndpoint.DataManagement, "POST")
        api_client.update_header.assert_called_once_with(NxtEndpoint.DataManagement)
        endpoint, request = api_client.post.call_args.args
        assert endpoint == NxtEndpoint.DataManagement
        assert isinstance(request, NxtDeviceDeletionRequest)
        assert request.devices == [device]
        assert api_client.post.call_args.kwargs == {
            "headers": {"x-request-id": "22222222-2222-2222-2222-222222222222"},
        }

    def test_delete_devices_posts_data_management_request(self, mocker: object) -> None:
        """delete_devices posts a device deletion request."""
        client = self._client(mocker)
        mocker.patch.object(client, "check_method", return_value=True)
        mocker.patch.object(client, "update_header", return_value=None)
        response = object()
        post = mocker.patch.object(client, "post", return_value=response)

        value = self._legacy_call(
            client.delete_devices,
            [self._device()],
            uid_validation=NxtUidValidationMode.PERMISSIVE,
        )

        assert value is response
        endpoint, request = post.call_args.args
        assert endpoint == NxtEndpoint.DataManagement
        assert isinstance(request, NxtDeviceDeletionRequest)
        assert request.devices == [self._device()]
        assert post.call_args.kwargs == {"headers": None}

    def test_delete_devices_sends_request_id_as_call_header(self, mocker: object) -> None:
        """delete_devices sends x-request-id without mutating client headers."""
        client = self._client(mocker)
        mocker.patch.object(client, "check_method", return_value=True)
        mocker.patch.object(client, "update_header", return_value=None)
        post = mocker.patch.object(client, "post", return_value=object())

        self._legacy_call(
            client.delete_devices,
            [self._device()],
            request_id="22222222-2222-2222-2222-222222222222",
        )

        assert post.call_args.kwargs == {
            "headers": {"x-request-id": "22222222-2222-2222-2222-222222222222"},
        }
        assert "x-request-id" not in client.headers

    def test_delete_devices_serializes_payload_and_request_id_header(
            self,
            mocker: object,
    ) -> None:
        """delete_devices serializes payload and sends x-request-id to requests."""
        client = self._client(mocker)
        device = self._device()
        request_id = "22222222-2222-2222-2222-222222222222"
        mocker.patch.object(client, "check_method", return_value=True)
        post_response = mocker.Mock()
        post_response.status_code = HTTPStatus.ACCEPTED
        post_response.url = NxtEndpoint.DataManagement.value
        post_response.headers = {"x-request-id": request_id}
        post_response.json.return_value = {
            "scheduledCount": 1,
            "status": "ACCEPTED",
            "devices": [
                {
                    "uid": device.uid,
                    "name": device.name,
                    "status": "SCHEDULED",
                }
            ],
        }
        post = mocker.patch("requests.sessions.Session.request", return_value=post_response)

        value = self._legacy_call(client.delete_devices, [device], request_id=request_id)

        assert isinstance(value, NxtDeviceDeletionResponse)
        assert value.status == NxtDataManagementBatchStatus.ACCEPTED
        assert value.request_id == request_id
        assert value.devices[0].status == NxtDataManagementDeviceStatus.SCHEDULED
        post.assert_called_once_with(
            "POST",
            "https://tenant.api.eu.nexthink.cloud/api/v1/data-management/device/deletions",
            headers={
                "Authorization": "Bearer None",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "x-request-id": request_id,
            },
            json={
                "devices": [
                    {
                        "uid": device.uid,
                        "name": device.name,
                    }
                ]
            },
            proxies=client.settings.proxies,
            timeout=300,
        )
        assert "x-request-id" not in client.headers

    def test_delete_devices_rejects_unsupported_post_method(self, mocker: object) -> None:
        """delete_devices fails if POST is not available for the endpoint."""
        client = self._client(mocker)
        mocker.patch.object(client, "check_method", return_value=False)
        post = mocker.patch.object(client, "post")

        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            self._legacy_call(client.delete_devices, [self._device()])

        post.assert_not_called()

    def test_delete_devices_strict_uid_validation_raises(self, mocker: object) -> None:
        """STRICT UID validation fails before the API call."""
        client = self._client(mocker)
        mocker.patch.object(client, "check_method", return_value=True)
        post = mocker.patch.object(client, "post")

        with pytest.raises(ValueError, match="1 invalid UID"):
            self._legacy_call(
                client.delete_devices,
                [self._device("not-a-uuid")],
                uid_validation=NxtUidValidationMode.STRICT,
            )

        post.assert_not_called()

    def test_delete_devices_warn_uid_validation_logs_and_continues(
            self,
            mocker: object,
            caplog: pytest.LogCaptureFixture,
    ) -> None:
        """WARN UID validation logs malformed UIDs and continues."""
        client = self._client(mocker)
        mocker.patch.object(client, "check_method", return_value=True)
        mocker.patch.object(client, "update_header", return_value=None)
        post = mocker.patch.object(client, "post", return_value=object())

        with caplog.at_level(logging.WARNING, logger="nexthink_api.Clients.nxt_data_management_client"):
            self._legacy_call(client.delete_devices, [self._device("not-a-uuid")])

        assert "1 malformed UID" in caplog.text
        assert "not-a-uuid" in caplog.text
        post.assert_called_once()

    def test_delete_devices_permissive_uid_validation_does_not_log(
            self,
            mocker: object,
            caplog: pytest.LogCaptureFixture,
    ) -> None:
        """PERMISSIVE UID validation lets malformed UIDs pass silently."""
        client = self._client(mocker)
        mocker.patch.object(client, "check_method", return_value=True)
        mocker.patch.object(client, "update_header", return_value=None)
        post = mocker.patch.object(client, "post", return_value=object())

        with caplog.at_level(logging.WARNING, logger="nexthink_api.Clients.nxt_data_management_client"):
            self._legacy_call(
                client.delete_devices,
                [self._device("not-a-uuid")],
                uid_validation=NxtUidValidationMode.PERMISSIVE,
            )

        assert not caplog.text
        post.assert_called_once()

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("11111111-1111-1111-1111-111111111111", True),
            ("not-a-uuid", False),
        ],
    )
    def test_is_valid_uuid(self, value: str, expected: bool) -> None:
        """is_valid_uuid detects valid UUID strings."""
        assert NxtApiClient.is_valid_uuid(value) is expected
