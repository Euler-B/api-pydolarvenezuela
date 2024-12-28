import json
import re
from typing import Union, Optional, Literal, Dict, List, Any
from datetime import datetime
from sqlalchemy.orm import Session
from .data.engine import engine
from .data.schemas import HistoryPriceSchema, DailyChangeSchema, MonitorSchema
from .data.services.monitors_db import (
    is_exist_page as _is_exist_page_,
    is_exist_currency as _is_exist_currency_,
    get_range_history_prices as _get_range_history_prices_, 
    get_daily_changes as _get_daily_changes_
)
from .utils.time import get_time_zone as getdate
from .utils.cache import CacheProvider, CacheHistoryMonitor
from .utils.func_consts import get_provider, get_currency
from .consts import PROVIDERS, CURRENCIES
from ._dataclass import Monitor

def _currency_converter(type: Literal['VES', 'USD', 'EUR'], value, monitor: Union[Monitor, dict]) -> Union[float, None]:
    """
    Convierte una cantidad de dinero de una moneda a otra utilizando los datos de un monitor específico.
    """
    price_monitor = monitor.price if isinstance(monitor, Monitor) else monitor.get('price', None)
    if not price_monitor:
        raise KeyError('The monitor was not found')

    try:
        if isinstance(value, int) or isinstance(value, float):
            if type == 'VES':
                return value / float(price_monitor)
            elif type in ['USD', 'EUR']:
                return value * float(price_monitor)
            else:
                raise ValueError(f"El tipo debe ser USD o VES no {type}.")
    except TypeError as e:
        raise e

def _check_currency_provider(provider, currency):
    """
    Valida si la moneda y el proveedor existen.
    """
    if currency not in CURRENCIES.keys():
        raise ValueError('No se encontró la moneda.')
    
    if provider not in [PROVIDERS[p]['id'] for p in PROVIDERS.keys()]:
        raise ValueError('No se encontró el proveedor.')
    
    provider_currencies = [PROVIDERS[p]['currencies'] for p in PROVIDERS if PROVIDERS[p]['id'] == provider][0]
    if CURRENCIES.get(currency) not in provider_currencies:
        raise ValueError(f'El proveedor {provider} no tiene la moneda {currency}.')

def _get_monitor(monitor_code: str, monitors_founds: Dict[str, Dict[str, Any]]) -> Union[Dict[str, Any], None]:
    """
    Obtiene un monitor en específico.

    - monitor_code: Key del monitor.
    - monitors_founds: Monitores encontrados.
    """
    if monitor_code in monitors_founds:
        return monitors_founds[monitor_code]
    return None

def _validate_date(date: str): 
    if re.match(r'\d{2}-\d{2}-\d{4}', date) is None: 
        raise ValueError('El formato de la fecha debe ser: dd-mm-yyyy.')

def get_all_monitors(
        currency: str, 
        provider: str, 
        format_date: Literal['timestamp', 'iso', 'default'],
        rounded_price: bool) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de un proveedor que estan guardado en caché.

    - currency: Moneda.
    - provider: Proveedor.
    - format_date: Formato de fecha.
    """
    if provider == 'default':
        return get_accurate_monitors(None, format_date, rounded_price)
    _check_currency_provider(provider, currency)
    
    cache = CacheProvider(provider, CURRENCIES.get(currency))
    monitors_dict = None
    
    if cache.get() is not None:
        monitors_serialized = MonitorSchema(custom_format=format_date, rounded_price=rounded_price, many=True).dump(cache.get())
        monitors_dict = {data.pop('key'): data for data in monitors_serialized if data.get('key')}
    
    result = {
        "datetime": getdate(),
        "monitors": {} if not monitors_dict else monitors_dict
    }
    return result

def get_accurate_monitors(monitor_code: Optional[str], format_date: str, rounded_price: bool) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de las paginas BCV y EnParaleloVzla que estan guardado en caché.

    - monitor_code: Key del monitor.
    - format_date: Formato de fecha.
    """
    default_monitors = [('bcv', 'usd'), ('enparalelovzla', 'usd')]
    monitor_data = {}
    for key in default_monitors:
        cache = CacheProvider(*key)
        
        if cache.get() is None:
            continue
        monitors_serialized = MonitorSchema(custom_format=format_date, rounded_price=rounded_price, many=True).dump(cache.get())
        monitors_dict = {data.pop('key'): data for data in monitors_serialized if data.get('key')}

        if 'usd' in monitors_dict:
            monitor_data['bcv'] = monitors_dict['usd']
            continue
        monitor_data['enparalelovzla'] = monitors_dict['enparalelovzla']
    
    if monitor_code:
        result = _get_monitor(monitor_code, monitor_data)
        if result is None:
            raise KeyError('No se encontró el monitor que estás buscando.')
        return result
    
    result = {
        "datetime": getdate(),
        "monitors": monitor_data
    }
    return result

