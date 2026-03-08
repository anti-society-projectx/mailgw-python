from typing import TYPE_CHECKING

from mailgw.models.domain import Domain

if TYPE_CHECKING:
    from mailgw.client import MailGWClient

class DomainsResource:
    def __init__(self, client: "MailGWClient") -> None:
        self._client = client

    async def get(self, page: int = 1) -> Domain:
        resp = await self._client._request(
            "GET",
            "/domains",
            params={
                "page": page
            }
        )

        return Domain.model_validate(resp.json())

    async def get_by_id(self, domain_id: str) -> Domain:
        resp = await self._client._request(
            "GET",
            "/domains",
            params={
                "id": domain_id
            }
        )

        return Domain.model_validate(resp.json())
