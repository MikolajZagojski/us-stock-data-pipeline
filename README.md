# US Stock Data Pipeline

A batch ETL pipeline that collects daily US stock market data from the Massive API, transforms selected stock records, stores raw and processed data as JSON files, and loads the results into PostgreSQL.

## Project overview

The goal of this project is to build a simple end-to-end data engineering pipeline for US stock market data.

The pipeline currently:

1. Fetches daily market data from the Massive API.
2. Stores the original API response in the raw data layer.
3. Filters selected stock tickers.
4. Transforms API fields into an internal schema.
5. Stores transformed records as processed JSON.
6. Loads the data into PostgreSQL.
7. Prevents duplicate records using a composite primary key.

## Architecture

```text
Massive API
    |
    v
Python Extract
    |
    v
data/raw/
    |
    v
Transform & Filter
    |
    v
data/processed/
    |
    v
PostgreSQL
```

## Tech Stack

- Python
- PostgreSQL
- Docker
- Docker Compose
- Psycopg
- uv
- REST API
- SQL
- Git

## Project Structure

```text
us-stock-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── sql/
│   └── create_table.sql
├── src/
│   └── stock_pipeline/
│       ├── __init__.py
│       ├── extract.py
│       ├── load.py
│       └── main.py
├── tests/
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── README.md
├── compose.yaml
├── pyproject.toml
└── uv.lock
```

## Data Schema

The processed stock records contain:

```text
ticker
open_price
high_price
low_price
close_price
volume
trade_day
```

The PostgreSQL table uses a composite primary key:

```text
(ticker, trade_day)
```

This prevents duplicate records for the same stock and trading day.

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
API_KEY=your_massive_api_key
DB_USER=stock_user
DB_PASS=your_postgres_password
DB_NAME=stock_market
DB_HOST=localhost
DB_PORT=5433
```

The `.env` file is excluded from Git and should not be committed.

## Setup

Install dependencies:

```bash
uv sync
```

## Running PostgreSQL

Start PostgreSQL using Docker Compose:

```bash
docker compose up -d
```

Check the running container:

```bash
docker ps
```

## Running the Pipeline

```bash
uv run python -m stock_pipeline.main
```

The pipeline will:

```text
fetch API data
→ save raw JSON
→ transform selected stocks
→ save processed JSON
→ load records into PostgreSQL
```

## Database

The PostgreSQL schema can be created using:

```text
sql/create_table.sql
```

The pipeline handles duplicate ticker/date combinations using PostgreSQL `ON CONFLICT`.

## Current Status

Implemented:

- Massive API integration
- API key management using environment variables
- Date validation
- Raw JSON storage
- Stock ticker filtering
- Data transformation
- Processed JSON storage
- PostgreSQL running in Docker
- Python-to-PostgreSQL connection
- Incremental loading
- Reconciliation of missing records
- Duplicate protection
