"""Dune ETL Pandas extractor."""

import pandas as pd

from dune_etl.config import DuneETLConfig
from dune_etl.engines.abc.blueprints import Extractor
from dune_etl.client import create_dune_client
from dune_etl.client import create_dune_query


class PandasExtractor(Extractor):
    """Pandas extractor."""

    def __init__(self, dune_client, dune_query, extraction_path):
        self.records_df = pd.DataFrame()

        self.dune_client = dune_client
        self.dune_query = dune_query

        self.extraction_path = extraction_path

    def query_records(self):
        """Query Dune records via Pandas engine."""
        # cache Dune records in Pandas DataFrame
        self.records_df = self.dune_client.run_query_dataframe(self.dune_query)

    def store_records(self, engine="pyarrow", compression="gzip"):
        """Store Dune records via Pandas engine."""
        # explicitly type cast numeric columns
        numeric_columns = ["amount", "amount_usd"]
        self.records_df[numeric_columns] = self.records_df[numeric_columns].apply(pd.to_numeric)

        # store records in compressed parquet file
        self.records_df.to_parquet(
            path=self.extraction_path, engine=engine, compression=compression,
        )


def create_pandas_extractor(config: DuneETLConfig) -> PandasExtractor:
    """Create Pandas extractor.
    
    Args:
    config: Dune ETL config (DuneETLConfig)
    
    Returns:
    Pandas extractor.
    """
    # create Dune client and load credentials from .env file
    client = create_dune_client(env_path=config.dotenv_path)

    # build Dune query
    query = create_dune_query(
        name=config.query_name,
        query_id=config.query_id,
    )

    # create Pandas extractor
    return PandasExtractor(
        dune_client=client,
        dune_query=query,
        extraction_path=config.extraction_path,
    )
