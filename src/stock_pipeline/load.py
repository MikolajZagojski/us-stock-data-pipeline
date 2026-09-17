from datetime import date, timedelta

import psycopg

from stock_pipeline.config import get_settings


def _connect() -> psycopg.Connection:
    s = get_settings()
    return psycopg.connect(
        host=s.db_host,
        port=s.db_port,
        dbname=s.db_name,
        user=s.db_user,
        password=s.db_pass,
    )


def load_stock_data(records: list):
    """Load stock records into PostgreSQL and ignore duplicate ticker-date pairs."""
    with _connect() as conn:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO stock_info (
                    ticker, open_price, high_price, low_price,
                    close_price, volume, trade_day
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, trade_day) DO NOTHING;
            """
            for record in records:
                input_values = [
                    record["ticker"],
                    record["open_price"],
                    record["high_price"],
                    record["low_price"],
                    record["close_price"],
                    record["volume"],
                    record["trade_day"],
                ]
                cur.execute(insert_query, input_values)


def get_last_trade_date() -> date | None:
    """Retrieve the most recent trade date from the stock_info table."""
    with _connect() as conn:
        with conn.cursor() as cur:
            query = "SELECT MAX(trade_day) FROM stock_info;"
            cur.execute(query)
            latest_date = cur.fetchone()
            if latest_date[0] is None:
                return None
            return latest_date[0]


def get_dates_to_fetch(start_date: date, end_date: date) -> list[date]:
    """Generate a list of dates from start_date to end_date inclusive."""
    current_date = start_date
    date_list = []

    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list


def get_existing_stock_keys(start_date: date, end_date: date) -> set[tuple[str, date]]:
    """Return existing (ticker, trade_day) keys for the given date range."""
    with _connect() as conn:
        with conn.cursor() as cur:
            query = """
                SELECT ticker, trade_day
                FROM stock_info
                WHERE trade_day BETWEEN %(start_date)s 
                AND %(end_date)s;"""
            cur.execute(query, {"start_date": start_date, "end_date": end_date})
            rows = cur.fetchall()
            return set(rows)
