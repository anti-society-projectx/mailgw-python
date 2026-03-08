from typing import TYPE_CHECKING

from mailgw.models.account import Account

if TYPE_CHECKING:
    from mailgw.client import MailGWClient

class AccountsResource:
    def __init__(self, client: "MailGWClient") -> None:
        self._client = client

    async def create(self, address: str, password: str) -> Account:
        resp = await self._client._request(
            "POST",
            "/accounts",
            json={
                "address": address,
                "password": password
            }
        )

        return Account.model_validate(resp.json())

    async def me(self, token: str) -> Account:
        resp = await self._client._request(
            "GET",
            "/me",
            token=token
        )

        return Account.model_validate(resp.json())

    async def read_by_id(self, account_id: str, token: str) -> Account:
        resp = await self._client._request(
            "GET",
            f"/accounts/{account_id}",
            token=token
        )

        return Account.model_validate(resp.json())

    async def delete_by_id(self, account_id: str, token: str) -> bool:
        await self._client._request(
            "DELETE",
            f"/accounts/{account_id}",
            token=token
        )

        return True
