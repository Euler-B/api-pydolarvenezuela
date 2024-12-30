from functools import wraps
from flask import request
from sqlalchemy.orm import sessionmaker
from .data.engine import engine
from .data.services.users_db import is_user_valid
from .utils.cache import CacheUserPetition
from .core import limiter
from .consts import TOKEN_SECRET, CURRENCY_ROUTES
from .exceptions import HTTPException, exception_map

session = sessionmaker(bind=engine)()

def _get_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        return request.remote_addr

def token_required_admin(f):
    """
    Token de autenticación requerido para acceder a las rutas Admin.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if token != TOKEN_SECRET:
            raise HTTPException(401, "Token inválido.")
                
        return f(*args, **kwargs)
    return decorated

def token_required(f):
    """
    Token de autenticación opcional pero requerido para acceder a las rutas User.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token and not request.path.split('/')[-1] in ['dollar', 'euro', 'conversion']:
            raise HTTPException(401, "Requiere un token de autenticación.")
        
        if not token:
            @limiter.limit("500 per hour", key_func=_get_ip)
            def limited_func():
                return f(*args, **kwargs)
            return limited_func()

        if token and not is_user_valid(session, token):
            raise HTTPException(401, "Token inválido.")
        
        if request.path in [route for currency in CURRENCY_ROUTES.values() for route in currency]:
            CacheUserPetition(request.path, token.split(' ')[1]).set()

        return f(*args, **kwargs)
    return decorated

def handle_exceptions(f):
    """
    Validación de excepciones.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            error = exception_map.get(type(e), 500)
            raise HTTPException(error, str(e))
    return decorated