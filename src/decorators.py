from functools import wraps
from flask import request
from sqlalchemy.orm import sessionmaker
from .data.engine import engine
from .data.services import is_user_valid
from .core import limiter
from .consts import TOKEN_SECRET
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
        
        if not token and request.path in ['/api/v1/dollar/history', '/api/v1/dollar/changes']:
            raise HTTPException(401, "Requiere un token de autenticación.")
        
        if not token:
            @limiter.limit("500 per hour", key_func=_get_ip)
            def limited_func():
                return f(*args, **kwargs)
            return limited_func()

        if token and not is_user_valid(session, token):
            raise HTTPException(401, "Token inválido.")
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
            error = exception_map.get(type(e), 500)
            raise HTTPException(error, str(e))
    return decorated