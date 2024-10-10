import requests
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
        stockData = []
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


def get_stock_timeseries_alphavantage(
    stockDataAlphavantage, parentCategory="Time Series (Daily)"
):
    data = {}
    if parentCategory == "Time Series (Daily)":
        data["open"] = get_stock_timeseries_element_alphavantage(
            stockDataAlphavantage, parentCategory, "1. open"
        )
        data["high"] = get_stock_timeseries_element_alphavantage(
            stockDataAlphavantage, parentCategory, "2. high"
        )
        data["low"] = get_stock_timeseries_element_alphavantage(
            stockDataAlphavantage, parentCategory, "3. low"
        )
        data["close"] = get_stock_timeseries_element_alphavantage(
            stockDataAlphavantage, parentCategory, "4. close"
        )
        data["volume"] = get_stock_timeseries_element_alphavantage(
            stockDataAlphavantage, parentCategory, "5. volume"
        )
    return data


def get_stock_timeseries_element_alphavantage(
    dataFromFile, parentCategory="Time Series (Daily)", timeseriesElement="4. close"
):
    if parentCategory in dataFromFile and len(dataFromFile[parentCategory]) != 0:
        return {
            key: val[timeseriesElement]
            for key, val in dataFromFile[parentCategory].items()
            if timeseriesElement in val
        }
    return {}
