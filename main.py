"""Dune ETL main function."""

from dune_etl.client import analyse
from dune_etl.etl import extract
from dune_etl.etl import transform
from dune_etl.config import create_dune_etl_config
from dune_etl.engines.pandas.extractor import create_pandas_extractor
from dune_etl.engines.pandas.transformer import create_pandas_transformer
from dune_etl.engines.pandas.analyser import create_pandas_analyser


# get Dune ETL config
CONFIG = create_dune_etl_config()


def main():
    # create Pandas extractor
    pandas_extractor = create_pandas_extractor(CONFIG)

    # store records in staging area
    extract(pandas_extractor)

    # create Pandas transformer
    pandas_transformer = create_pandas_transformer(CONFIG)

    # summarize by vertical and protocol by week
    transform(pandas_transformer)

    # create Pandas analyser
    pandas_analyser = create_pandas_analyser(CONFIG)

    # create top k analysis for verticals and protocols
    analyse(pandas_analyser)


if __name__ == "__main__":
    main()
