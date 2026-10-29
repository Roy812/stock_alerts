import os
from datetime import date, datetime, time

import certifi
import finnhub
import requests
import websocket

if datetime.now().time() < time(15, 30):
    requests.post("https://ntfy.sh/stock_alerts", data="Started pre market ntfy workflow at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# requests.post("https://ntfy.sh/stock_alerts", data="TEST: " + os.environ.get("TEST_SECRET"))

# ALPACA - HISTORICAL BARS (GMT)
query_date = datetime.now().date().strftime("%Y-%m-%d")
# url = "https://data.alpaca.markets/v2/stocks/bars?symbols=MU&timeframe=30min&start=" + query_date + "T11%3A45%3A00Z&end=" + query_date + "T12%3A15%3A00Z&limit=1000&adjustment=raw&feed=sip&sort=asc"
url = "https://data.alpaca.markets/v2/stocks/bars?symbols=AAPL&timeframe=30min&limit=1000&adjustment=raw&feed=sip&sort=asc"
headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": os.environ.get("ALPACA_API_KEY"),
    "APCA-API-SECRET-KEY": os.environ.get("ALPACA_SECRET_KEY")
}

try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    payload = response.json()
    print(payload)
except requests.RequestException as error:
    print(f"Alpaca request failed: {error}")
else:
    bars = payload.get("bars") or {}
    stock_bars = bars.get("AAPL") or []

    if stock_bars:
        stock_data = stock_bars[stock_bars.__len__() - 1]
        print(stock_data.get("c"), "on", stock_data.get("t"))
        requests.post("https://ntfy.sh/stock_alerts", data= "AAPL: " + str(stock_data.get("c")) + " on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print("No stock data available for AAPL on", query_date, "at the requested time")

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