import pytest
from discoweb_client import DiscoWebClient
from typing import Generator

from dotenv import dotenv_values

config = dotenv_values(".env")

@pytest.fixture()
def discoweb() -> Generator[DiscoWebClient, None, None]:
    yield DiscoWebClient(config['DISCOWEB_TOKEN'])