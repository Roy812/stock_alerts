import requests
import websocket
import certifi

requests.post("https://ntfy.sh/stock_alerts", data="Test message")

# ALPHA VANTAGE

# APIkey = ""
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MU&apikey=...'
# r = requests.get(url)
# data = r.json()

# print(data)

# FINNHUB
# apiKey = ""

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
