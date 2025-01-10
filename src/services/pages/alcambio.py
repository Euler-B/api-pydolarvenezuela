import json
from ...utils.request import request
from ...utils.time import get_formatted_timestamp
from ...utils.func_consts import get_url_image
from ..._pages import AlCambio
from ._base import Base

class AlCambioService(Base):
    PAGE = AlCambio

    @classmethod
    def _load(cls, **kwargs):
        response = request('POST', (cls.PAGE.name, cls.PAGE.provider))
        response = json.loads(response)

        rates = []
        country_conversions = response['data']['getCountryConversions']
        rate_types = ['PRIMARY', 'SECONDARY']

        for rate in country_conversions['conversionRates']:
            if rate['type'] in rate_types:
                name  = 'EnParaleloVzla' if not rate['official'] else 'BCV'
                key   = name.lower()
                date  = get_formatted_timestamp(country_conversions['dateParalelo'] if not rate['official'] else country_conversions['dateBcv'])
                image = get_url_image(cls.PAGE.name, key)
                rates.append({
                    'key': key,
                    'title': name,
                    'price': rate['baseValue'],
                    'last_update': date,
                    'image': image
                })
                rate_types.remove(rate['type'])

            if not rate_types:
                break
            
        return rates