from discoweb_client import DiscoWebClient
from bdd_helper import Given,When, Then

def test_get_discos():
    Given('day and object type')
    day=