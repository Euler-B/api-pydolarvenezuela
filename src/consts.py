import os
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()

SQL_MOTOR      = os.getenv('SQL_MOTOR')
SQL_HOST       = os.getenv('SQL_HOST')
SQL_DB_NAME    = os.getenv('SQL_DB_NAME')
SQL_PORT       = os.getenv('SQL_PORT')
SQL_USER       = os.getenv('SQL_USER')
SQL_PASSWORD   = os.getenv('SQL_PASSWORD')

REDIS_HOST     = os.getenv('REDIS_HOST')
REDIS_PORT     = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_DB       = os.getenv('REDIS_DB', 0) # default 0

TOKEN_SECRET   = os.getenv('TOKEN_SECRET')
TIMEOUT        = int(os.getenv('TIMEOUT', 15)) # in minutes

TIME_ZONE      = os.getenv('TIMEZONE', 'America/Caracas')
TIME_ZONE      = timezone(TIME_ZONE)

DROPBOX_TOKEN  = os.getenv('DROPBOX_TOKEN')
DROPBOX_APP_KEY    = os.getenv('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = os.getenv('DROPBOX_APP_SECRET')
DROPBOX_FOLDER     = os.getenv('DROPBOX_FOLDER', 'backup')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

DROPBOX_JOB = False if not all([DROPBOX_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET]) else True
TELEGRAM_JOB = False if not all([TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]) else True

PROVIDERS = {
    'Al Cambio': {
        'id': 'alcambio',
        'currencies': ['usd']
    },
    'Banco Central de Venezuela': {
        'id': 'bcv',
        'currencies': ['usd']
    },
    'Cripto Dolar': {
        'id': 'criptodolar',
        'currencies': ['usd', 'eur']
    },
    'Dolar Today': {
        'id': 'dolartoday',
        'currencies': ['usd']
    },
    'EnParaleloVzla': {
        'id': 'enparalelovzla',
        'currencies': ['usd']
    },
    'Italcambio': {
        'id': 'italcambio',
        'currencies': ['usd']
    }
}
CURRENCIES = {
    'dollar': 'usd',
    'euro': 'eur'
}
UPDATE_SCHEDULE = {
    'enparalelovzla': {
        'not': [
            'Sat', 'Sun'
        ], 'hours': [
            ('08:45', '10:00'),
            ('12:45', '14:00')
        ]
    },
    'alcambio': {
        'not': [
            'Sat', 'Sun'
        ], 'hours': [
            ('08:45', '10:00'),
            ('12:45', '14:00'),
            ('16:00', '18:00'),
            ('00:00', '01:00')
        ]
    },
    'bcv': {
        'not': [
            'Sat', 'Sun'
        ], 'hours': [
            ('16:00', '18:00')
        ]
    }
}

CURRENCY_ROUTES = {
    'dollar': ['/api/v1/dollar', '/api/v1/dollar/history', '/api/v1/dollar/changes', '/api/v1/dollar/conversion'],
    'euro': ['/api/v1/euro', '/api/v1/euro/history', '/api/v1/euro/changes', '/api/v1/euro/conversion'],
}

ALLOWED_ROUTES = [
    '', 
    'pricing', 
    'login', 
    'dashboard', 
    'dashboard/usage', 
    'dashboard/profile'
]

URL_DB  = f'{SQL_MOTOR}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}'