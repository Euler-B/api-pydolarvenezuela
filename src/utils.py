import httpx
import asyncio
from uuid import uuid4
from typing import Optional
from sqlalchemy.orm import Session
from .data.engine import engine
from .core import logger
from .consts import PROVIDERS, CURRENCIES
from .data.services.webhooks_db import (
    get_all_monitor_webhook,
    change_webhook_status, 
    delete_all_monitor_webhook,
    get_all_webhooks,
    set_webhook_status,
    is_intents_webhook_limit,
    delete_webhook_status
)
from .data.schemas import MonitorSchema

async def send_webhook(url: str, token: str, verify: bool, data: Optional[dict] = {'message': 'Hello, World!'}) -> None:
    try:
        headers = {
            'Authorization': f'Bearer {token}',
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
    
def send_webhooks(test: bool = False, **kwargs) -> None:
    """
    Envía los webhooks a los monitores.
    """
    from .data.services.monitors_db import get_monitor_by_id as _get_monitor_by_id_
    from .data.services.webhooks_db import get_webhook_by_model as get_webhook

    def send_webhook_test() -> None:
        with Session(engine) as session:               
            webhook = get_webhook(session, kwargs.get('token_user'))
            if not webhook:
                return
            
            data = []
            for m in webhook.monitors:
                monitor = _get_monitor_by_id_(session, m.monitor_id)
                data.append(MonitorSchema().dump(monitor))

            try:
                asyncio.run(
                    send_webhook(webhook.url, webhook.token, webhook.certificate_ssl, {'monitors': data})
                )
            except Exception as e:
                logger.error(f'Error al enviar el webhook: {str(e)}')

    if test:
        send_webhook_test()
        return

    with Session(engine) as session:
        monitor_webhooks = get_all_monitor_webhook()
        if not monitor_webhooks:
            return
        
        monitors_ids_save = {}
        for webhook in get_all_webhooks(session):
            if not webhook.status:
                continue
            data = []

            for m in webhook.monitors:
                if m.monitor_id not in monitor_webhooks:
                    continue
                
                if m.monitor_id in monitors_ids_save:
                    data.append(monitors_ids_save[m.monitor_id])
                    continue

                monitor = _get_monitor_by_id_(session, m.monitor_id)
                monitors_ids_save[m.monitor_id] = MonitorSchema().dump(monitor)
                data.append(monitors_ids_save[m.monitor_id])
            try:
                asyncio.run(
                    send_webhook(webhook.url, webhook.token, webhook.certificate_ssl, {'monitors': data})
                )
            except Exception as e:
                logger.error(f'Error al enviar el webhook: {str(e)}')

                if not is_intents_webhook_limit(webhook.id):
                    set_webhook_status(webhook.id, 1)
                else:
                    change_webhook_status(session, webhook.id, False)
                    delete_webhook_status(webhook.id)
                    logger.info(f'Webhook desactivado por superar el límite de intentos: {webhook.url}')

        delete_all_monitor_webhook()

def get_provider(provider: str) -> str:
    for key, value in PROVIDERS.items():
        if provider.lower() in value.lower():
            return key
    return provider
        
def get_currency(currency: str) -> str:
    return CURRENCIES.get(currency.lower())