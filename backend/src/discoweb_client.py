import requests
from datetime import date
from dataclasses import dataclass


@dataclass
class Result:
    data: list[any]
    page: int
    total_pages: int


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
        return response.json()

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
        pagination = api_result['meta']['pagination']
        return Result(api_result['data'], pagination['currentPage'], pagination['totalPages'])

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
        pagination = api_result['meta']['pagination']
        return Result(api_result['data'], pagination['currentPage'], pagination['totalPages'])