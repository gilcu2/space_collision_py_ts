from discoweb_client import DiscosWebClient
from bdd_helper import Given,When, Then
from datetime import datetime

def test_get_payloads_by_reentry(discos_web: DiscosWebClient):
    Given('interval')
    begin=datetime.strptime('2025-01-01','%Y-%m-%d').date()
    end=datetime.strptime('2025-01-31','%Y-%m-%d').date()
    page_size=10


    When('download')
    payloads=discos_web.get_payloads_by_reentry(begin, end, page_size=page_size)

    Then('is expected')
    assert len(payloads.data) == page_size

def test_get_launches_without_data(discos_web: DiscosWebClient):
    Given('interval')
    begin=datetime.strptime('2025-01-01','%Y-%m-%d').date()
    end=datetime.strptime('2025-01-02','%Y-%m-%d').date()
    page_size=100


    When('download')
    launches=discos_web.get_launches(begin, end, page_size=page_size)

    Then('is expected')
    assert len(launches.data) == 0

def test_get_launches_with_pagination(discos_web: DiscosWebClient):
    Given('interval')
    begin=datetime.strptime('2025-01-01','%Y-%m-%d').date()
    end=datetime.strptime('2025-01-31','%Y-%m-%d').date()
    page_size=10


    When('download')
    launches=discos_web.get_launches(begin, end, page_size=page_size)

    Then('is expected')
    assert len(launches.data) == page_size

def test_get_reentries(discos_web: DiscosWebClient):
    Given('interval')
    begin=datetime.strptime('2025-01-01','%Y-%m-%d').date()
    end=datetime.strptime('2025-01-10','%Y-%m-%d').date()
    page_size=10


    When('download')
    reentries=discos_web.get_reentries(begin, end, page_size=page_size)

    Then('is expected')
    assert len(reentries.data) == page_size