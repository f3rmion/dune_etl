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
