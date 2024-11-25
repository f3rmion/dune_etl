"""Dune ETL client and base query."""

import dotenv
import os

from dune_client.client import DuneClient
from dune_client.query import QueryBase


def create_dune_client(env_path: str = os.getcwd()) -> DuneClient:
    """Create Dune client from .env file.
    
    Args:
    env_path: .env file path (str)
    
    Returns:
    Dune client instance.
    """
    # load credentials
    dotenv.load_dotenv(env_path)
    return DuneClient.from_env()


def create_dune_query(name: str, query_id: int) -> QueryBase:
    """Create Dune query.
    
    Args:
    name: name of query (str)
    query_id: Dune identifier of query (int)
    
    Returns:
    Dune query base instance.
    """
    return QueryBase(
        name=name,
        query_id=query_id,
    )