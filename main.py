from dune_etl.engines.abc.blueprints import Extractor
from dune_etl.config import create_dune_etl_config
from dune_etl.engines.pandas.extractor import create_pandas_extractor

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


def main():
    # create Pandas extractor
    pandas_extractor = create_pandas_extractor(CONFIG)
    
    # store records in staging area
    extract(pandas_extractor)

if __name__ == "__main__":
    main()