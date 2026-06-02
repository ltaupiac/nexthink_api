"""Internal Spark domain client."""

from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.Clients.nxt_response import NxtResponse, SparkResponseType
from nexthink_api.Models.nxt_endpoint import NxtEndpoint
from nexthink_api.Spark.nxt_spark_handoff_conversation_message_request import (
    NxtSparkHandoffConversationMessageRequest,
)

__all__ = ["NxtSparkClient"]


class NxtSparkClient:
    """Internal delegate for Spark behavior."""

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal Spark client."""
        self._api_client = api_client

    def handoff(
            self,
            data: NxtSparkHandoffConversationMessageRequest,
            user_principal_name: str,
            timezone: str | None = None,
    ) -> SparkResponseType:
        """Hand off a conversation message to Spark."""
        if not user_principal_name:
            raise ValueError("user_principal_name is required")
        endpoint = NxtEndpoint.SparkHandoff
        if not self._api_client.check_method(endpoint, "POST"):
            raise ValueError("Unsupported HTTP method")
        self._api_client.update_header(endpoint)
        response = self._api_client.transport.post(
            endpoint.value,
            headers=self._headers(user_principal_name, timezone),
            json=data.model_dump(exclude_none=True, mode="json"),
        )
        return NxtResponse().from_response(response=response)

    def _headers(self, user_principal_name: str, timezone: str | None) -> dict:
        """Return Spark headers with required user principal metadata."""
        headers = dict(self._api_client.headers)
        headers["User-Principal-Name"] = user_principal_name
        if timezone is not None:
            headers["Timezone"] = timezone
        return headers
