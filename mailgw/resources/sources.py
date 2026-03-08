from typing import TYPE_CHECKING

from mailgw.models.source import Source

if TYPE_CHECKING:
    from mailgw import MailGWClient

class SourcesResource:
    def __init__(self, client: "MailGWClient") -> None:
        self._client = client

    async def get_source_message(self, message_id: str, token: str) -> Source:
        resp = await self._client._request(
            "GET",
            f"/sources/{message_id}",
            token=token
        )

        return Source.model_validate(resp.json())
