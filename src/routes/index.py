from flask import Blueprint, render_template

route = Blueprint('index', __name__)

@route.get('/', defaults={'path': ''})
@route.get('/<path:path>')
def index(path: str):
    return render_template('index.html')