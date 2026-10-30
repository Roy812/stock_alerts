import os
from datetime import date, datetime
from repository import stock_repository

from supabase import create_client, Client
import requests

requests.post("https://ntfy.sh/stock_alerts", data="Started stock price history wf on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# try:
#     data = stock_repository.get_all_stocks()
#     for stock in data:
#         # ALPHA VANTAGE
#         ticker = stock["ticker"]
#         url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=' + os.environ.get("ALPHA_VANTAGE_API")
#         try:
#             r = requests.get(url, timeout=15)
#             r.raise_for_status()
#             data = r.json()
#         except requests.RequestException as error:
#             print(f"Alpha Vantage request failed: {error}")
#         else:
#             daily_data = data.get("Time Series (Daily)") or {}
#             # yesterday = date.today() - timedelta(days=1)
#             today = date.today()
#             today_data = daily_data.get(str(today)) or {}
#             # print(today_data)
#             closing_price = today_data.get("4. close")
#         if closing_price is None:
#             print("No closing price available for " + ticker + " on", today)
#         else:
#             # INSERT STOCK PRICE HISTORY
#             # stock_repository.add_stock_price_history(ticker, closing_price)
#             print(closing_price)
# except Exception as error:
#     raise RuntimeError("Failed to retrieve stocks from Supabase") from error

# # ALPHA VANTAGE
# ticker = "AAPL"
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=' + os.environ.get("ALPHA_VANTAGE_API")
# try:
#     r = requests.get(url, timeout=15)
#     r.raise_for_status()
#     data = r.json()
# except requests.RequestException as error:
#     print(f"Alpha Vantage request failed: {error}")
# else:
#     daily_data = data.get("Time Series (Daily)") or {}
#     # yesterday = date.today() - timedelta(days=1)
#     today = date.today()
#     today_data = daily_data.get(str(today)) or {}
#     closing_price = today_data.get("4. close")
#     if closing_price is None:
#         print("No closing price available for AAPL on", today)
#     else:
#         print(closing_price)