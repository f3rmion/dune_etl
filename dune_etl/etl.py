"""Dune ETL extract, transform, and analys steps."""

from dune_etl.engines.abc.blueprints import Analyser
from dune_etl.engines.abc.blueprints import Extractor
from dune_etl.engines.abc.blueprints import Transformer


def extract(extractor: Extractor):
    """Extraction function to store Dune query records.

    Args:
    extractor: Extractor ABC blueprint (Extractor)
    """
    # query Dune and cache results in DataFrame-like object
    extractor.query_records()

    # store cached records as parquet files
    extractor.store_records()


def transform(transformer: Transformer):
    """Tranformation function to summarize Dune query records.

    Args:
    transformer: Transfomer ABC blueprint (Transfomer)
    """
    # read Dune records from parquet file into DataFrame-like object
    transformer.read_records()

    # summarize records by vertical and protocol by week
    transformer.create_summary()


def analyse(analyser: Analyser):
    """Analyser function to create top k analysis.

    Args:
    analyser: Analyser ABC blueprint (Analyser)
    """
    analyser.create_analysis()
