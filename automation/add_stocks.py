import os
from datetime import date, datetime
from typing import TypedDict

from supabase import create_client, Client
import finnhub
import requests

from repository import stock_repository

requests.post("https://ntfy.sh/stock_alerts", data="Started add stocks wf on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
try:
    # TICKER
    # test = "MU,NVDA"
    # tickers = test.split(",")
    tickers = os.environ.get("ADD_STOCKS_SECRET").split(",")
    print("Tickers:", tickers)

    for ticker in tickers:
        print("Processing ticker:", ticker)
        finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API"))

        # COMPANY NAME
        data = finnhub_client.symbol_lookup(ticker).get("result")
        for result in data:
            if result.get("displaySymbol") == ticker:
                company_name = result.get("description")

        # CATEGORY
        # test_categories = "MEMORY,CPU"
        # categories = test_categories.split(",")
        categories = os.environ.get("CATEGORY_SECRET").split(",")
        category = categories[tickers.index(ticker)]
        print("Category:", category)

        # PRICE
        quote_data = finnhub_client.quote(ticker)
        price = float(quote_data.get("c"))

        # ADD STOCK
        print("New Stock:", ticker, company_name, category, price)
        stock_repository.add_stocks([{
            "ticker": ticker,
            "company_name": company_name,
            "price": price,
            "category": category
        }])

    requests.post("https://ntfy.sh/stock_alerts", data="Stocks added successfully: " + tickers)
except Exception as error:
    requests.post("https://ntfy.sh/stock_alerts", data="Failed to add stocks: " + str(error))
    raise RuntimeError("Failed to add stock") from error
