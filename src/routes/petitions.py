from typing import Callable
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..data.engine import engine
from ..utils.cache import CacheHistoryPetition
from ..decorators import token_required, handle_exceptions
from ..data.services.user_petitions_db import (
    get_hourly_totals_24h,
    get_daily_totals_7d,
    get_daily_totals_30d
)

route = Blueprint('petitions', __name__)

def _get_hourly_or_daily_totals(func: Callable, path: str, token: str) -> list:
    cache = CacheHistoryPetition(path.split('/')[-1].replace('-', '_'), token.split(' ')[1])
    if cache.get(): return cache.get()

    with Session(engine) as session:
        cache.set(func(session, token))
    return cache.get()

@route.get('/hourly-totals-24h')
@token_required
@handle_exceptions
def hourly_totals_24h():
    token = request.headers.get('Authorization')

    response = _get_hourly_or_daily_totals(get_hourly_totals_24h, request.path, token)
    return jsonify(response)
    
@route.get('/daily-totals-7d')
@token_required
@handle_exceptions
def daily_totals_7d():
    token = request.headers.get('Authorization')

    response = _get_hourly_or_daily_totals(get_daily_totals_7d, request.path, token)
    return jsonify(response)
    
@route.get('/daily-totals-30d')
@token_required
@handle_exceptions
def daily_totals_30d():
    token = request.headers.get('Authorization')

    response = _get_hourly_or_daily_totals(get_daily_totals_30d, request.path, token)
    return jsonify(response)