from bdd_helper import Given, When, Then, And
from fastapi.testclient import TestClient
from api import app
from postgres import Postgres
import requests



def test_get_space_objects_variation(postgres: Postgres):
    Given('interval and test tables with data')
    begin = '2025-01-01'
    end = '2025-01-31'

    When('get variation')
    response = requests.get(f"http://localhost:8000/get_space_objects_variation/?begin={begin}&end={end}")

    Then('is expected')
    assert response.status_code == 200
    result=response.json()
    assert len(result['days']) == 31
    assert len(result['variations']) == 31


