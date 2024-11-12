from typing import Union, Any, List, Dict
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from pyDolarVenezuela.pages import (
    AlCambio, 
    BCV, 
    ExchangeMonitor, 
    EnParaleloVzla
)
from pyDolarVenezuela.models import Monitor, Page
from .data.engine import engine
from .data.models import Monitor as MonitorModel
from .data.services.monitors_db import (
    is_exist_page as _is_exist_page_,
    is_exist_monitor as _is_exist_monitor_,
    is_exist_currency as _is_exist_currency_,
    is_monitor_exists as _is_monitor_exists_,
    create_page as _create_page_,
    create_currency as _create_currency_,
    create_monitor as _create_monitor_,
    create_list_monitors as _create_list_monitors_,
    update_monitor as _update_monitor_,
    get_monitor as _get_monitor_,
    get_list_monitors as _get_list_monitors_,
)
from .consts import TIME_ZONE

class Provider:
    def __init__(self, provider: Page, currency: str, monitor_data: List[Monitor]) -> None:
        self.provider = provider
        self.currency = currency
        self.monitor_data = monitor_data
        
        self.session = sessionmaker(bind=engine)()

        bool_page, self.page_id = _is_exist_page_(self.session, provider.name)
        if not bool_page:    
            self.page_id = _create_page_(self.session, provider.name, provider.provider)

        bool_currency, self.currency_id = _is_exist_currency_(self.session, currency)
        if not bool_currency:
            self.currency_id = _create_currency_(self.session, currency)

    def _load_data(self) -> None:
        for monitor in self.monitor_data:
            if not _is_monitor_exists_(self.session, self.page_id, self.currency_id):
                _create_list_monitors_(self.session, self.page_id, self.currency_id, self.monitor_data)
                break

            if not _is_exist_monitor_(self.session, self.page_id, self.currency_id, monitor.key):
                _create_monitor_(self.session, self.provider.name, monitor.title, monitor.price, monitor.last_update)
            else:
                old_monitor = _get_monitor_(self.session, self.page_id, self.currency_id, monitor.key)
                
                old_last_update = old_monitor.last_update
                new_last_update = monitor.last_update

                update_data = {
                    'price': monitor.price,
                    'price_old': old_monitor.price,
                    'last_update': monitor.last_update
                }

                if old_monitor.image != monitor.image:
                    update_data['image'] = monitor.image

                if self.provider in [AlCambio, ExchangeMonitor, EnParaleloVzla]:
                    if old_last_update.astimezone(TIME_ZONE) != new_last_update:
                        _update_monitor_(self.session, self.page_id, self.currency_id, old_monitor.id, **update_data)
                elif self.provider in [BCV]:
                    if old_last_update.date() != new_last_update.date():
                        _update_monitor_(self.session, self.page_id, self.currency_id, old_monitor.id, **update_data)
                else:
                    if old_monitor.price != monitor.price and monitor.price > 0:
                        _update_monitor_(self.session, self.page_id, self.currency_id, old_monitor.id, **update_data)

    def get_list_monitors(self) -> List[MonitorModel]:
        try:
            self._load_data()
            return _get_list_monitors_(self.session, self.page_id, self.currency_id)
        except Exception as e:
            raise e