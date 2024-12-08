from ..consts import PROVIDERS, CURRENCIES

def get_provider(provider: str) -> str:
    """
    Obtiene el proveedor de la lista de proveedores.
    """
    for key, value in PROVIDERS.items():
        if provider.lower() in value['id'].lower():
            return key
    return provider
        
def get_currency(currency: str) -> str:
    """
    Obtiene la moneda de la lista de monedas.
    """
    return CURRENCIES.get(currency.lower())