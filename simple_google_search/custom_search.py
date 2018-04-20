import json
import requests
from .logger import logger


class CustomSearch:

    URL = 'https://www.googleapis.com/customsearch/v1'

    def __init__(self, api_key, cse_id):
        self._api_key = api_key
        self._cse_id = cse_id

    def _build_params(self, query):
        params = {
            'cx': self._cse_id,
            'key': self._api_key,
            'q': query,
        }

        return params

    def _call(self, query):
        params = self._build_params(query)

        try:
            res = requests.get(self.URL, params=params)
        except requests.RequestException as e:
            logger.error(str(e))
            return None

        if res.status_code != requests.codes.ok:
            if hasattr(res, 'text'):
                logger.error(res.text)
            else:
                logger.error('Something error occured.')
            return None

        return res.json()

    def search(self, query):
        search_result = self._call(query)

        return search_result['items'] if search_result else []
