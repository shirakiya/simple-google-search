import re
from bs4 import BeautifulSoup
import requests


class GoogleSearch:

    SEARCH_URL = 'https://www.google.co.jp/search?q={}'

    regex_date = re.compile(r'\d+年\d+月\d+日 ... ')

    @classmethod
    def _extract_title(cls, card_bs):
        title_bs = card_bs.find('h3')
        return title_bs.string if title_bs else None

    @classmethod
    def _extract_description(cls, card_bs):
        st = card_bs.find('span', class_='st')

        if not st:
            return None

        raw_description = st.get_text()
        description = ''.join(raw_description.split('\n'))
        description = cls.regex_date.sub('', description)  # 冒頭の日付情報を削除する

        return description

    @classmethod
    def search(cls, query):
        html = requests.get(cls.SEARCH_URL.format(query)).text
        soup = BeautifulSoup(html, 'lxml')

        results = []

        for card_bs in soup.find_all('div', class_='g'):
            title = cls._extract_title(card_bs)
            if not title:
                continue
            description = cls._extract_description(card_bs)
            if not description:
                continue

            results.append({
                'title': title,
                'description': description,
            })

        return results
