from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..data.engine import engine
from ..decorators import token_required, handle_exceptions
from ..data.services.user_petitions_db import (
    get_hourly_totals_24h,
    get_daily_totals_7d,
    get_daily_totals_30d
)

route = Blueprint('petitions', __name__)

@route.get('/hourly-totals-24h')
@token_required
@handle_exceptions
def hourly_totals_24h():
    token_user = request.headers.get('Authorization')

    with Session(engine) as session:
        return jsonify(get_hourly_totals_24h(session, token_user))
    
@route.get('/daily-totals-7d')
@token_required
@handle_exceptions
def daily_totals_7d():
    token_user = request.headers.get('Authorization')

    with Session(engine) as session:
        return jsonify(get_daily_totals_7d(session, token_user))
    
@route.get('/daily-totals-30d')
@token_required
@handle_exceptions
def daily_totals_30d():
    token_user = request.headers.get('Authorization')

    with Session(engine) as session:
        return jsonify(get_daily_totals_30d(session, token_user))