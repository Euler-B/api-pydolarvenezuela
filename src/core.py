"""https://github.com/alisaifee/flask-limiter/issues/46"""
import logging
from redis import Redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .consts import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB

if not all([REDIS_HOST, REDIS_PORT, REDIS_PASSWORD]):
    raise ValueError('Missing REDIS_HOST, REDIS_PORT or REDIS_PASSWORD environment variables')

limiter = Limiter(
    get_remote_address,
    storage_uri="memory://"
)

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

logger    = logging.getLogger('pyDolarAPI')
logger.setLevel(logging.DEBUG)
handler   = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - [%(asctime)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)