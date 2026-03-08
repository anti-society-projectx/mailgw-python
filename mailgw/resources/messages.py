from typing import TYPE_CHECKING

import httpx
from httpx_sse import aconnect_sse
import json

from mailgw.logger import logger
from mailgw.models import Account
from mailgw.models.message import Messages, Message, ReadMessage

if TYPE_CHECKING:
    from mailgw.client import MailGWClient


class MessagesResources:
    def __init__(self, client: "MailGWClient") -> None:
        self._client = client

    async def listen_messages(self, account_id: str, token: str, read_timeout: float | None = 120.0):
        params = {
            "topic": f"/accounts/{account_id}",
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        async with aconnect_sse(
                self._client._client,
                "GET",
                "https://api.mail.gw/.well-known/mercure",
                params=params,
                headers=headers,
                timeout=httpx.Timeout(connect=10.0, read=read_timeout, write=10.0, pool=None)
        ) as event_source:
            async for sse in event_source.aiter_sse():
                raw = json.loads(sse.data)
                match raw.get("@type"):
                    case "Message":
                        yield Message.model_validate(raw)

    async def reads(self, token: str) -> Messages:
        resp = await self._client._request(
            "GET",
            "/messages",
            token=token
        )

        return Messages.model_validate(resp.json())

    async def read_by_id(self, message_id: str, token: str) -> ReadMessage:
        resp = await self._client._request(
            "GET",
            f"/messages/{message_id}",
            token=token
        )

        return ReadMessage.model_validate(resp.json())
