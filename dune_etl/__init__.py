"""Dune ETL entry point."""

import os
from pathlib import Path

from dotenv import load_dotenv


class DuneETLConfig:
    """Dune ETL configuration."""

    def __init__(
            self,
            dotenv_path,
            extraction_path,
            transformation_path,
    ):
        self.dotenv_path = dotenv_path
        self.extraction_path = extraction_path
        self.transformation_path = transformation_path


def create_dune_etl_config():
    """Create Dune ETL configuration.
    
    Returns:
    Dune ETL configuration.
    """
    # define .env path
    root_path = os.path.join(os.path.dirname(__file__), "..")
    dotenv_path = os.path.join(root_path, ".env")

    # load variables into environment
    load_dotenv(dotenv_path)

    # check for extract and transform directories
    extraction_path = os.path.join(root_path, "extracted")
    transformation_path = os.path.join(root_path, "transformed")

    # create paths if necessary
    Path(extraction_path).mkdir(exist_ok=True)
    Path(transformation_path).mkdir(exist_ok=True)


    return DuneETLConfig(
        dotenv_path=dotenv_path,
        extraction_path=extraction_path,
        transformation_path=transformation_path
    )



