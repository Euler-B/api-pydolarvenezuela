from sqlalchemy import func
from sqlalchemy.orm import Session
from pyDolarVenezuela.data.models import (
    Page, 
    Monitor, 
    MonitorPriceHistory
)

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

def modificate_monitor(session: Session, page: str, monitor: str, data: dict) -> None:
    page = session.query(Page).filter(func.lower(Page.name) == func.lower(page)).first() 
    if not page:
        raise Exception("La pagina no fue encontrada.")
    
    monitor = session.query(Monitor).filter(func.lower(Monitor.title) == func.lower(monitor), 
                                            Monitor.page_id == page.id).update(data)
    session.commit()