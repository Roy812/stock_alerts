import requests
import websocket
import certifi
from datetime import date, datetime, timedelta
from fetcher import fetcher

# requests.post("https://ntfy.sh/stock_alerts", data="Test message")

# fetcher.add_stock("MU", "Micron Technology", 999.00)
# fetcher.get_stock("MU")

# ALPHA VANTAGE

# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MU&apikey=...'
# r = requests.get(url)
# data = r.json()
# yesterday = date.today() - timedelta(days=1)
# print(data.get("Time Series (Daily)").get(str(yesterday)).get("4. close"))

# FINNHUB

# def on_message(ws, message):
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(ws, status_code, message):
#     print("### closed ###")
#     print("Status:", status_code)
#     print("Message:", message)

# def on_open(ws):
#     ws.send('{"type":"subscribe","symbol":"MU"}')
#     ws.send('{"type":"subscribe","symbol":"SNDK"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=...",
#                               on_message = on_message,
#                               on_error = on_error,
#                               on_close = on_close)
#     ws.on_open = on_open
#     ws.run_forever(
#         sslopt={"ca_certs": certifi.where()}
#     )
