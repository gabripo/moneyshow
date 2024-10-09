import requests
from stocks_show.libs.dummy_data import get_default_stock_data
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY


def get_stock_from_api(tickerInput, apiName="alphavantage") -> dict:
    stockData = {}
    if apiName == "alphavantage":
        stockData["ticker"] = tickerInput

        stockDataDaily = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={tickerInput}&apikey={ALPHA_ADVANTAGE_API_KEY}&outputsize=full"
        ).json()
        if "Time Series (Daily)" in stockDataDaily:
            stockData["prices"] = stockDataDaily["Time Series (Daily)"]

        stockDataSMA = requests.get(
            f"https://www.alphavantage.co/query?function=SMA&symbol={tickerInput}&interval=daily&time_period=10&series_type=close&apikey={ALPHA_ADVANTAGE_API_KEY}"
        ).json()
        if "Technical Analysis: SMA" in stockDataSMA:
            stockData["sma"] = stockDataSMA["Technical Analysis: SMA"]
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
        validApi |= (group in stockData) and (len(stockData[group]) != 0)
    return validApi
