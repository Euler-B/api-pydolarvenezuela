from babel.dates import format_date, format_time
from datetime import datetime
from pytz import timezone, utc

standard_time_zone = timezone('America/Caracas')

def get_datestring_to_datetime(date_string: str):
    """
    Formatear string a datetime.
    """
    datetime_obj = datetime.now(standard_time_zone)
    try:
        return datetime_obj.strptime(date_string, '%d/%m/%Y, %I:%M %p')
    except ValueError:
        return datetime_obj.strptime(date_string, '%d/%m/%Y').astimezone(standard_time_zone)

def get_formatted_timestamp(date_timestamp_ms: int):
    """
    Formatear milisegundos a datetime.
    """
    timestamp_s  = date_timestamp_ms / 1000.0
    return datetime.fromtimestamp(timestamp_s, standard_time_zone)

def get_formatted_date_bcv(date_string: str):
    """
    Formatear datetime.
    """
    return datetime.fromisoformat(date_string).astimezone(standard_time_zone)

def get_formatted_date(date_string: str):
    """
    Formatear datetime.
    """
    return datetime.fromisoformat(date_string).astimezone(standard_time_zone)


def get_formatted_date_tz(date_string: str):
    """
    Formatear datetime desde TZ.
    """
    dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=utc)
    return dt.astimezone(standard_time_zone)


def get_time(date_string: str):
    """
    Formatear datetime.
    """
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M')

def get_time_zone():
    """
    Obtener la hora actual de Venezuela.
    """
    datetime_obj = datetime.now(standard_time_zone)

    formatted_date = format_date(datetime_obj.date(), format='full', locale='es')
    formatted_time = format_time(datetime_obj.time(), format='h:mm:ss a', locale='es')

    return {
        "date": formatted_date,
        "time": formatted_time
    }