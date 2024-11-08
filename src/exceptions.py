from typing import Optional
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from dataclasses import dataclass

exception_map = { 
    KeyError: 404,
    ValueError: 400,
}

@dataclass
class HTTPException(Exception):
    code: Optional[int] = 500
    message: Optional[str] = "Unknown Error"
    response: Optional[str] = None

    def __post_init__(self):
        self.response = HTTP_STATUS_CODES.get(self.code, "Unknown Error").upper()

def handle_http_exception(e: HTTPException):
    return jsonify(
        {
            "error": e.response, 
            "message": e.message
        }
    ), e.code

# handle default exceptions

def page_not_found(e):
    result = HTTPException(404, "No se pudo encontrar la página que estaba buscando. Por favor, consulta la documentación en: https://github.com/fcoagz/api-pydolarvenezuela")
    return handle_http_exception(result)

def forbidden(e):
    result = HTTPException(403, "El servidor entendió la solicitud, pero se niega a autorizarla.")
    return handle_http_exception(result)

def method_not_allowed(e):
    result = HTTPException(405, "El método de solicitud no es compatible con la funcionalidad de la página.")
    return handle_http_exception(result)

def internal_server_error(e):
    result = HTTPException(500, "Error interno del servidor.")
    return handle_http_exception(result)

def gateway_timeout(e):
    result = HTTPException(504, "El servidor no pudo responder a tiempo.")
    return handle_http_exception(result)