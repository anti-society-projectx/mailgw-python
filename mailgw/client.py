from typing import Any

from httpx import AsyncClient, Response
from httpx._types import QueryParamTypes

from mailgw.exceptions import APIError
from mailgw.logger import logger
from mailgw.resources import AccountsResource, DomainsResource, TokensResource
from mailgw.resources.messages import MessagesResources
from mailgw.resources.sources import SourcesResource


class MailGWClient:
    def __init__(
            self,
            timeout: float = 2.0
    ):
        self._base_url = "https://api.mail.gw"
        self._client = AsyncClient(
            base_url=self._base_url,
            timeout=timeout
        )

        self.accounts = AccountsResource(self)
        self.domains = DomainsResource(self)
        self.token = TokensResource(self)
        self.messages = MessagesResources(self)
        self.sources = SourcesResource(self)

        logger.debug("Successful initialization MailGWClient")

    async def __aenter__(self) -> "MailGWClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _request(
            self,
            method: str,
            url: str,
            params: QueryParamTypes | None = None,
            json: Any | None = None,
            token: str | None = None,
            **kwargs: Any
    ) -> Response:
        logger.debug("Fetch to %s method %s%s url", method, self._base_url, url)
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = await self._client.request(
            method=method,
            url=url,
            json=json,
            params=params,
            headers=headers,
            **kwargs
        )

        if response.is_error:
            try:
                payload = response.json()
                message = payload.get("detail") or payload.get("message") or response.text
            except Exception:
                message = response.text

            raise APIError(response.status_code, message)

        return response
