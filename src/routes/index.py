import os
from flask import Blueprint, render_template, jsonify, request
from ..consts import ALLOWED_ROUTES
from ..exceptions import HTTPException
from ..decorators import handle_exceptions

route = Blueprint('index', __name__)

@route.get('/', defaults={'path': ''})
@route.get('/<path:path>')
@handle_exceptions
def index(path: str = None):
    is_html_exists = os.path.exists(f'src/www/dist/index.html')

    if request.path == '/' and not is_html_exists:
        return jsonify({'message': 'Welcome to PyDolarVenezuela API!'}), 200
    
    if path in ALLOWED_ROUTES:
        if not is_html_exists:
            raise HTTPException(500, "El frontend no está disponible.")
        return render_template('index.html')
    
    raise HTTPException(404, "No se pudo encontrar la página que estaba buscando. Por favor, consulta la documentación en: https://github.com/fcoagz/api-pydolarvenezuela")