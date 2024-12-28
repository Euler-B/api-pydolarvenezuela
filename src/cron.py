import json
from datetime import datetime
from ._pages import (
    AlCambio, 
    BCV, 
    CriptoDolar, 
    DolarToday, 
    EnParaleloVzla, 
    Italcambio
)
from .services.pages import PageData
from .core import logger
from .consts import (
    TIME_ZONE,
    CURRENCIES,
    PROVIDERS,
    UPDATE_SCHEDULE
)
from ._provider import Provider
from .backup import backup
from .services.webhooks import send_webhooks
from .utils.cache import CacheProvider, CacheUserPetition
from .storage.dropbox import DropboxStorage
from .storage.telegram import TelegramStorage

pages    = [AlCambio, BCV, CriptoDolar, DolarToday, EnParaleloVzla, Italcambio]
monitors = [
    PageData(page, currency=currency)
    for currency in CURRENCIES.values() 
    for page in pages if currency in page.currencies
]

def update_data(name: str, monitor: PageData) -> None:
    """
    Obtiene los datos de un monitor y los guarda en caché.

    - name: Nombre del proveedor.
    - monitor: Instancia de Monitor.
    """
    try:
        provider = Provider(monitor.page, monitor.kwargs['currency'], monitor.get_values())
        CacheProvider(name, monitor.kwargs['currency']).set([m.__dict__ for m in provider.get_list_monitors()])
    except Exception as e:
        logger.warning(f'Error al obtener datos de {monitor.page.name}: {str(e)}')

def reload_monitors() -> None:
    """
    Recarga los datos de los monitores y los guarda en caché.
    """
    for monitor in monitors:
        name = PROVIDERS.get(monitor.page.name)['id']
        logger.info(f'Recargando datos de "{monitor.page.name}".')
        update_data(name, monitor)
    send_webhooks()

def job() -> None:
    """
    Itera sobre los monitores y actualiza los datos en caché.\n
    Actualiza los datos de un monitor si la hora actual está dentro del rango de actualización.
    """
    dt   = datetime.now(TIME_ZONE)
    _day_  = dt.strftime('%a')
    _hour_ = dt.strftime('%H:%M')

    for monitor in monitors:
        name = PROVIDERS.get(monitor.page.name)['id']
        
        if name not in UPDATE_SCHEDULE.keys():
            logger.info(f'Actualizando datos de "{monitor.page.name}".')
            update_data(name, monitor)
            continue

        if _day_ in UPDATE_SCHEDULE.get(name, {}).get('not', []):
            continue

        for start, end in UPDATE_SCHEDULE.get(name, {}).get('hours', []):
            if _hour_ >= start and _hour_ <= end:
                logger.info(f'Actualizando datos de "{monitor.page.name}".')
                update_data(name, monitor)
                break
    send_webhooks()

def generate_petitions() -> None:
    """
    Genera las peticiones de los usuarios y las guarda en la base de datos.
    """
    from sqlalchemy.orm import Session
    from .data.engine import engine
    from .data.services.user_petitions_db import create_user_petition as _create_user_petition_

    cache = CacheUserPetition()

    with Session(engine) as session:
        for user in cache.get_all_petitions_users():
            _create_user_petition_(session, **user)
        cache.delete_all_petitions_users()

def upload_backup_dropbox() -> None:
    """
    Sube el archivo de backup a Dropbox.
    """
    dropbox = DropboxStorage()

    try:
        response = backup()
        if not response['success']:
            raise Exception(response['message'])
        dropbox.upload(response['path'])
        logger.info('Backup subido a Dropbox.')
    except Exception as e:
        logger.error(f'Error al subir el archivo de backup a Dropbox: {str(e)}')

def upload_backup_telegram() -> None:
    """
    Sube el archivo de backup a Telegram.
    """
    telegram = TelegramStorage()

    try:
        response = backup()
        if not response['success']:
            raise Exception(response['message'])
        telegram.upload(response['path'])
        logger.info('Backup subido a Telegram.')
    except Exception as e:
        logger.error(f'Error al subir el archivo de backup a Telegram: {str(e)}')