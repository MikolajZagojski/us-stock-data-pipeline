import os 
import psycopg
from dotenv import load_dotenv


def get_pass() -> str:
    load_dotenv()
    if not os.getenv("DB_PASS"):
        raise ValueError("DB_PASS not found in enviroment variables. Please set it in the .env file.")
    return os.getenv("DB_PASS")


HOST = "localhost"
PORT = 5433
DB = "stock_market"
USER = "stock_user"
PASS = get_pass()


def load_stock_data(records: list):
    """Load stock records into PostgreSQL and ignore duplicate ticker-date pairs."""
    with psycopg.connect(host=HOST,port=PORT,dbname=DB,user=USER,password=PASS) as conn:
        with conn.cursor() as cur:
            insert_query = "INSERT INTO stock_info (ticker, open_price, high_price, low_price, close_price, volume, trade_day) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ticker, trade_day) DO NOTHING;"
            for record in records:
                input_values = [record["ticker"], record["open_price"], record["high_price"], record["low_price"], record["close_price"], record["volume"], record["trade_day"]]
                cur.execute(insert_query, input_values)




