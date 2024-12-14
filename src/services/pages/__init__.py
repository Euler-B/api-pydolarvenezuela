from typing import Any, Dict, List, Type
from ..._dataclass import Page
from ._base import Base
from .alcambio import AlCambioService
from .bcv import BCVService
from .criptodolar import CriptoDolarService
from .dolartoday import DolarTodayService
from .enparalelovzla import EnParaleloVzlaService
from .italcambio import ItalcambioService

PAGES: List[Type[Base]] = [
    AlCambioService, 
    BCVService, 
    CriptoDolarService, 
    DolarTodayService, 
    EnParaleloVzlaService, 
    ItalcambioService
]

class PageData:
    def __init__(self, page: Page, **kwargs) -> None:
        self.page = page
        self.kwargs = kwargs

    def get_values(self) -> List[Dict[str, Any]]:
        try:
            page_class = [p for p in PAGES if p.PAGE.name == self.page.name][0]
            return page_class.get_values(**self.kwargs)
        except Exception as e:
            raise e