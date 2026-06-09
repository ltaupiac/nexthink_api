"""Nexthink Tenant Configuration Class."""

from typing import ClassVar, Self, Optional, Dict, Union
import os
from pydantic import BaseModel, HttpUrl, Field, model_validator

from nexthink_api.Models.nxt_region_name import NxtRegionName


class NxtSettings(BaseModel):
    """Configuration class for Nexthink API.

    This class is used by client during initialization.

    Attributes
    ----------
        instance : str
            The name of the Nexthink instance.
        region : NxtRegionName
            The region of the Nexthink instance.
        infinity_base_uri : HttpUrl
            The base URI of the Nexthink API.
        token_url : HttpUrl
            The URL of the token endpoint.
        proxies : Optional[dict]
            A dictionary of proxies to use for the requests. Defaults to None.

    > ### Note
    >    - if proxy are not provided, it will try to detect proxies from environment variables
    >    - if no proxy are detected, it will disable the proxy
    >    - false value disable the proxy

    """

    base_url: ClassVar[str] = 'https://{instance}.api.{region}.nexthink.cloud'
    login_base_url: ClassVar[str] = 'https://{instance}-login.{region}.nexthink.cloud'
    token_path: ClassVar[str] = '/oauth2/default/v1/token'
    instance: str = Field(min_length=1)
    region: NxtRegionName
    infinity_base_uri: HttpUrl = Field(init=False, default=None)
    token_url: HttpUrl = Field(init=False, default=None)
    proxies: Optional[Union[Dict[str, str], bool]] = None

    @model_validator(mode='before')
    @classmethod
    def set_infinity_base_uri(cls, values: dict) -> dict:
        """Set the base URI of the Nexthink API.

        Parameters
        ----------
            values : dict
                class attributes in dict format

        Returns
        -------
            dict
                The validated and updated attributes in dict format.

        Raises
        ------
            ValueError
                If instance or region are not provided.

        """
        instance = values.get("instance")
        region = values.get("region")

        if instance is None or region is None:
            raise ValueError("Instance and Region are required")

        region_value = region.value if isinstance(region, NxtRegionName) else region
        values['infinity_base_uri'] = cls.base_url.format(instance=instance, region=region_value)
        values['token_url'] = f"{cls.login_base_url.format(instance=instance, region=region_value)}{cls.token_path}"
        return values

    @model_validator(mode='after')
    def set_settings_init(self) -> Self:
        """Finish the initialization of the settings object when class is instantiated.

        Returns
        -------
            NxtSettings
                the instantiated class

        """
        # Proxy has not been provided, try to detect proxies
        if self.proxies is None:
            # Attempt to detect proxies from environment variables (optional)
            self.proxies = {
                'http': os.getenv("http_proxy") or os.getenv("HTTP_PROXY"),
                'https': os.getenv("https_proxy") or os.getenv("HTTPS_PROXY")
            } or {}
        # False is used to disable proxy
        elif self.proxies is False:
            self.proxies = {}

        return self
