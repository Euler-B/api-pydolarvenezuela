from typing import Optional, List
from datetime import datetime
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from ...exceptions import MissingKeyError, WebhookExistsError
from ...core import cache
from ..models import User, Webhook, MonitorsWebhooks, Page, Monitor
from ..schemas import WebhookSchema
from .users_db import is_user_valid

def create_webhook(session: Session, token_user: str, **kwargs) -> None:    
    if not is_user_valid(session, token_user):
        raise Exception('User not found')
    
    user = session.query(User).filter(User.token == token_user).first()
    
    if session.query(Webhook).filter(Webhook.user_id == user.id).count() > 0:
        raise WebhookExistsError('Webhook already exists')

    try:
        new_webhook = Webhook(
            user_id=user.id, 
            url=kwargs.get('url'), 
            token=kwargs.get('token'), 
            certificate_ssl=kwargs.get('certificate_ssl'),
            created_at=datetime.now()
            )
        session.add(new_webhook)

        for monitor_data in kwargs.get('monitors'):
            if 'page' not in monitor_data or 'monitor' not in monitor_data:
                raise MissingKeyError('Cada objeto debe contener page y monitor.')
            
            page = session.query(Page).filter(func.lower(Page.name) == func.lower(monitor_data['page'])).first()
            if not page:
                raise ValueError('Pagina no encontrada')
            
            monitor = session.query(Monitor).filter(
                Monitor.page_id == page.id, 
                func.lower(Monitor.key) == func.lower(monitor_data['monitor'])).first()
            if not monitor:
                raise ValueError('Monitor no encontrado')
    
            new_monitor_webhook = MonitorsWebhooks(
                webhook_id=new_webhook.id,
                monitor_id=monitor.id
            )
            session.add(new_monitor_webhook)
        session.commit()
    except Exception as e:
        session.rollback() # Rollback the transaction
        raise e
    
def get_webhook(session: Session, token_user: str) -> dict:
    if not is_user_valid(session, token_user):
        raise Exception('User not found')
    
    user = session.query(User).filter(User.token == token_user).first()
    
    webhook = session.query(Webhook).filter(Webhook.user_id == user.id).all()
    if not webhook:
        return []
    
    return WebhookSchema().dump(webhook, many=True)

def delete_webhook(session: Session, token_user: str, webhook_id: Optional[int] = None) -> None:
    if not is_user_valid(session, token_user):
        raise Exception('User not found')
    
    user = session.query(User).filter(User.token == token_user).first()
    
    webhook = session.query(Webhook).filter(Webhook.user_id == user.id).first()
    if not webhook:
        raise ValueError('Webhook no encontrado')
    
    session.query(MonitorsWebhooks).filter(MonitorsWebhooks.webhook_id == webhook.id).delete()
    session.delete(webhook)
    session.commit()

def get_unique_monitor_ids(session: Session) -> List[int]:
    unique_monitor_ids = session.query(distinct(MonitorsWebhooks.monitor_id)).all()

    return [monitor_id for monitor_id, in unique_monitor_ids]

def get_all_webhooks(session: Session) -> List[Webhook]:
    return session.query(Webhook).all()

# Cache

def get_all_monitor_webhook() -> List[int]:
    keys = cache.keys('monitor_webhook:*')
    if not keys:
        return []

    return [int(key.split(':')[1]) for key in keys if cache.get(key) not in [None, 0]]

def set_monitor_webhook(monitor_id: int, boolean: bool) -> None:
    cache.set(f'monitor_webhook:{monitor_id}', int(boolean))

def is_monitor_webhook(monitor_id: int) -> bool:
    return cache.get(f'monitor_webhook:{monitor_id}') is not None

def delete_monitor_webhook(monitor_id: int) -> None:
    cache.delete(f'monitor_webhook:{monitor_id}')

def delete_all_monitor_webhook() -> None:
    keys = cache.keys('monitor_webhook:*')
    for key in keys:
        cache.set(key, 0)