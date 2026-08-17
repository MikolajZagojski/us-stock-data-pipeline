import requests 
import os
import json
from dotenv import load_dotenv
from datetime import date,datetime

# Massive API configuration
BASE_URL = "https://api.massive.com/"
ENDPOINT ="v2/aggs/grouped/locale/us/market/stocks/"



def get_date(date_str: str) -> date:
    """Parse a YYYY-MM-DD string and reject future dates."""
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    if parsed_date > datetime.today().date():
        raise ValueError("Choose date from past or today")
    return parsed_date

#API key is loaded form .env
def get_api_key() -> str:
    load_dotenv()
    if not os.getenv("API_KEY"):
        raise ValueError("API_KEY not found in environment variables. Please set it in the .env file.")
    return os.getenv("API_KEY")


def get_data_json(trade_date: date) -> dict:
    """Fetch the US stock market daily summary for a given trading date."""
    try:
        response = requests.get(BASE_URL+ENDPOINT+f"{trade_date}",
                                headers={"Authorization": f"Bearer {get_api_key()}"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

def save_to_json(data ,prefix: str, file_path: str, trade_date: date):
    """Persist raw or processed pipeline data as formatted JSON."""
    with open(f"{file_path}/{prefix}_{trade_date}.json","w") as f:
        json.dump(data,f,indent=4)


def filter_stock_data(response_data: dict,tickers: set) -> list:
    """Filter selected tickers and map Massive fields to internal schema."""
    records = []
    for stock in response_data["results"]:
        if stock["T"] in tickers:
            record = {
                "ticker": stock["T"],
                "open_price": stock["o"],
                "high_price": stock["h"],
                "low_price": stock["l"],
                "close_price": stock["c"],
                "volume": stock["v"],
                "trade_day": (datetime.fromtimestamp(stock["t"]/1000).date()).isoformat() #Massive returns timestamps in milliseconds
                }

            records.append(record)
    return records

