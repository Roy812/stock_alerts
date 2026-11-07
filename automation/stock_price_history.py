import os
from datetime import date, datetime, timedelta
from repository import stock_repository, stock_price_history_repository

import finnhub
import requests


def get_daily_volume(ticker: str, date: str):
    headers = {
        'Content-Type': 'application/json'
    }
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate=" + date + "&token=" + os.environ.get("TIINGO_API_KEY"), headers=headers)
    payload = requestResponse.json()
    volume = 0
    if len(payload) == 0:
        print("No data returned from Tiingo API for today.")
    else:
        volume = payload[0].get("volume")
    return volume


requests.post("https://ntfy.sh/stock_alerts", data="Started stock price history wf on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

try:
    stocks = stock_repository.get_all_stocks()
    finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API"))

    for stock in stocks:
        ticker = stock["ticker"]
        print(f"Fetching price history for {ticker}...")

        # FINNHUB API call to get the current stock price after close
        quote_data = finnhub_client.quote(ticker)
        close_price = float(quote_data.get("c"))

        # TIINGO API call to get the daily close price and volume for the stock
        volume = get_daily_volume(ticker, date.today().strftime("%Y-%m-%d"))

        stock_price_history_repository.add_stock_price_history(ticker, close_price, volume)
        print(f"Added price history for {ticker}: price: {close_price} volume: {volume}")

    requests.post("https://ntfy.sh/stock_alerts", data="Stock price history updated successfully")
except Exception as error:
    requests.post("https://ntfy.sh/stock_alerts", data="Failed to update stock price history")
    raise RuntimeError("Failed to update stock price history") from error
