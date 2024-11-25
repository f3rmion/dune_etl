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
            query_id,
            query_name,
            transform_vertical_name,
            transform_protocol_name,
    ):
        self.dotenv_path = dotenv_path
        self.extraction_path = extraction_path
        self.transformation_path = transformation_path

        self.transform_vertical_name = transform_vertical_name
        self.transform_protocol_name = transform_protocol_name

        self.query_id = query_id
        self.query_name = query_name


def create_dune_etl_config():
    """Create Dune ETL configuration.
    
    Returns:
    Dune ETL configuration.
    """
    # define rot and .env path
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

    extraction_path = os.path.join(extraction_path, os.environ["EXTARCT_NAME"])
    transform_vertical_name = os.path.join(transformation_path, os.environ["TRANSFORM_VERTICAL_NAME"])
    transform_protocol_name = os.path.join(transformation_path, os.environ["TRANFORM_PROTOCOL_NAME"])

    # get query details
    query_id = os.environ["QUERY_ID"]
    query_name = os.environ["QUERY_NAME"]

    return DuneETLConfig(
        dotenv_path=dotenv_path,
        extraction_path=extraction_path,
        transformation_path=transformation_path,
        query_id=query_id,
        query_name=query_name,
        transform_vertical_name=transform_vertical_name,
        transform_protocol_name=transform_protocol_name
    )


