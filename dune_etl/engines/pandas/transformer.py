"""Dune ETL Pandas transformer."""

import pandas as pd

from dune_etl.config import DuneETLConfig
from dune_etl.engines.abc.blueprints import Transformer


class PandasTransformer(Transformer):
    """Pandas transformer."""

    def __init__(self, extract_name, transform_vertical_name, transform_protocol_name):
        self.extract_name = extract_name
        self.transform_vertical_name = transform_vertical_name
        self.transform_protocol_name = transform_protocol_name

        self.results_df = pd.DataFrame()
        self.vertical_df = pd.DataFrame()
        self.protocol_df = pd.DataFrame()

    def read_records(self, engine="pyarrow"):
        """Read extracted records in parquet formar via Pandas/Pyarrow."""
        self.results_df = pd.read_parquet(self.extract_name, engine=engine)

    def create_summary(self, engine="pyarrow", compression="gzip"):
        """Summarize Dune data.

        We want weekly summary at the vertical and protocol level.
        The following metrics are needed:
        - unique safes
        - total transactions
        - outgoing tvo in usd
        """
        # convert block_date to datetime
        self.results_df["block_date"] = pd.to_datetime(self.results_df["block_date"])

        # extract the week (ISO week)
        self.results_df["week"] = (
            self.results_df["block_date"].dt.to_period("W").astype(str)
        )

        # summarize vertical by week
        self.vertical_df = (
            self.results_df.groupby(["week", "vertical"])
            .agg(
                unique_safes=("safe_sender", "nunique"),
                total_transactions=("tx_hash", "count"),
                outgoing_tvp_usd=("amount_usd", "sum"),
            )
            .reset_index()
        )

        # store vertical summary
        self.vertical_df.to_parquet(
            path=self.transform_vertical_name,
            engine=engine,
            compression=compression,
        )

        # summarize protocol by week
        self.protocol_df = (
            self.results_df.groupby(["week", "protocol"])
            .agg(
                unique_safes=("safe_sender", "nunique"),
                total_transactions=("tx_hash", "count"),
                outgoing_tvp_usd=("amount_usd", "sum"),
            )
            .reset_index()
        )

        # store protocol summary
        self.protocol_df.to_parquet(
            path=self.transform_protocol_name,
            engine=engine,
            compression=compression,
        )


def create_pandas_transformer(config: DuneETLConfig) -> PandasTransformer:
    """Create Pandas trasnformer.

    Args:
    config: Dune ETL config (DuneETLConfig)

    Returns:
    Pandas transformer.
    """
    # create Pandas transformer
    return PandasTransformer(
        extract_name=config.extraction_path,
        transform_vertical_name=config.transform_vertical_name,
        transform_protocol_name=config.transform_protocol_name,
    )
