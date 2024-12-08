from typing import Union
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