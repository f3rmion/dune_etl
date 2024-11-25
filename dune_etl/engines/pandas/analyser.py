"""Dune ETL Pandas transformer."""

import pandas as pd

from dune_etl.config import DuneETLConfig
from dune_etl.engines.abc.blueprints import Analyser


class PandasAnalyser(Analyser):
    """Pandas analyser."""

    def __init__(
            self,
            transform_vertical_name,
            transform_protocol_name,
            top5_vertical_tvp,
            top5_vertical_transaction,
            top5_protocol_tvp,
            top5_protocol_transaction,
    ):
        self.transform_vertical_name = transform_vertical_name
        self.transform_protocol_name = transform_protocol_name

        self.top5_vertical_tvp = top5_vertical_tvp
        self.top5_vertical_transaction = top5_vertical_transaction
        self.top5_protocol_tvp = top5_protocol_tvp
        self.top5_protocol_transaction = top5_protocol_transaction 

        self.vertical_df = pd.DataFrame()
        self.protocol_df = pd.DataFrame()

    def create_analysis(self, engine="pyarrow", compression="gzip"):
        """Find top 5 TVP verticals and protocols.
        
        We define top TVP by:
        - highest transaction volume
        - highest transaction count
        """
        # read vertical summary
        self.vertical_df = pd.read_parquet(self.transform_vertical_name, engine=engine)

        # filter out unclassified and burn address
        self.vertical_df = self.vertical_df[
            ~self.vertical_df["vertical"].str.contains("unclassified", case=False, na=False) &
            ~self.vertical_df["vertical"].str.contains("burn address", case=False, na=False)
        ]

        # read protocol summary
        self.protocol_df = pd.read_parquet(self.transform_protocol_name, engine=engine)


        # filter out unclassified and burn address
        self.protocol_df = self.protocol_df[
            ~self.protocol_df["protocol"].str.contains("unclassified", case=False, na=False) &
            ~self.protocol_df["protocol"].str.contains("burn address", case=False, na=False)
        ]

        # explicitly type cast numeric columns
        numeric_columns = ["outgoing_tvp_usd", "total_transactions"]
        self.vertical_df[numeric_columns] = self.vertical_df[numeric_columns].apply(pd.to_numeric)
        self.protocol_df[numeric_columns] = self.protocol_df[numeric_columns].apply(pd.to_numeric)

        # create vertical metrics
        grouped_verticals = (
            self.vertical_df.groupby("vertical")
            .agg(
                total_tvp=("outgoing_tvp_usd", "sum"),
                total_transactions=("total_transactions", "sum"),
            )
            .reset_index()
        )

        # create protocol metrics
        grouped_protocols = (
            self.protocol_df.groupby("protocol")
            .agg(
                total_tvp=("outgoing_tvp_usd", "sum"),
                total_transactions=("total_transactions", "sum"),      
            )
            .reset_index()
        )

        # get top 5 TVP verticals and protocols
        top5_vertical_by_tvp = grouped_verticals.nlargest(5, "total_tvp")
        top5_vertical_by_transactions = grouped_verticals.nlargest(5, "total_transactions")

        top5_protocol_by_tvp = grouped_protocols.nlargest(5, "total_tvp")
        top5_protocol_by_transactions = grouped_protocols.nlargest(5, "total_transactions")

        # store analysis results
        top5_vertical_by_tvp.to_csv(self.top5_vertical_tvp)
        top5_vertical_by_transactions.to_csv(self.top5_vertical_transaction)
        top5_protocol_by_tvp.to_csv(self.top5_protocol_tvp)
        top5_protocol_by_transactions.to_csv(self.top5_protocol_transaction)


def create_pandas_analyser(config: DuneETLConfig) -> PandasAnalyser:
    """Create Pandas analyser.
    
    Args:
    config: Dune ETL config (DuneETLConfig)
    
    Returns:
    Pandas analyser.
    """
    # create Pandas analyser
    return PandasAnalyser(
        transform_vertical_name=config.transform_vertical_name,
        transform_protocol_name=config.transform_protocol_name,
        top5_vertical_tvp=config.top5_vertical_tvp,
        top5_vertical_transaction=config.top5_vertical_transaction,
        top5_protocol_tvp=config.top5_protocol_tvp,
        top5_protocol_transaction=config.top5_protocol_transaction,
    )