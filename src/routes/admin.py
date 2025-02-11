from flask import Blueprint, request, jsonify, send_file
from sqlalchemy.orm import Session
from ..decorators import token_required_admin, handle_exceptions
from ..data.engine import engine
from ..data.services.users_db import (
    create_user as _create_user_,
    modificate_user as _modificate_user_,
    delete_user as _delete_user_,
    get_users as _get_users_
)
from ..data.services.monitors_db import (
    modificate_monitor as _modificate_monitor_,
    delete_page as _delete_page_
)

route   = Blueprint('admin', __name__)

# Users 

@route.post('/create-user')
@token_required_admin
@handle_exceptions
def create_user():
    name = request.form.get('name')
    
    if not name:
        raise ValueError('Falta el nombre del usuario.')
    
    with Session(engine) as session:
        token = _create_user_(session, name)
    return jsonify({"message": "Usuario creado exitosamente.", "token": token}), 200

@route.get('/get-users')
@token_required_admin
@handle_exceptions
def get_users_route():
    with Session(engine) as session:
        users = _get_users_(session)
    return jsonify(users), 200

@route.put('/modificate-user')
@token_required_admin
@handle_exceptions
def modificate_user():
    id_user = request.form.get('id')
    is_premium = request.form.get('is_premium')

    if not all([id_user, is_premium]):
        raise ValueError('Falta el id del usuario o el estado de premium.')
    
    with Session(engine) as session:
        _modificate_user_(session, id_user, is_premium)
    return jsonify({"message": "Usuario modificado exitosamente."}), 200

@route.delete('/delete-user')
@token_required_admin
@handle_exceptions
def delete_user():
    id_user = request.form.get('id')
    
    if not id_user:
        raise ValueError('Falta el id del usuario.')
    
    with Session(engine) as session:
        _delete_user_(session, id_user)
    return jsonify({"message": "Usuario eliminado exitosamente."}), 200
    
# Monitors

@route.get('/reload-monitors')
@token_required_admin
@handle_exceptions
def reload_monitors():
    from ..cron import reload_monitors
    
    reload_monitors()
    return jsonify({"message": "Monitores recargados exitosamente."}), 200

@route.put('/modificate-monitor')
@token_required_admin
@handle_exceptions
def modificate_monitor():
    form = request.form.to_dict()
    page = form.pop('page', None)
    currency = form.pop('currency', None)
    monitor  = form.pop('monitor', None)
    update   = form.pop('update', False)

    if not all([page, currency, monitor]):
        raise ValueError('Falta el nombre de la página o la moneda o el monitor.')
    
    if not form:
        raise ValueError('No se proporcionaron los datos a modificar.')

    with Session(engine) as session:
        _modificate_monitor_(session, page, currency, monitor, form, update)
    return jsonify({"message": "Monitor modificado exitosamente."}), 200

@route.delete('/delete-page')
@token_required_admin
@handle_exceptions
def delete_page():
    name = request.form.get('name')
    if not name:
        raise ValueError('Falta el nombre de la página.')
    
    with Session(engine) as session:
        _delete_page_(session, name)
    return jsonify({"message": "Página eliminada exitosamente."}), 200

# Backup

@route.get('/get-backup')
@token_required_admin
@handle_exceptions
def get_backup():
    from ..backup import backup
    
    response = backup()
    if not response['success']:
        raise ValueError(response['message'])
    
    return send_file(response['path'], as_attachment=True, mimetype='application/sql'), 200 