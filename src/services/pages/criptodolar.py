import json
from ...utils.request import request
from ...utils.time import get_formatted_date_tz
from ...utils.common import _convert_specific_format, _convert_dollar_name_to_monitor_name
from ...utils.func_consts import get_url_image
from ..._pages import CriptoDolar
from ._base import Base

class CriptoDolarService(Base):
    PAGE = CriptoDolar

    @classmethod
    def _load(cls, **kwargs):
        response = request('GET', (cls.PAGE.name, f'{cls.PAGE.provider}coins/latest'), params={'type': 'bolivar', 'base': kwargs.get('currency', 'usd')})
        response = json.loads(response)
        data = []

        for monitor in response:
            if monitor['type'] in ['bolivar', 'bancove']:
                key = _convert_specific_format(_convert_dollar_name_to_monitor_name(monitor['name']))
                image = get_url_image(cls.PAGE.name, key)
                title = _convert_dollar_name_to_monitor_name(monitor['name'])
                price = round(monitor['price'], 2)
                last_update = get_formatted_date_tz(monitor['updatedAt'])

                data.append({
                    'key': key,
                    'title': title,
                    'price': price,
                    'last_update': last_update,
                    'image': image
                })

        return data