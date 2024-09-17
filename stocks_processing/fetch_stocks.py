import requests
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY


def fetch_stock_data(symbol):
    api_key = ALPHA_ADVANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data
