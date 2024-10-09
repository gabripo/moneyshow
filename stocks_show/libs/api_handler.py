import requests
from stocks_show.libs.dummy_data import get_default_stock_data
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY


def get_stock_from_api(tickerInput, apiName="alphavantage") -> dict:
    stockData = {}
    if apiName == "alphavantage":
        stockData["prices"] = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={tickerInput}&apikey={ALPHA_ADVANTAGE_API_KEY}&outputsize=full"
        ).json()
        stockData["sma"] = requests.get(
            f"https://www.alphavantage.co/query?function=SMA&symbol={tickerInput}&interval=daily&time_period=10&series_type=close&apikey={ALPHA_ADVANTAGE_API_KEY}"
        ).json()
    else:
        # TODO add more APIs
        stockData = get_default_stock_data(tickerInput)
    return stockData


def is_valid_api_data(stockData, groups=["prices", "sma"]) -> bool:
    """
    function to check whether fetched API data is ok to be used
    """
    validApi = False
    for group in groups:
        if group == "prices":
            validApi |= "Time Series (Daily)" in stockData[group]
        elif group == "sma":
            validApi |= "Technical Analysis: SMA" in stockData[group]
    return validApi
