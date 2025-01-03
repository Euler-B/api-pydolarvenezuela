from typing import List
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import Page, Monitor, Currency, MonitorPriceHistory
from .webhooks_db import (
    get_unique_monitor_ids as _get_unique_monitor_ids_,
)
from ...utils.cache import CacheWebhookMonitor

# Validators

def is_exist_page(session: Session, name: str) -> tuple:
    page = session.query(Page).filter(func.lower(Page.name) == func.lower(name)).first()
    return page is not None, page.id if page else None

def is_exist_currency(session: Session, symbol: str) -> tuple:
    currency = session.query(Currency).filter(func.lower(Currency.symbol) == func.lower(symbol)).first()
    return currency is not None, currency.id if currency else None

def is_exist_monitor(session: Session, page_id: int, currency_id: int, monitor: str) -> bool:
    return session.query(Monitor).filter(
                Monitor.page_id == page_id, 
                Monitor.currency_id == currency_id, 
                func.lower(Monitor.key) == func.lower(monitor)).count() > 0

def is_monitor_exists(session: Session, page_id: int, currency_id: int) -> bool:
    return session.query(Monitor).filter(
            Monitor.page_id == page_id, Monitor.currency_id == currency_id
            ).count() > 0
    
# Services

def create_page(session: Session, name: str, url: str) -> int:
    page = Page(name=name, url=url) 
    session.add(page) 
    session.commit() 
    
    return page.id

def delete_page(session: Session, name: str) -> None:
    from ...utils.func_consts import get_provider
    provider_name = get_provider(name)
    page = session.query(Page).filter(func.lower(Page.name) == func.lower(provider_name)).first()
    if not page:
        raise Exception("La pagina no fue encontrada.")
    
    monitors = session.query(Monitor).filter(Monitor.page_id == page.id).all()
    for monitor in monitors:
        session.query(MonitorPriceHistory).filter(MonitorPriceHistory.monitor_id == monitor.id).delete()
    session.query(Monitor).filter(Monitor.page_id == page.id).delete()
    session.query(Page).filter(Page.name == name).delete()
    session.commit()

def create_currency(session: Session, symbol: str) -> int:
    currency = Currency(symbol=symbol)
    session.add(currency)
    session.commit()
    
    return currency.id

# Monitors

def create_monitor(session: Session, page_id: int, currency_id: int, **kwargs) -> int:
    session.add(Monitor(page_id=page_id, currency_id=currency_id, **kwargs))
    session.commit()

def create_list_monitors(session: Session, page_id: int, currency_id: int, monitors: list) -> None:
    monitors = [
        Monitor(**monitor.__dict__, page_id=page_id, currency_id=currency_id) for monitor in monitors
    ]
    session.add_all(monitors)
    session.commit()

def update_monitor(session: Session, page_id: int, currency_id: int, monitor_id: int, **kwargs) -> None:
    monitor_ids = _get_unique_monitor_ids_(session)

    if monitor_id in monitor_ids:
        CacheWebhookMonitor(monitor_id).set(True)

    old_price = kwargs.get('price_old')
    new_price = kwargs.get('price')

    change  = round(float(new_price) - float(old_price), 2)
    percent = float(f'{round(float((change / new_price) * 100 if old_price != 0 else 0), 2)}'.replace('-', ' ')),
    color   =  "red" if new_price < old_price else "green" if new_price > old_price else "neutral"
    symbol  = "▲" if color == "green" else "▼" if color == "red" else ""
    last_update = kwargs.get('last_update')
    change  = float(str(change).replace('-', ''))

    data = {
        'price': new_price,
        'price_old': old_price,
        'change': change,
        'percent': percent,
        'color': color,
        'symbol': symbol,
        'last_update': last_update
    }
    
    session.query(Monitor).filter(
        Monitor.page_id == page_id, 
        Monitor.currency_id == currency_id, 
        Monitor.id == monitor_id).update(data)
    session.commit()
    add_history_price(session, monitor_id, new_price, last_update)

