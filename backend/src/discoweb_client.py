import requests
from datetime import date
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


@dataclass
class Result:
    data: list[any]
    page: int
    total_pages: int


def extract_pagination(api_result) -> tuple[int, int]:
    try:
        page = api_result['meta']['pagination']['currentPage']
        total_pages = api_result['meta']['pagination']['totalPages']
    except Exception as e:
        logger.warning(f"Problem with pagination: {api_result} {e}")
        page = 0
        total_pages = 1
    return page,total_pages


class DiscosWebClient:

    def __init__(self, token: str, url: str = 'https://discosweb.esoc.esa.int/api/'):
        self.headers = {
            'Authorization': f'Bearer {token}',
            'DiscosWeb-Api-Version': '2',
        }
        self.url = url

    def get(self, path: str, params: dict = None) -> dict:
        url = f'{self.url}{path}'
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        result = response.json()
        return result

    def get_objects_by_reentry(self, object_class: str, begin: date, end: date,
                               sort_by: str = 'reentry.epoch',
                               page_size: int = 30, page: int = 1) -> Result:
        params = {
            'filter': f"eq(objectClass,{object_class})&ge(reentry.epoch,epoch:'{begin}')&le(reentry.epoch,epoch:'{end}')",
            'sort': f'{sort_by}',
            'page[size]': f'{page_size}',
            'page[number]': f'{page}',

        }
        api_result = self.get('objects', params)

        page, total_pages = extract_pagination(api_result)
        return Result(api_result['data'], page, total_pages)

    def get_payloads_by_reentry(self, begin: date, end: date, page_size: int = 30, page: int = 1) -> Result:
        return self.get_objects_by_reentry('Payload', begin, end, page_size=page_size, page=page)

    def get_launches(self, begin: date, end: date,
                     page_size: int = 30, page: int = 1
                     ) -> Result:
        params = {
            'filter': f"ge(epoch,epoch:'{begin}')&le(epoch,epoch:'{end}')",
            'page[size]': f'{page_size}',
            'page[number]': f'{page}',

        }
        api_result = self.get('launches', params)

        page, total_pages = extract_pagination(api_result)
        return Result(api_result['data'], page, total_pages)

    def get_reentries(self, begin: date, end: date,
                      page_size: int = 30, page: int = 1
                      ) -> Result:
        params = {
            'filter': f"ge(epoch,epoch:'{begin}')&le(epoch,epoch:'{end}')",
            'page[size]': f'{page_size}',
            'page[number]': f'{page}',

        }
        api_result = self.get('reentries', params)

        page,total_pages= extract_pagination(api_result)
        return Result(api_result['data'], page, total_pages)
