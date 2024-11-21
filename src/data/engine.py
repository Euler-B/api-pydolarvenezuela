from sqlalchemy import create_engine
from ..consts import URL_DB
from .models import Base

engine = create_engine(URL_DB, pool_size=20, max_overflow=20)
Base.metadata.create_all(engine)