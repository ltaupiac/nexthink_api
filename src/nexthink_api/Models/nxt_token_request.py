"""Authentication request on the Nexthink API."""

from typing import Dict
from pydantic import BaseModel, Field


class NxtTokenRequest(BaseModel):
    """Model for an OAuth Authentication request on the Nexthink API.

    Attributes
    ----------
        data (Dict[str, str]):
            Header for requesting the Token

    """

    data: Dict[str, str] = Field(
        default={
            'grant_type': 'client_credentials',
            'scope': 'service:integration',
        },
        frozen=True,
    )

    def get_request_header(self) -> dict:
        """Return the form payload for requesting the token.

        Returns
        -------
            dict(str, str):
                Form payload for requesting the Token

        """
        return self.data
