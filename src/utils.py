import requests
from uuid import uuid4
from typing import Optional

def send_webhook(url: str, token: str, verify: bool, data: Optional[dict] = {'message': 'Hello, World!'}) -> None:
    try:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'X-Request-ID': str(uuid4())
        }

        response = requests.post(url, headers=headers, json=data, verify=verify, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f'Error al enviar el webhook: {e}')
    except Exception as e:
        raise e