def modificate_monitor(session: Session, page: str, currency: str, monitor_title: str, data: dict, update: bool) -> None:
    from ...consts import PROVIDERS
    from ...utils.cache import CacheProvider

    page = session.query(Page).filter(func.lower(Page.name) == func.lower(page)).first() 
    if not page:
        raise Exception("La pagina no fue encontrada.")
    
    currency = session.query(Currency).filter(func.lower(Currency.symbol) == func.lower(currency)).first()
    if not currency:
        raise Exception("La moneda no fue encontrada.")
    
    cache = CacheProvider(PROVIDERS.get(page.name)['id'], currency.symbol)
    monitor = session.query(Monitor).filter(func.lower(Monitor.title) == func.lower(monitor_title), 
                                            Monitor.page_id == page.id,
                                            Monitor.currency_id == currency.id).first()
    
    for key, value in data.items(): setattr(monitor, key, value)
    
    if not update:
        monitor_price_history = session.query(MonitorPriceHistory).\
            filter(MonitorPriceHistory.monitor_id == monitor.id).order_by(MonitorPriceHistory.id.desc()).first()
        session.delete(monitor_price_history)

    session.commit()
    add_history_price(session, monitor.id, data['price'], data['last_update'])
    cache.set([m.__dict__ for m in session.query(Monitor).filter(Monitor.page_id == page.id, Monitor.currency_id == currency.id).all()])

def get_monitor(session: Session, page_id: int, currency_id: int, monitor: str) -> Monitor:
    monitor = session.query(Monitor).filter(
        Monitor.page_id == page_id, 
        Monitor.currency_id == currency_id, 
        func.lower(Monitor.key) == func.lower(monitor)).first()
    
    if not monitor:
        raise Exception("El monitor no fue encontrado.")
    
    return monitor

def get_monitor_by_id(session: Session, monitor_id: int) -> Monitor:
    monitor = session.query(Monitor).filter(Monitor.id == monitor_id).first()
    
    if not monitor:
        raise Exception("El monitor no fue encontrado.")
    
    return monitor

def get_list_monitors(session: Session, page_id: int, currency_id: int) -> List[Monitor]:
    return session.query(Monitor).filter(
        Monitor.page_id == page_id, Monitor.currency_id == currency_id
    ).all()

# History Prices

def add_history_price(session: Session, monitor_id: int, price: float, last_update: datetime) -> None:
    session.add(MonitorPriceHistory(monitor_id=monitor_id, price=price, last_update=last_update))
    session.commit()

def get_range_history_prices(session: Session, page_id: int, currency_id: int, monitor_name: str, start_date: datetime, end_date: datetime, order: str) -> list:
    monitor = session.query(Monitor).filter(
        Monitor.page_id == page_id, 
        Monitor.currency_id == currency_id, 
        func.lower(Monitor.key) == func.lower(monitor_name)).first()
    
    if not monitor:
        raise Exception("El monitor no fue encontrado.")
    
    changes = {}
    query = session.query(MonitorPriceHistory).filter(
        MonitorPriceHistory.monitor_id == monitor.id,
        func.date(MonitorPriceHistory.last_update) >= start_date,
        func.date(MonitorPriceHistory.last_update) <= end_date
    )

    if order == 'asc':
        query = query.order_by(MonitorPriceHistory.last_update.asc())
    else:
        query = query.order_by(MonitorPriceHistory.last_update.desc())

    for price_history in query.all():
        date_key = price_history.last_update.date()
        
        if date_key not in changes:
            changes[date_key] = {
                'price': price_history.price,
                'price_high': price_history.price,
                'price_low': price_history.price,
                'price_open': price_history.price,
                'last_update': price_history.last_update
            }
        else:
            changes[date_key]['price_high'] = max(changes[date_key]['price_high'], price_history.price)
            changes[date_key]['price_low']  = min(changes[date_key]['price_low'], price_history.price)
            changes[date_key]['price_open'] = price_history.price
    
    return [{**value} for value in changes.values()]

def get_daily_changes(session: Session, page_id: int, currency_id: int, monitor_name: str, date: datetime, order: str) -> list:
    monitor = session.query(Monitor).filter(
        Monitor.page_id == page_id, 
        Monitor.currency_id == currency_id, 
        func.lower(Monitor.key) == func.lower(monitor_name)).first()
    
    if not monitor:
        raise Exception("El monitor no fue encontrado.")
    
    results = session.query(MonitorPriceHistory).filter(
        MonitorPriceHistory.monitor_id == monitor.id,
        func.date(MonitorPriceHistory.last_update) == date,
    )

    if order == 'asc':
        results = results.order_by(MonitorPriceHistory.last_update.asc())
    else:
        results = results.order_by(MonitorPriceHistory.last_update.desc())

    return [result.__dict__ for result in results.all()]