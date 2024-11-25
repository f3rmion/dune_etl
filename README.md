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

```bash
DUNE_API_KEY=<your API key>
DUNE_API_REQUEST_TIMEOUT=120

QUERY_ID=<Dune query ID>
QUERY_NAME=<Dune query name>

EXTARCT_NAME="extract.parquet.gzip"
TRANSFORM_VERTICAL_NAME="summary_vertical.parquet.gzip"
TRANFORM_PROTOCOL_NAME="summary_protocol.parquet.gzip"

TOP5_VERTICAL_TVP="top5_vertical_total_tvp.csv"
TOP5_VERTICAL_TRANSACTIONS="top5_vertical_transactions.csv"
TOP5_PROTOCOL_TVP="top5_protocol_total_tvp.csv"
TOP5_PROTOCOL_TRANSACTIONS="top5_protocol_transactions.csv"
```

## Run Dune ETL

To run the full ETL we use the following command

```bash
> uv run main.py
```
