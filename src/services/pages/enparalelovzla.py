import re
from bs4 import BeautifulSoup
from ...utils.request import request
from ...utils.extras import list_monitors_images
from ...utils.time import get_formatted_date
from ..._pages import EnParaleloVzla
from ._base import Base

PATTERN = r"(🗓|🕒|💵|🔺|🔻|🟰)|Bs\. (\d{2},\d{2})"

class EnParaleloVzlaService(Base):
    PAGE = EnParaleloVzla

    @classmethod
    def _load(cls, **kwargs):
        html = request('GET', (cls.PAGE.name, cls.PAGE.provider))
        soup = BeautifulSoup(html, 'html.parser')
        
        widget_messages = soup.find_all('div', 'tgme_widget_message_wrap js-widget_message_wrap')
        last_occurrences = []

        for widget in widget_messages:
            message = widget.find('div', 'tgme_widget_message text_not_supported_wrap js-widget_message')
            
            if message is None:
                continue
            
            data_message = message.find('div', 'tgme_widget_message_bubble')
            text_message = data_message.find('div', 'tgme_widget_message_text js-message_text')
                
            if text_message is None:
                continue
            
            result = re.findall(PATTERN, text_message.text.strip())
            if result and cls._is_valid_message(result):   
                price = cls._extract_price(result)

                if price is not None:
                    last_update = get_formatted_date(cls._get_date_message(data_message))
                    image = next((image.image for image in list_monitors_images if image.provider == 'enparalelovzla' and image.title == 'enparalelovzla'), None)

                    data = {
                        'key': 'enparalelovzla',
                        'title': 'EnParaleloVzla',
                        'price': price,
                        'last_update': last_update,
                        'image': image
                    }
                    last_occurrences.append(data)
        return [last_occurrences[-1]] if last_occurrences else None
    
    @classmethod
    def _is_valid_message(cls, result: list):
        return len([emoji[0] for emoji in result if emoji[0]]) == 4

    @classmethod
    def _extract_price(cls, result: list):
        value = ''.join([r[-1] for r in result if r[-1]]).replace(',', '.')
        return float(value) if value else None
    
    @classmethod
    def _get_date_message(cls, data_message: BeautifulSoup):
        return data_message.find('div', 'tgme_widget_message_info short js-message_info').find('time').get('datetime')