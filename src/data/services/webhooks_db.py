import requests
from uuid import uuid4
from typing import Optional
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from ...exceptions import MissingKeyError, WebhookExistsError
from ..models import User, Webhook, MonitorsWebhooks, Page, Monitor
from ..schemas import WebhookSchema
from .users_db import is_user_valid

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