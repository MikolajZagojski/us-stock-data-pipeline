from datetime import date, timedelta

from stock_pipeline import extract, load

STOCK_TICKERS = {"AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.A", "JPM", "JNJ"}

START_DATE = date(2026, 8, 4)


END_DATE = date(2026, 8, 7)


RECONCILIATION_START = START_DATE
RECONCILIATION_END = END_DATE


def process_day(trade_date: date):
    """Fetch, transform, persist and load stock data for one trading day."""

    print(f"Fetching data for {trade_date}")

    response_data = extract.get_data_json(trade_date)

    extract.save_to_json(response_data, "raw_stocks", "data/raw", trade_date)

    records = extract.filter_stock_data(response_data, STOCK_TICKERS)

    extract.save_to_json(records, "stocks", "data/processed", trade_date)

    load.load_stock_data(records)


def run_incremental_load():
    """Load new dates that come after the latest date stored in PostgreSQL."""

    last_trade_date = load.get_last_trade_date()

    if last_trade_date is None:
        start_date = START_DATE
    else:
        start_date = last_trade_date + timedelta(days=1)

    dates_to_fetch = load.get_dates_to_fetch(start_date, END_DATE)

    for trade_date in dates_to_fetch:
        process_day(trade_date)


def run_reconciliation():
    """Detect missing ticker-date pairs and backfill affected dates."""

    reconciliation_dates = load.get_dates_to_fetch(RECONCILIATION_START, RECONCILIATION_END)

    expected_keys = {
        (ticker, trade_date) for trade_date in reconciliation_dates for ticker in STOCK_TICKERS
    }

    existing_keys = load.get_existing_stock_keys(RECONCILIATION_START, RECONCILIATION_END)

    missing_keys = expected_keys - existing_keys

    if not missing_keys:
        print("No missing stock records found.")
        return

    print("Missing stock records:")

    for key in sorted(missing_keys):
        print(key)

    missing_dates = sorted({trade_date for ticker, trade_date in missing_keys})

    for trade_date in missing_dates:
        process_day(trade_date)


if __name__ == "__main__":
    run_incremental_load()
    run_reconciliation()
