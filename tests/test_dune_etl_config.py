from dune_etl import create_dune_etl_config
from dune_etl import DuneETLConfig

def test_can_create_config():
    config = create_dune_etl_config()
    assert isinstance(config, DuneETLConfig)