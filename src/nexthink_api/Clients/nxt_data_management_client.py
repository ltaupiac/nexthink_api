"""Internal Data Management domain client."""

import logging
import uuid
from typing import Optional

from nexthink_api.Clients.nxt_response import DataManagementResponseType
from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.DataManagement.nxt_device_deletion_request import NxtDeviceDeletionRequest
from nexthink_api.DataManagement.nxt_device_entry import NxtDeviceEntry
from nexthink_api.DataManagement.nxt_uid_validation_mode import NxtUidValidationMode
from nexthink_api.Models.nxt_endpoint import NxtEndpoint

__all__ = ["NxtDataManagementClient"]

logger = logging.getLogger(__name__)


class NxtDataManagementClient:
    """Internal delegate for Data Management behavior.

    Auth, persistent headers, settings, and transport lifecycle remain owned by
    ``NxtApiClient`` during this phase. Behavior will be moved here only after
    facade compatibility tests are in place.
    """

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal Data Management client."""
        self._api_client = api_client

    def delete_devices(
            self,
            devices: list[NxtDeviceEntry],
            request_id: Optional[str] = None,
            uid_validation: NxtUidValidationMode = NxtUidValidationMode.WARN,
    ) -> DataManagementResponseType:
        """Schedule device deletions through the Data Management API."""
        endpoint = NxtEndpoint.DataManagement
        if not self._api_client.check_method(endpoint, "POST"):
            raise ValueError("Unsupported HTTP method")
        self.validate_device_uids(devices, uid_validation)
        self._api_client.update_header(endpoint)
        headers = {"x-request-id": request_id} if request_id else None
        return self._api_client.post(endpoint, NxtDeviceDeletionRequest(devices=devices), headers=headers)

    @staticmethod
    def validate_device_uids(
            devices: list[NxtDeviceEntry],
            uid_validation: NxtUidValidationMode,
    ) -> None:
        """Validate Data Management device UIDs according to the provided mode."""
        invalid_uids = [device.uid for device in devices if not NxtDataManagementClient.is_valid_uuid(device.uid)]
        if not invalid_uids:
            return
        if uid_validation == NxtUidValidationMode.STRICT:
            raise ValueError(f"{len(invalid_uids)} invalid UID(s): {invalid_uids}")
        if uid_validation == NxtUidValidationMode.WARN:
            logger.warning(
                "%d malformed UID(s); these devices should return INVALID: %s",
                len(invalid_uids),
                invalid_uids,
            )

    @staticmethod
    def is_valid_uuid(value: str) -> bool:
        """Return True if value is a valid UUID."""
        try:
            uuid.UUID(value)
        except ValueError:
            return False
        return True
