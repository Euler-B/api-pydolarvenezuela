import httpx
from uuid import uuid4
from typing import Optional

async def send_webhook(url: str, token: str, verify: bool, data: Optional[dict] = {'message': 'Hello, World!'}) -> None:
    try:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'X-Request-ID': str(uuid4())
        }

        async with httpx.AsyncClient(verify=verify) as client:
            response = await client.post(url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
    except httpx.RequestError as e:
        raise Exception(f'Error al enviar el webhook: {e}')
    except Exception as e:
        raise e