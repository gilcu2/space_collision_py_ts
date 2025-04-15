from bdd_helper import Given, When, Then, And
from postgres import Postgres
from datetime import datetime

def test_command_and_query(postgres:Postgres):
    Given("table, data, and queries")
    src_table='payloads'
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