def get_page_or_monitor(
        currency: str, 
        page: Optional[str], 
        monitor_code: Optional[str], 
        format_date: str,
        rounded_price: bool) -> Union[Dict[str, Any], Dict[str, str]]:    
    """
    Obtiene los monitores de una página o un monitor en específico.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor
    - format_date: Formato de fecha.
    """
    page = 'default' if page is None and currency == 'dollar' else 'criptodolar' if page is None else page
    result = get_all_monitors(currency, page, format_date, rounded_price)
    
    if monitor_code:
        result = _get_monitor(monitor_code, result['monitors'])
        if result is None:
            raise KeyError('No se encontró el monitor que estás buscando.')
    return result

def fetch_monitor_data(
        page_id: int, 
        currency_id: int, 
        monitor_code: str, 
        start_date: str, 
        end_date: str, 
        data_type: Literal['daily', 'history'],
        order: Literal['asc', 'desc']) -> List[Dict[str, Any]]:
    with Session(engine) as session:
        if data_type == 'history':
            return _get_range_history_prices_(session, page_id, currency_id, monitor_code, start_date, end_date, order)
        elif data_type == 'daily':
            return _get_daily_changes_(session, page_id, currency_id, monitor_code, start_date, order)
        return []

def get_monitor_data(
        currency: str, 
        page: str, 
        monitor_code: str, 
        start_date: str, 
        end_date: str, 
        data_type: Literal['daily', 'history'], 
        format_date: Literal['timestamp', 'iso', 'default'],
        rounded_price: bool,
        order: Literal['asc', 'desc']) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de precios de un monitor.
    """
    cache = CacheHistoryMonitor(page, currency, monitor_code, start_date, end_date, data_type, order)
    
    if cache.get() is None:
        name_page = get_provider(page)
        symbol    = get_currency(currency)

        if not all([name_page, symbol]):
            raise KeyError('No se encontró la página o la moneda que estás buscando.')
        
        with Session(engine) as session:
            _p, page_id = _is_exist_page_(session, name_page)
            _c, currency_id = _is_exist_currency_(session, symbol)
            
            for date in [start_date, end_date]:
                _validate_date(date)

            start_date  = datetime.strptime(start_date, "%d-%m-%Y").date()
            end_date    = datetime.strptime(end_date, "%d-%m-%Y").date()
            results = fetch_monitor_data(page_id, currency_id, monitor_code, start_date, end_date, data_type, order)  
            
            if not results:
                raise ValueError('No se encontraron datos para el monitor solicitado.')
            
            cache.set(results)
    
    if data_type == 'daily':
        schema = DailyChangeSchema(custom_format=format_date, rounded_price=rounded_price, many=True).dump(cache.get())
    else:
        schema = HistoryPriceSchema(custom_format=format_date, rounded_price=rounded_price, many=True).dump(cache.get())
    results = {
        'datetime': getdate(),
        data_type: schema
    }
    return results       

def get_history_prices(
        currency: str, 
        page: str, 
        monitor_code: str, 
        start_date: str, 
        end_date: str, 
        format_date: str,
        rounded_price: bool,
        order: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene el historial de precios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - start_date: Fecha de inicio.
    - end_date: Fecha de finalización.
    """
    return get_monitor_data(currency, page, monitor_code, start_date, end_date, 'history', format_date, rounded_price, order)

def get_daily_changes(
        currency: str, 
        page: str, 
        monitor_code: str, 
        date: str, 
        format_date: str,
        rounded_price: bool,
        order: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los cambios diarios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - date: Fecha.
    """
    return get_monitor_data(currency, page, monitor_code, date, date, 'daily', format_date, rounded_price, order)

def get_price_converted(currency: str, type: str, value: Union[int, float], page: str, monitor_code: str) -> Union[float, Dict[str, str]]:
    """
    Convierte un valor de una moneda a otra.

    - currency: Moneda.
    - type: Tipo de conversión. (VES, USD, EUR).
    - value: Valor a convertir.
    """
    monitor = get_page_or_monitor(currency, page, monitor_code, 'default', False)
    result = _currency_converter(type, float(value), monitor)

    return result