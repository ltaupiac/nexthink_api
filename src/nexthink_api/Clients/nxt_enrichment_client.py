"""Internal Enrichment domain client."""

from nexthink_api.Clients.nxt_client_facade import NxtClientFacade
from nexthink_api.Clients.nxt_response import EnrichmentResponseType
from nexthink_api.Enrichment.nxt_enrichment_request import NxtEnrichmentRequest
from nexthink_api.Models.nxt_endpoint import NxtEndpoint

__all__ = ["NxtEnrichmentClient"]


class NxtEnrichmentClient:
    """Internal delegate for Enrichment behavior.

    Auth, persistent headers, settings, and transport lifecycle remain owned by
    ``NxtApiClient`` during this phase. Enrichment is moved last after the
    delegation pattern is proven on lower-risk domains.
    """

    def __init__(self, api_client: NxtClientFacade) -> None:
        """Initialize the internal Enrichment client."""
        self._api_client = api_client

    def run(self, data: NxtEnrichmentRequest) -> EnrichmentResponseType:
        """Run an enrichment request on the Enrichment endpoint."""
        return self.run_enrichment(NxtEndpoint.Enrichment, data)

    def run_enrichment(self, endpoint: NxtEndpoint, data: NxtEnrichmentRequest) -> EnrichmentResponseType:
        """Run an enrichment request on the specified endpoint using the provided data."""
        if not self._api_client.check_method(endpoint, 'POST'):
            raise ValueError('Unsupported HTTP method')
        self._api_client.update_header(endpoint)
        return self._api_client.post(endpoint, data)
