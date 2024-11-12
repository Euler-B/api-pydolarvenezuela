from typing import Literal
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from ..data.engine import engine
from ..decorators import token_required, handle_exceptions
from ..data.services.webhooks_db import (
    send_webhook as _send_webhook_,
    create_webhook as _create_webhook_,
    delete_webhook as _delete_webhook_,
    get_webhook as _get_webhook_
)

route = Blueprint('webhook', __name__)
session = sessionmaker(bind=engine)()

@route.post('/set-webhook')
@token_required
@handle_exceptions
def set_webhook():
    token_user = request.headers.get('Authorization')

    data = request.json
    url = data.get('url') 
    certificate_ssl = data.get('certificate_ssl', True) 
    token_secret = data.get('token_secret') 
    monitors = data.get('monitors')

    if not url or not token_secret or not monitors:
        raise ValueError(f'{'url' if not url else 'token_secret' if not token_secret else 'monitors'} es requerido')
    
    if not isinstance(monitors, list):
        raise ValueError('Monitors debe ser una lista de diccionarios')
    if not len(monitors) <= 3:
        raise ValueError('Monitors debe tener un máximo de 3 monitores')
    if not all(isinstance(monitor, dict) for monitor in monitors):
        raise ValueError('Monitors debe ser una lista de diccionarios')

    # Procesing webhook
    _send_webhook_(url, token_secret, certificate_ssl) # Send webhook to verify the url
    _create_webhook_(session, token_user, 
                     url=url, 
                     token=token_secret, 
                     certificate_ssl=certificate_ssl, 
                     monitors=monitors)
    
    return jsonify({"message": "Webhook creado con éxito"}), 201
    
@route.delete('/del-webhook')
@token_required
@handle_exceptions
def del_webhook():
    token_user = request.headers.get('Authorization')

    _delete_webhook_(session, token_user)
    return jsonify({"message": "Webhook eliminado con éxito"}), 200

@route.get('/get-webhook')
@token_required
@handle_exceptions
def get_webhook():
    token_user = request.headers.get('Authorization')

    webhook = _get_webhook_(session, token_user)
    return jsonify(webhook), 200