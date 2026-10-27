import os
from datetime import date, datetime, timedelta

import certifi
import finnhub
import requests
import websocket

requests.post("https://ntfy.sh/stock_alerts", data="Started notification workflow on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# requests.post("https://ntfy.sh/stock_alerts", data="TEST: " + os.environ.get("TEST_SECRET"))

# ALPACA - HISTORICAL BARS (GMT)
# query_date = (datetime.now() - timedelta(days=1)).date().strftime("%Y-%m-%d")
# query_date = datetime.now().date().strftime("%Y-%m-%d")

# url = "https://data.alpaca.markets/v2/stocks/bars?symbols=AAPL&timeframe=30min&start=" + query_date + "T12%3A00%3A00Z&end=" + query_date + "T12%3A30%3A00Z&limit=1000&adjustment=raw&feed=sip&sort=asc"
# headers = {
#     "accept": "application/json",
#     "APCA-API-KEY-ID": os.environ.get("ALPACA_API_KEY"),
#     "APCA-API-SECRET-KEY": os.environ.get("ALPACA_SECRET_KEY")
# }
# response = requests.get(url, headers=headers)

# try: 
#     stock_data = response.json().get("bars").get("AAPL")[0] # Get the first bar data for AAPL
#     print(stock_data.get("c"), "on", stock_data.get("t"))
# except:
#     print("No stock data available for AAPL on", query_date, "at given time")

# FINNHUB - QUOTE
# finnhub_client = finnhub.Client(api_key="...")
# print(finnhub_client.quote("MU")["dp"])
# if finnhub_client.quote("MU")["dp"] > 4.99:
#     requests.post("https://ntfy.sh/stock_alerts", data="MU up over 4.99%: " + str(finnhub_client.quote("MU")["dp"]))

# ALPHA VANTAGE
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MU&apikey=...'
# r = requests.get(url)
# data = r.json()
# yesterday = date.today() - timedelta(days=1)
# print(data.get("Time Series (Daily)").get(str(yesterday)).get("4. close"))