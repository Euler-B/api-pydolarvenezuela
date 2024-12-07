import httpx
import asyncio
from uuid import uuid4
from typing import Optional
from sqlalchemy.orm import Session
from ..data.engine import engine
from ..core import logger
from ..data.services.webhooks_db import (
    change_webhook_status, 
    get_all_webhooks,
    get_webhook_by_model as get_webhook
)
from ..data.services.monitors_db import get_monitor_by_id as _get_monitor_by_id_
from ..data.schemas import MonitorSchema
from ..utils.cache import CacheWebhookUser, CacheWebhookMonitor
from ..exceptions import HTTPException

async def send_webhook(url: str, token: str, verify: bool, data: Optional[dict] = {'message': 'Hello, World!'}) -> None:
    """
    Envía un webhook a la url especificada.
    """
    response = None

    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'pyDolarVenezuela/1.0',
            'X-Request-ID': str(uuid4())
        }

        async with httpx.AsyncClient(verify=verify) as client:
            response = await client.post(url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
    except Exception as e:
        if response:
            raise HTTPException(response.status_code, str(e))
        raise HTTPException(500, str(e))
    
def send_webhooks(test: bool = False, **kwargs) -> None:
    """
    Envía los webhooks a las urls especificadas.
    """
    def send_webhook_test() -> None:
        with Session(engine) as session:               
            webhook = get_webhook(session, kwargs.get('token_user'))
            if not webhook:
                raise ValueError('Webhook no encontrado')
            
            data = []
            for m in webhook.monitors:
                monitor = _get_monitor_by_id_(session, m.monitor_id)
                data.append(MonitorSchema().dump(monitor))

            try:
                asyncio.run(
                    send_webhook(webhook.url, webhook.token, webhook.certificate_ssl, {'monitors': data})
                )
            except Exception as e:
                raise e

    if test:
        send_webhook_test()
        return

    with Session(engine) as session:
        monitor_webhooks = CacheWebhookMonitor().get_all_webhook_active()
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

                cache_user = CacheWebhookUser(webhook.id)
                if not cache_user.is_intents_webhook_limit():
                    cache_user.set()
                else:
                    change_webhook_status(session, webhook.id, False)
                    cache_user.delete()
                    logger.info(f'Webhook desactivado por superar el límite de intentos: {webhook.url}')

        CacheWebhookMonitor().delete_all_monitor_webhook()