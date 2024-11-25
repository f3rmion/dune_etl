import os

from dune_client.client import DuneClient
from dune_client.query import QueryBase

from dune_etl.client import create_dune_client
from dune_etl.client import create_dune_query


def test_can_create_dune_client():
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    client = create_dune_client(dotenv_path)
    assert isinstance(client, DuneClient)


def test_can_create_dune_query():
    wanted_id = 123456
    wanted_name = "test"

    query = create_dune_query(name=wanted_name, query_id=wanted_id)
    assert isinstance(query, QueryBase)

    assert query.name == wanted_name
    assert query.query_id == wanted_id
