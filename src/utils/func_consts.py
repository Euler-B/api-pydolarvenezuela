from typing import Union
from .extras import LIST_IMAGES_URL
from ..consts import PROVIDERS, CURRENCIES

def get_provider(provider: str) -> Union[str, None]:
    """
    Obtiene el proveedor de la lista de proveedores.
    """
    for key, value in PROVIDERS.items():
        if provider.lower() == value['id'].lower():
            return key
    return None
        
def get_currency(currency: str) -> Union[str, None]:
    """
    Obtiene la moneda de la lista de monedas.
    """
    return CURRENCIES.get(currency.lower())

def get_url_image(provider: str, monitor: str) -> Union[str, None]:
    """
    Obtiene la URL de la imagen del proveedor.
    """
    for obj in LIST_IMAGES_URL:
        if obj['provider'].lower() == provider.lower() and obj['title'].lower() == monitor.lower():
            return obj['image']
    return None