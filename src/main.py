import extract
import load 

STOCK_TICKERS = {"AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.A", "JPM", "JNJ"}



if __name__ == "__main__":
    trade_date = extract.get_date("2026-04-02")
    
    response_data = extract.get_data_json(trade_date)

    extract.save_to_json(response_data,"raw_stocks","data/raw",trade_date)

    records = extract.filter_stock_data(response_data,STOCK_TICKERS)

    extract.save_to_json(records,"stocks","data/processed",trade_date)


    load.load_stock_data(records)


    