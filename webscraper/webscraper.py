import requests

response = requests.get("https://www.ionq.com/news")
print(response.text)
