import requests
from datetime import date

class DiscoWebClient:

    def __init__(self, token: str, url: str = 'https://discosweb.esoc.esa.int/api/'):
        self.headers = {
            'Authorization': f'Bearer {token}',
            'DiscosWeb-Api-Version': '2',
        }

    def get(self, path: str, params: dict = None) -> dict:
        url = f'{self.url}{path}'
        response = requests.get(url,headers=self.headers,params=params)
        return response.json()

    def get_discos(self,object_class:str,begin_date:date,end_date:date, sort_by:str='reentry.epoch'):
        params = {
            'filter': f"eq(objectClass,{object_class})&gte(reentry.epoch,epoch:'{begin_date}')&lte(reentry.epoch,epoch:'{end_date}')",
            'sort': '-reentry.epoch',
        }
        return self.get('objects',params)