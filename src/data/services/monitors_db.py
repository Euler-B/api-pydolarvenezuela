from typing import List
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import Page, Monitor, Currency, MonitorPriceHistory
from .webhooks_db import (
    get_unique_monitor_ids as _get_unique_monitor_ids_,
    set_monitor_webhook as _set_monitor_webhook_
)

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
    page = session.query(Page).filter(func.lower(Page.name) == func.lower(name)).first()
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
        _set_monitor_webhook_(monitor_id, True)

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

def modificate_monitor(session: Session, page: str, monitor: str, data: dict) -> None:
    page = session.query(Page).filter(func.lower(Page.name) == func.lower(page)).first() 
    if not page:
        raise Exception("La pagina no fue encontrada.")
    
    monitor = session.query(Monitor).filter(func.lower(Monitor.title) == func.lower(monitor), 
                                            Monitor.page_id == page.id).update(data)
    session.commit()

def get_monitor(session: Session, page_id: int, currency_id: int, monitor: str) -> Monitor:
    monitor = session.query(Monitor).filter(
        Monitor.page_id == page_id, 
        Monitor.currency_id == currency_id, 
        func.lower(Monitor.key) == func.lower(monitor)).first()
    
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

def get_range_history_prices(session: Session, page_id: int, currency_id: int, monitor_name: str, start_date: datetime, end_date: datetime) -> list:
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
    ).order_by(MonitorPriceHistory.last_update.desc()).all() # Order by last_update desc

    for price_history in query:
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

def get_daily_changes(session: Session, page_id: int, currency_id: int, monitor_name: str, date: datetime) -> list:
    monitor = session.query(Monitor).filter(
        Monitor.page_id == page_id, 
        Monitor.currency_id == currency_id, 
        func.lower(Monitor.key) == func.lower(monitor_name)).first()
    
    if not monitor:
        raise Exception("El monitor no fue encontrado.")
    
    results = session.query(MonitorPriceHistory).filter(
        MonitorPriceHistory.monitor_id == monitor.id,
        func.date(MonitorPriceHistory.last_update) == date,
    ).all()

    return [result.__dict__ for result in results]