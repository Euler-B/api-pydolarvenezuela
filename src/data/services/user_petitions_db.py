import json
from typing import List
from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ...utils.cache import CacheHistoryPetition
from ..models import UserPetition
from .users_db import get_user_id

def _get_hourly_totals_by_day(query: List[UserPetition]) -> dict: 
    results = {'total': 0, 'paths': defaultdict(list)}
    days = defaultdict(dict)

    for day in query:
        date = day.created_at.strftime('%Y-%m-%d')
        
        if day.path not in days[date]:
            days[date][day.path] = 0

        days[date][day.path] += day.total_petitions

    for date, paths in days.items():
        for path, total_petitions in paths.items():
            results['paths'][path].append({
                'date': date,
                'total_petitions': total_petitions
            })
            results['total'] += total_petitions
    return results

def create_user_petition(session: Session, token: str, path: str, total_petitions: int) -> None:
    user_id = get_user_id(session, token)
    
    session.add(UserPetition(user_id=user_id, path=path, total_petitions=total_petitions, created_at=datetime.now()))
    session.commit()

def get_hourly_totals_24h(session: Session, token: str) -> list:
    last_24h = datetime.now() - timedelta(hours=24)
    user_id = get_user_id(session, token)

    cache = CacheHistoryPetition('hourly_totals_24h', user_id)
    if cache.get(): return cache.get()

    query = session.query(UserPetition).filter(UserPetition.created_at >= last_24h, UserPetition.user_id == user_id).all()
    results = {'total': 0, 'paths': defaultdict(list)}
    for hour in query:
        results['paths'][hour.path].append({
            'time': hour.created_at.strftime('%H:00'),
            'total_petitions': hour.total_petitions
        })
        results['total'] += hour.total_petitions

    cache.set(results)
    return results

def get_daily_totals_7d(session: Session, token: str) -> list:
    last_7d = datetime.now() - timedelta(days=7)
    user_id = get_user_id(session, token)

    cache = CacheHistoryPetition('daily_totals_7d', user_id)
    if cache.get(): return cache.get()

    query = session.query(UserPetition).filter(UserPetition.created_at >= last_7d, UserPetition.user_id == user_id).all()
    results = _get_hourly_totals_by_day(query)
    cache.set(results)
    
    return results

def get_daily_totals_30d(session: Session, token: str) -> list:
    last_30d = datetime.now() - timedelta(days=30)
    user_id = get_user_id(session, token)

    cache = CacheHistoryPetition('daily_totals_30d', user_id)
    if cache.get(): return cache.get()

    query = session.query(UserPetition).filter(UserPetition.created_at >= last_30d, UserPetition.user_id == user_id).all() 
    results = _get_hourly_totals_by_day(query)
    cache.set(results)
    
    return results
