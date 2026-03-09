# mailgw-python

Async Python client for the [mail.gw](https://mail.gw) API.

It helps you:
- list available domains
- create and manage temporary mail accounts
- read mailbox messages
- listen for new messages in real time (Mercure/SSE webhook-like stream)
- fetch raw source of a message

## Requirements

- Python 3.10+

## Installation

### Poetry

```bash
poetry add mailgw-python
```

### pip (from PyPI)

```bash
pip install mailgw-python
```

### pip (specific version)

```bash
pip install "mailgw-python==0.1.0"
```

### pip (from TestPyPI)

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple mailgw-python
```

### pip (from GitHub)

```bash
pip install "git+https://github.com/<your-user>/<your-repo>.git"
```

### pip (from local source)

```bash
pip install .
```

## Quick Start

```python
import asyncio
import uuid

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        domains = await client.domains.get()
        domain = domains.hydra_member[0].domain

        address = f"{uuid.uuid4()}@{domain}"
        password = str(uuid.uuid4())

        account = await client.accounts.create(address, password)
        token_data = await client.token.get_token(address, password)
        token = token_data.token

        messages = await client.messages.reads(token)
        print(f"Mailbox has {messages.total_items} messages")

        await client.accounts.delete_by_id(account.id, token)


if __name__ == "__main__":
    asyncio.run(main())
```

## API Usage Examples

### 1) Get all domains

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        domains = await client.domains.get(page=1)
        for item in domains.hydra_member or []:
            print(item.domain, item.is_active)


if __name__ == "__main__":
    asyncio.run(main())
```

### 2) Get one domain by ID

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        domain = await client.domains.get_by_id("your-domain-id")
        print(domain)


if __name__ == "__main__":
    asyncio.run(main())
```

### 3) Create one account

```python
import asyncio
import uuid

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        domains = await client.domains.get()
        domain = domains.hydra_member[0].domain

        address = f"{uuid.uuid4()}@{domain}"
        password = str(uuid.uuid4())

        account = await client.accounts.create(address, password)
        print("Account ID:", account.id)
        print("Address:", account.address)


if __name__ == "__main__":
    asyncio.run(main())
```

### 4) Authenticate and get token

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        token_data = await client.token.get_token(
            address="user@your-domain.tld",
            password="your-password",
        )
        print("Token:", token_data.token)


if __name__ == "__main__":
    asyncio.run(main())
```

### 5) Get current account (`/me`)

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        me = await client.accounts.me("your-jwt-token")
        print(me.id, me.address)


if __name__ == "__main__":
    asyncio.run(main())
```

### 6) Get all messages

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        messages = await client.messages.reads("your-jwt-token")
        print("Total:", messages.total_items)
        for message in messages.messages:
            print(message.id, message.subject)


if __name__ == "__main__":
    asyncio.run(main())
```

### 7) Get one message by ID

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        message = await client.messages.read_by_id(
            message_id="your-message-id",
            token="your-jwt-token",
        )
        print(message.subject)
        print(message.text)


if __name__ == "__main__":
    asyncio.run(main())
```

### 8) Get raw message source

```python
import asyncio

from mailgw import MailGWClient


async def main():
    async with MailGWClient() as client:
        source = await client.sources.get_source_message(
            message_id="your-message-id",
            token="your-jwt-token",
        )
        print(source.data)


if __name__ == "__main__":
    asyncio.run(main())
```

### 9) Receive messages via webhook-like stream (SSE)

`listen_messages` subscribes to the Mail.gw Mercure topic for your account and yields new `Message` events.

```python
import asyncio
import httpx

from mailgw import MailGWClient


async def main():
    account_id = "your-account-id"
    token = "your-jwt-token"

    async with MailGWClient() as client:
        try:
            async for event in client.messages.listen_messages(account_id, token):
                full_message = await client.messages.read_by_id(event.id, token)
                print("New message:", full_message.subject)
                break
        except httpx.ReadTimeout:
            print("No new messages within timeout window")


if __name__ == "__main__":
    asyncio.run(main())
```

### 10) Forward new messages to your own webhook URL

If you need classic HTTP webhooks, subscribe via SSE and forward each event to your endpoint.

```python
import asyncio
import httpx

from mailgw import MailGWClient


async def main():
    account_id = "your-account-id"
    token = "your-jwt-token"
    webhook_url = "https://your-service.example/webhooks/mailgw"

    async with MailGWClient() as client, httpx.AsyncClient(timeout=10.0) as webhook_client:
        async for event in client.messages.listen_messages(account_id, token):
            message = await client.messages.read_by_id(event.id, token)
            await webhook_client.post(
                webhook_url,
                json={
                    "id": message.id,
                    "subject": message.subject,
                    "intro": message.intro,
                    "text": message.text,
                    "created_at": message.created_at,
                },
            )


if __name__ == "__main__":
    asyncio.run(main())
```

## Resource Methods

### `client.domains`
- `get(page: int = 1)`
- `get_by_id(domain_id: str)`

### `client.accounts`
- `create(address: str, password: str)`
- `me(token: str)`
- `read_by_id(account_id: str, token: str)`
- `delete_by_id(account_id: str, token: str)`

### `client.token`
- `get_token(address: str, password: str)`

### `client.messages`
- `reads(token: str)`
- `read_by_id(message_id: str, token: str)`
- `listen_messages(account_id: str, token: str, read_timeout: float | None = 120.0)`

### `client.sources`
- `get_source_message(message_id: str, token: str)`

## Error Handling

All API errors raise `mailgw.exceptions.APIError`.

```python
import asyncio

from mailgw import MailGWClient
from mailgw.exceptions import APIError


async def main():
    async with MailGWClient() as client:
        try:
            await client.accounts.me("invalid-token")
        except APIError as e:
            print(f"Status: {e.status_code}")
            print(f"Message: {e.message}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Notes

- Use `async with MailGWClient()` to close HTTP connections automatically.
- You can override request timeout: `MailGWClient(timeout=5.0)`.
- Real-time updates use Mercure Server-Sent Events (SSE).
