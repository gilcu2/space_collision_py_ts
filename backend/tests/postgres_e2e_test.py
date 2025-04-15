from bdd_helper import Given, When, Then, And
from postgres import Postgres
from datetime import datetime

def test_command_and_query(postgres:Postgres):
    Given("table and data")
    src_table='reentries'
    test_table=f'{src_table}_test'
    postgres.drop_table(test_table)
    postgres.create_table_as(test_table, src_table)

    data=[
        (1,{'test':1, 'test_date': '2025-01-01'}),
        (2, {'test': 2, 'test_date': '2025-01-02'}),
        (3, {'test': 3, 'test_date': '2025-01-03'}),
    ]



    When("insert")
    postgres.insert_data(test_table, data)

    And('query')
    query_sql = f"SELECT * FROM {test_table} WHERE (data->>'test_date')::date > '2025-01-01'"
    result=postgres.query(query_sql)

    Then("is expected")
    assert len(result) == 2


def test_get_number_by_day(postgres:Postgres):
    Given("table with data")
    src_table = 'reentries'
    test_table = f'{src_table}_test'
    date_field='test_date'
    postgres.drop_table(test_table)
    postgres.create_table_as(test_table, src_table)

    data = [
        (1, {'test': 1, date_field: '2025-01-01'}),
        (2, {'test': 2, date_field: '2025-01-01'}),
        (3, {'test': 3, date_field: '2025-01-03'}),
    ]

    And('the expected result')
    expected=[
        (datetime.strptime('2025-01-01', "%Y-%m-%d").date(), 2),
        (datetime.strptime('2025-01-03', "%Y-%m-%d").date(), 1),
    ]

    When("insert")
    postgres.insert_data(test_table, data)

    And('query')
    result = postgres.get_number_by_day(test_table, date_field)

    Then("is expected")
    assert result == expected
