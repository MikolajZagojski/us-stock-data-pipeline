# US Stock Data Pipeline

A batch ETL pipeline that collects daily US stock market data from the Massive API, transforms selected stock records, stores raw and processed data as JSON files, and loads the results into PostgreSQL

## Project overview

The goal of this project is to build a simple end-to-emd data engineering pipeline for US stock market data.

The pipeline currently:

1. Fetch daily market data from the Massive API.
2. Stores the orginal API reponse in the raw data layer.
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
│   ├── extract.py
│   ├── load.py
│   └── main.py
├── compose.yaml
├── .gitignore
└── README.md
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

Create a `.env` file in the project root:

```env
API_KEY=your_massive_api_key
DB_PASS=your_postgres_password
```

The `.env` file is excluded from Git and should not be committed.

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

Activate the Python virtual environment and run:

```bash
python src/main.py
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
- Batch inserts
- Duplicate protection


## Purpose

This project was created as a hands-on Data Engineering portfolio project focused on learning and demonstrating ETL pipeline design, data storage, PostgreSQL, Docker, and Python.