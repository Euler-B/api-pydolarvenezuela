from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Page:
    name: str
    provider: str
    currencies: list

@dataclass
class Monitor:
    key: str
    title: str  
    price: float  
    price_old: Optional[float] = None 
    last_update: Optional[datetime] = None  
    image: Optional[str] = None  
    percent: Optional[float] = 0.0
    change: Optional[float] = 0.0  
    color: Optional[str] = "neutral" 
    symbol: Optional[str] = "" 

@dataclass
class HistoryPrice:
    price: float
    price_high: float
    price_low: float
    price_open: float
    last_update: datetime

@dataclass
class ChangePrice:
    price: float
    last_update: datetime

@dataclass
class Image:
    title: str
    image: str
    provider: str