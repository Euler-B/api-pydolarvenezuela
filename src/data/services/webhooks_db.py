from typing import Optional, List
from datetime import datetime
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from ...exceptions import MissingKeyError, WebhookExistsError
from ..models import User, Webhook, MonitorsWebhooks, Page, Currency, Monitor
from ..schemas import WebhookSchema
from .users_db import is_user_valid

def raise_webhook_exists_error(session: Session, token_user: str) -> None:
    user = session.query(User).filter(User.token == token_user).first()
    if not user:
        raise Exception('Usuario no encontrado')

    if session.query(Webhook).filter(Webhook.user_id == user.id).count() > 0:
        raise WebhookExistsError('El webhook ya existe')
    
def create_webhook(session: Session, token_user: str, **kwargs) -> None:
    from ...utils.func_consts import get_provider, get_currency    
    user = session.query(User).filter(User.token == token_user).first()

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
            if 'page' not in monitor_data or 'currency' not in monitor_data or'monitor' not in monitor_data:
                raise MissingKeyError('Cada objeto debe contener page, currency y monitor')

            provider_name = get_provider(monitor_data['page'])
            page = session.query(Page).filter(func.lower(Page.name) == func.lower(provider_name)).first()
            if not page:
                raise ValueError('Pagina no encontrada')
            
            currency_name = get_currency(monitor_data['currency'])
            currency = session.query(Currency).filter(func.lower(Currency.symbol) == func.lower(currency_name)).first()
            if not currency:
                raise ValueError('Moneda no encontrada')
            
            monitor = session.query(Monitor).filter(
                Monitor.page_id == page.id,
                Monitor.currency_id == currency.id, 
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

def get_webhook_by_model(session: Session, token_user: str) -> Webhook:
    user = session.query(User).filter(User.token == token_user).first()
    return session.query(Webhook).filter(Webhook.user_id == user.id).first()

def change_webhook_status(session: Session, webhook_id: int, status: bool) -> None:
    webhook = session.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise ValueError('Webhook no encontrado')
    
    webhook.status = status
    session.commit()

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