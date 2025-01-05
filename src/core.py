"""https://github.com/alisaifee/flask-limiter/issues/46"""
import logging
from typing import Literal
from redis import Redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .consts import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB

if not all([REDIS_HOST, REDIS_PORT, REDIS_PASSWORD]):
    raise ValueError('Missing REDIS_HOST, REDIS_PORT or REDIS_PASSWORD environment variables')

try:
    cache = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=REDIS_DB,
        decode_responses=True
    )
    cache.ping()
except Exception as e:
    raise e

limiter = Limiter(
    get_remote_address,
    storage_uri=f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)

class Logger:
    shared_handler = None

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        if not Logger.shared_handler:
            Logger.shared_handler = logging.StreamHandler()
            Logger.shared_handler.setFormatter(
                logging.Formatter('%(levelname)s - [%(asctime)s] - %(message)s')
            )
        
        self.logger.addHandler(Logger.shared_handler)
    
    def _log(self, message: str, level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'):
        self.logger.log(getattr(logging, level), message)
    
    def info(self, message: str):
        self._log(message, 'INFO')

    def debug(self, message: str):
        self._log(message, 'DEBUG')

    def warning(self, message: str):
        self._log(message, 'WARNING')

    def error(self, message: str):
        self._log(message, 'ERROR')  

    def critical(self, message: str):
        self._log(message, 'CRITICAL')

logger = Logger('pydolarapi')