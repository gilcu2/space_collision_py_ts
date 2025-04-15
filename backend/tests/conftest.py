import pytest
from discoweb_client import DiscosWebClient
from typing import Generator

from dotenv import dotenv_values

config = dotenv_values(".env")

@pytest.fixture()
def discos_web() -> Generator[DiscosWebClient, None, None]:
    yield DiscosWebClient(config['DISCOWEB_TOKEN'])