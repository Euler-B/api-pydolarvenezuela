from typing import Literal
from flask import Blueprint, request, jsonify
from ..decorators import token_required, handle_exceptions
from ..service import (
    get_page_or_monitor,
    get_price_converted,
    get_history_prices, 
    get_daily_changes as get_daily_changes_,
    _validate_date
)

route = Blueprint('monitors', __name__)

@route.get('/<string:currency>')
@token_required
@handle_exceptions
def get_monitor_by_page_or_monitor(currency: Literal['dollar', 'euro']):
    page    = request.args.get('page')
    monitor = request.args.get('monitor')
    format_date = request.args.get('format_date', 'default')
    rounded_price = True if request.args.get('rounded_price', 'true') == 'true' else False

    response = get_page_or_monitor(currency, page, monitor, format_date, rounded_price)
        
    return jsonify(response), 200

@route.get('/<string:currency>/history')
@token_required
@handle_exceptions
def get_history(currency: Literal['dollar', 'euro']):
    page = request.args.get('page')
    monitor = request.args.get('monitor')
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')
    format_date = request.args.get('format_date', 'default')
    rounded_price = True if request.args.get('rounded_price', 'true') == 'true' else False

    if not all([page, monitor, start_date, end_date]):
        raise ValueError('Por favor, proporciona los parametros: (page, monitor, start_date y end_date).')
    
    for date in [start_date, end_date]:
        _validate_date(date)

    response = get_history_prices(currency, page, monitor, start_date, end_date, format_date, rounded_price)
    return jsonify(response), 200

@route.get('/<string:currency>/changes')
@token_required
@handle_exceptions
def get_daily_changes(currency: Literal['dollar', 'euro']):
    page = request.args.get('page')
    monitor = request.args.get('monitor')
    date = request.args.get('date')
    format_date = request.args.get('format_date', 'default')
    rounded_price = True if request.args.get('rounded_price', 'true') == 'true' else False

    if not all([page, monitor, date]):
        raise ValueError('Por favor, proporciona los parametros: (page, monitor y date).')
    
    _validate_date(date)

    response = get_daily_changes_(currency, page, monitor, date, format_date, rounded_price)
    return jsonify(response), 200

@route.get('/<string:currency>/conversion')
@token_required
@handle_exceptions
def value_conversion(currency: Literal['dollar', 'euro']):
    type    = request.args.get('type')
    value   = request.args.get('value')
    page    = request.args.get('page')
    monitor = request.args.get('monitor')

    if not all([type, value, page, monitor]):
        raise ValueError('Por favor, proporciona los parametros: (type, value y monitor).')
    
    response = get_price_converted(currency, type, value, page, monitor)
    return jsonify(response), 200