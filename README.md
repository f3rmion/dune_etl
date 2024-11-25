# Dune ETL for outgoing TVP data of Safe accounts

## Introduction

This extract, transform, and load (ETL) project is intended to handle outgoing total value processed (TVP) of Safe accounts.
We extract onchain outgoing TVP data on Ethereum mainnet.
The raw data is transformed and summarized using middleware code to provide us wthi the following metrics for pre-defined verticals and protocols:

- Unique Safes
- The total number of transactions aggregated per Safe per week
- Outgoing TVP in USD aggregated per Safe per week

Data is stored in a compressed [`parquet`](https://parquet.apache.org/docs/overview/motivation/) format to allow efficient storage and querying.
Abstracted classes (ABCs) are used to define the intended behaviour for ETL functions preferring behaviour over explicit implementation details.
Classes that implement those ABCs are used via dependency injections in the ETL functions to simplify modifications in the future.


## Setup project via `uv`

We use [`uv`](https://docs.astral.sh/uv/getting-started/) as our Python package manager and dependency resolver.

## Environment variables

The following environment variables are stored within an `.env` file in the root directory of this project:

- `DUNE_API_KEY`: Your Dune API key
- `DUNE_API_REQUEST_TIMEOUT`: Timeout parameter (`default = 120`)
- `QUERY_ID`: Dune query id
- `QUERY_NAME`: Dune query name
- `EXTRACT_NAME`: Name of the extraction file (`default = extract.parquet.gzip`)
- `TRANSFORM_VERTICAL_NAME`: Name of the vertical summary file (`default = summary_vertical.parquet.gzip`)
- `TRANSFORM_PROTOCOL_NAME`: Name of the protocol summary file (`default = summary_protocol.parquet.gzip`)

