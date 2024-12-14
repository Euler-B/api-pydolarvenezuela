from typing import Any, Dict, List
from ..._dataclass import Monitor, Page

class Base:
    PAGE: Page = None
    
    @classmethod
    def _load(cls, **kwargs) -> List[Dict[str, Any]]:
        raise NotImplementedError
    
    @classmethod
    def get_values(cls, **kwargs) -> List[Dict[str, Any]]:
        try:
            result = cls._load(**kwargs)
            if not result:
                raise Exception(f'({cls.PAGE.name}) - Monitores no encontrados')
            return [Monitor(**monitor) for monitor in result]
        except Exception as e:
            raise e