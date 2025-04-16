import pytest
from discoweb_client import DiscosWebClient
from typing import Generator
from postgres import Postgres

from dotenv import dotenv_values

config = dotenv_values(".env")

@pytest.fixture()
def discos_web() -> Generator[DiscosWebClient, None, None]:
    yield DiscosWebClient(config['DISCOWEB_TOKEN'])

@pytest.fixture()
def postgres() -> Generator[Postgres, None, None]:
    host = "localhost"
    port = "5432"
    user = "postgres"
    password = "postgres"
    database = "postgres"
    url = f"postgres://{host}:{port}/{database}?user={user}&password={password}"
    yield Postgres(url)