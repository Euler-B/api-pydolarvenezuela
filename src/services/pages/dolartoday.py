import json
from datetime import datetime
from ...utils.request import request
from ...utils.extras import list_monitors_images
from ...utils.common import _convert_specific_format, _convert_dollar_name_to_monitor_name
from ...utils.time import standard_time_zone
from ..._pages import DolarToday
from ._base import Base

class DolarTodayService(Base):
    PAGE = DolarToday

    @classmethod
    def _load(cls, **kwargs):
        response = request('POST', (cls.PAGE.name, f'{cls.PAGE.provider}wp-admin/admin-ajax.php'), data={
            'action': 'dt_currency_calculator_handler',
            'amount': '1'})
        response = json.loads(response)
        data = []

        for key, value in response.items():
            title = _convert_dollar_name_to_monitor_name(key)
            key = _convert_specific_format(title)
            image = next((image.image for image in list_monitors_images if image.provider == 'dolartoday' and image.title == key), None)
            price = float(str(value).replace('Bs.', '').strip())   
            last_update = datetime.now(standard_time_zone)

            data.append({
                'key': key,
                'title': title,
                'price': price,
                'last_update': last_update,
                'image': image
            })

        return data