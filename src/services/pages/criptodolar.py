import json
from ...utils.request import request
from ...utils.time import get_formatted_date_tz
from ...utils.common import _convert_specific_format, _convert_dollar_name_to_monitor_name
from ...utils.extras import list_monitors_images
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
                image = next((image.image for image in list_monitors_images if image.provider == 'criptodolar' and image.title == _convert_specific_format(
                        _convert_dollar_name_to_monitor_name(monitor['name']))), None)
                key = _convert_specific_format(_convert_dollar_name_to_monitor_name(monitor['name']))
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