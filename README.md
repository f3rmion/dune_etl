# Dune ETL for Outgoing TVP Data of Safe Accounts

This ETL pipeline processes outgoing Total Value Processed (TVP) data for Safe accounts on Ethereum mainnet. Key outputs include:

- **Unique Safes**
- **Weekly Aggregations**:
  - Total transactions per Safe.
  - Outgoing TVP in USD per Safe.

Data is stored in compressed [`parquet`](https://parquet.apache.org/docs/overview/motivation/) format for efficiency. Abstract base classes (ABCs) define behaviors for modular ETL components.

---

## Setup Instructions

### Prerequisites

Install [`uv`](https://docs.astral.sh/uv/getting-started/) as the package manager (see [installation guide](https://docs.astral.sh/uv/getting-started/installation/)).

### Environment Variables

Add the following to a `.env` file in the project root:

```bash
DUNE_API_KEY=<your API key>
DUNE_API_REQUEST_TIMEOUT=120

QUERY_ID=4326389
QUERY_NAME="transfer_classification"

EXTRACT_NAME="extract.parquet.gzip"
TRANSFORM_VERTICAL_NAME="summary_vertical.parquet.gzip"
TRANSFORM_PROTOCOL_NAME="summary_protocol.parquet.gzip"

TOP5_VERTICAL_TVP="top5_vertical_total_tvp.csv"
TOP5_VERTICAL_TRANSACTIONS="top5_vertical_transactions.csv"
TOP5_PROTOCOL_TVP="top5_protocol_total_tvp.csv"
TOP5_PROTOCOL_TRANSACTIONS="top5_protocol_transactions.csv"
```

## Running the ETL

Run the pipeline with:

```bash
> uv run main.py
```

This executes the following steps:

1. **Extract**: Fetch raw data via the Dune API.
2. **Transform**: Create weekly summaries for verticals and protocols.
3. **Analyze**: Identify top-5 verticals and protocols by TVP and transaction count.

## Improvements of ETL Components

### Extract

**Current**:

- Fetches data with `run_query_dataframe` (Dune client) and stores locally in `$ROOT/extracted`.

**Improvement**:

- Use `ResultResponse.get_rows()` for pagination.
- Store data in cloud (e.g., AWS S3) instead of local storage.
- Implement better file naming (UUID + timestamp).

### Transform

**Current**:

- Pandas processes data and saves summaries in `$ROOT/transformed`.

**Improvement**:

- Use distributed computation frameworks like Dask that support lazy memory evaluation.

### Analyze

**Current**:

- Pandas performs top-k analysis; unclassified data and burn address are excluded. Results saved in `$ROOT/analysis`.

**Improvement**:

- Support distributed analysis for large datasets.
  Add automated visualization (e.g., Matplotlib, Plotly).

## Enhancements

1. **Efficiency**: Replace in-memory Pandas with distributed engines (e.g., Dask).
2. **Scalability**: Partition data and adopt cloud solutions.
3. **Extensibility**: Keep using dependency injection for modular ETL components with updated parts.
4. **Testing**: Improve (unit) test coverage for all ETL steps (dependency injection can be used for mocking).

These improvements will ensure the pipeline remains scalable, efficient, and future-proof.

## Dockerizing the ETL Application (description only)

To enhance portability and scalability, we should containerize the ETL pipeline using Docker. This will allow us to package the application and its dependencies into a single image that can be run on any system with Docker installed:

1. **Replace Local Storage**: Use a cloud staging area (e.g., AWS S3) for storing data instead of the local filesystem.
2. **Expose ETL Functions via an API**: Provide programmatic access to `extract`, `transform`, and `analyse` steps.
3. **Containerize the Application**: Package the ETL pipeline as a Docker container.
4. **Enable Cloud Deployment**: Use tools like ArgoCD to deploy the containerized application into a cloud environment. For this purpose, have a separate GitHub repository for the deployment configuration (environment values).

---

### Implementation Steps

#### 1. Replace Local Storage with a Cloud Staging Area

- **Current Implementation**: Data is stored in `$ROOT/extracted`, `$ROOT/transformed`, and `$ROOT/analysis` directories on the local filesystem.
- **Proposed Changes**:
  - Integrate with a cloud-based staging area such as **AWS S3**.
  - Use libraries like `boto3` to handle uploads and downloads of intermediate data.
  - Update environment variables for cloud configuration.

#### 2. Integrate an API for ETL Functions

- Use **FastAPI** to expose the ETL steps as RESTful endpoints:
  - `/extract`: Initiates the data extraction process.
  - `/transform`: Processes raw data into summaries.
  - `/analyse`: Performs top-k analysis and generates reports.
- Add a `Dockerfile` that containerized the `dune_etl` within a FastAPI application and create a CI/CD pipeline for automated testing and deployment of the created image.

## Rewriting the ETL in Apache Airflow (description only)

Apache Airflow can be used to orchestrate the ETL pipeline and AWS S3 as the staging area for intermediate data. The pipeline will consist of modular, atomic steps for `extract`, `transform`, and `analyse`, linked together as a **Directed Acyclic Graph (DAG)**.
Each task should take inputs from AWS S3 and store outputs to AWS S3, based on different prefixes that define the stage of the ETL.

Advantages of using Apache Airflow:

1. **Scalability**: Airflow can handle complex workflows with dependencies between tasks.
2. **Monitoring**: Built-in monitoring and alerting capabilities.
3. **Scheduling**: Define schedules for each task and manage dependencies between them.
4. **Extensibility**: Easily add new tasks or modify existing ones.
5. **Reusability**: Define reusable tasks and workflows.
