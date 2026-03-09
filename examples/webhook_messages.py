import asyncio
import uuid

import httpx

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        domains = await client.domains.get()
        domain = domains.hydra_member[0].domain
        address = f"{uuid.uuid4()}@{domain}"
        password = str(uuid.uuid4())

        account = await client.accounts.create(
            address,
            password
        )
        print(account)

        token_data = await client.token.get_token(account.address, password)
        token = token_data.token

        me = await client.accounts.me(token)
        print(me)

        try:
            async for message in client.messages.listen_messages(me.id, token):
                message_data = await client.messages.read_by_id(message.id, token)

                print("Received message: \n", message_data)
                break

        except httpx.ReadTimeout:
            print('ReadTimeout error')

        await client.accounts.delete_by_id(account.id, token)


if __name__ == "__main__":
    asyncio.run(main())
