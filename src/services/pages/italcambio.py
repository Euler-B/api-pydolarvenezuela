from datetime import datetime
from bs4 import BeautifulSoup
from ...utils.request import request
from ...utils.time import standard_time_zone
from ...utils.extras import code_currencies
from ..._pages import Italcambio
from ._base import Base

class ItalcambioService(Base):
    PAGE = Italcambio

    @classmethod
    def _load(cls, **kwargs):
        response = request('GET', (cls.PAGE.name, cls.PAGE.provider))
        soup = BeautifulSoup(response, 'html.parser')
        section_currencies_italcambio = soup.find('div', 'container-fluid compra')
        monitors_amounts = [
            x.text for x in section_currencies_italcambio.find_all('p', 'small')
            ]

        rates = []
        for i in range(len(monitors_amounts)):
            if i%2 == 0:
                if monitors_amounts[i] in code_currencies:
                    title = code_currencies[monitors_amounts[i]]
                    key = monitors_amounts[i].lower()
                    price_old = float(str(monitors_amounts[i+1]).split()[-1])
                    price = price_old
                    last_update = datetime.now(standard_time_zone)

                    rates.append({
                        'key': key,
                        'title': title,
                        'price': price,
                        'last_update': last_update
                    })

        return rates