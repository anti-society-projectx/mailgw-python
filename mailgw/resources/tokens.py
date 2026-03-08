from typing import TYPE_CHECKING

from mailgw.models import Token

if TYPE_CHECKING:
    from mailgw import MailGWClient


class TokensResource:
    def __init__(self, client: "MailGWClient") -> None:
        self._client = client

    async def get_token(self, address: str, password: str) -> Token:
        resp = await self._client._request(
            "POST",
            "/token",
            json={
                "address": address,
                "password": password
            }
        )

        return Token.validate(resp.json())
