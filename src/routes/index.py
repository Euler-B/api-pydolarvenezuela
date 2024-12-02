from flask import Blueprint, render_template
from ..decorators import handle_exceptions

route = Blueprint('index', __name__)

@route.get('/', defaults={'path': ''})
@route.get('/<path:path>')
@handle_exceptions
def index(path: str = None):
    return render_template('index.html')