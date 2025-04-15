from bdd_helper import Given, When, Then
from fastapi.testclient import TestClient
from api import app
from postgres import Postgres
from discoweb_client import DiscosWebClient


client = TestClient(app)

def test_download_data(postgres:Postgres, discos_web:DiscosWebClient):
    Given('interval and test tables')
    begin='2025-01-01'
    end='2025-01-31'
    suffix='_test'
    tables=['launches', 'reentries']
    for table in tables:
        postgres.drop_table(f'{table}{suffix}')
        postgres.create_table_as(f'{table}{suffix}', table)

    When('download')
    response = client.get(f"/download_data/?begin={begin}&end={end}&suffix={suffix}")

    Then('is expected')
    assert response.status_code == 200
    assert response.json()['launches'] > 0
    assert response.json()['reentries'] > 0

    for table in tables:
        postgres.drop_table(f'{table}{suffix}')

