import asyncio
from urllib.parse import urlparse
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..data.engine import engine
from ..decorators import token_required, handle_exceptions
from ..data.services.webhooks_db import (
    create_webhook as _create_webhook_,
    delete_webhook as _delete_webhook_,
    get_webhook as _get_webhook_,
    raise_webhook_exists_error
)
from ..services.webhooks import send_webhook as _send_webhook_, send_webhooks

route = Blueprint('webhook', __name__)

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
    
    parsed_url = urlparse(url)

    if not parsed_url.scheme in ['http', 'https']:
        raise ValueError('La url debe ser http o https')
    if not parsed_url.hostname:
        raise ValueError('La url debe tener un hostname')
    if not parsed_url.path:
        raise ValueError('La url debe tener un path')
    if parsed_url.hostname in ['localhost', '']:
        raise ValueError('La url no puede ser una dirección local')
    
    if token_secret.startswith('Bearer '):
        token_secret = token_secret.replace('Bearer ', '')

    with Session(engine) as session:
        raise_webhook_exists_error(session, token_user) # Check if webhook exists

        # Procesing webhook
        asyncio.run(_send_webhook_(url, token_secret, certificate_ssl)) # Send webhook to verify the url
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

    with Session(engine) as session:
        _delete_webhook_(session, token_user)

    return jsonify({"message": "Webhook eliminado con éxito"}), 200

@route.get('/get-webhook')
@token_required
@handle_exceptions
def get_webhook():
    token_user = request.headers.get('Authorization')

    with Session(engine) as session:
        webhook = _get_webhook_(session, token_user)
    return jsonify(webhook), 200

@route.post('/test-webhook')
@token_required
@handle_exceptions
def test_webhook():
    token_user = request.headers.get('Authorization')

    send_webhooks(True, token_user=token_user)
    return jsonify({"message": "Webhook enviado con éxito"}), 200