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
    'Al Cambio': 'alcambio',
    'Banco Central de Venezuela': 'bcv',
    'Cripto Dolar': 'criptodolar',
    'Dolar Today': 'dolartoday',
    'EnParaleloVzla': 'enparalelovzla',
    'Italcambio': 'italcambio'
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
            ('16:00', '18:00')
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

URL_DB  = f'{SQL_MOTOR}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}'