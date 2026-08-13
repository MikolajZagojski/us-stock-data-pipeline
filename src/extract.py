import requests 
import os
import json
from dotenv import load_dotenv
from datetime import date,datetime
from pprint import pprint

BASE_URL = "https://api.massive.com/"
ENDPOINT ="v2/aggs/grouped/locale/us/market/stocks/"

stock_tickers = {"AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.A", "JPM", "JNJ"}

def get_date(date_str: str) -> date:
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if parsed_date > datetime.today().date():
        raise ValueError("Choose date from past or today")

    return parsed_date

def get_api_key() -> str:
    load_dotenv()
    if not os.getenv("API_KEY"):
        raise ValueError("Brak klucza API w zmiennych środowiskowych")
    return os.getenv("API_KEY")

def get_data_json(url : str,date: date) -> dict:
    try:
        response = requests.get(url+ENDPOINT+f"{date}",
                                headers={"Authorization": f"Bearer {get_api_key()}"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Błąd typu {e}")


date = get_date("2026-04-01")
response_data =get_data_json(BASE_URL,date)

def filter_stock_data(response_data: dict,tickers: set) -> list:
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
                "trade_day": (datetime.fromtimestamp(stock["t"]/1000).date()).isoformat()
                }

            records.append(record)
    return records

def save_to_json(records, file_path,date):
    with open(f"{file_path}/sample_{date}.json","w") as f:
        json.dump(records,f,indent=4)

records = filter_stock_data(response_data,stock_tickers)

save_to_json(records,"data/processed",date)