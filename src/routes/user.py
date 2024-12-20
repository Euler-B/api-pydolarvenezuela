from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..data.engine import engine
from ..decorators import token_required, handle_exceptions
from ..data.services.users_db import get_user_id, get_user, is_user_valid, change_user_name

route = Blueprint('users', __name__)

@route.post('/validate-token')
@handle_exceptions
def validate_token():
    token = request.headers.get('Authorization')
    
    with Session(engine) as session:
        return jsonify({'success': is_user_valid(session, token)})
    
@route.get('/get-user')
@token_required
@handle_exceptions
def get_user_data():
    token = request.headers.get('Authorization')
    
    with Session(engine) as session:
        user_id = get_user_id(session, token)
        return jsonify(get_user(session, user_id))
    
@route.put('/change-name')
@token_required
@handle_exceptions
def change_name():
    token = request.headers.get('Authorization')
    name = request.get_json().get('name')

    if not name:
        raise ValueError('name es requerido')
    
    with Session(engine) as session:
        user_id = get_user_id(session, token)
        change_user_name(session, user_id, name)
        return jsonify({'success': True})