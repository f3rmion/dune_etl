from dune_etl.engines.abc.blueprints import Analyser
from dune_etl.engines.abc.blueprints import Extractor
from dune_etl.engines.abc.blueprints import Transformer
from dune_etl.config import create_dune_etl_config
from dune_etl.engines.pandas.extractor import create_pandas_extractor
from dune_etl.engines.pandas.transformer import create_pandas_transformer
from dune_etl.engines.pandas.analyser import create_pandas_analyser

# get Dune ETL config
CONFIG = create_dune_etl_config()


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