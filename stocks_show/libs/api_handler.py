import requests
from stocks_show.libs.dummy_data import get_default_stock_data
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY


def get_stock_from_api(tickerInput, apiName="alphavantage") -> dict:
    stockData = {}
    if apiName == "alphavantage":
        stockData["ticker"] = tickerInput

        stockDataDaily = api_alphavantage_call(
            tickerInput, ALPHA_ADVANTAGE_API_KEY, "TIME_SERIES_DAILY"
        )
        if "Time Series (Daily)" in stockDataDaily:
            stockData["prices"] = stockDataDaily["Time Series (Daily)"]

        stockDataSMA = api_alphavantage_call(
            tickerInput, ALPHA_ADVANTAGE_API_KEY, "SMA"
        )
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


def api_alphavantage_call(tickerInput, apiKey, dataType="TIME_SERIES_DAILY"):
    query = f"https://www.alphavantage.co/query?function={dataType}&symbol={tickerInput}&apikey={apiKey}"
    return requests.get(query).json()
