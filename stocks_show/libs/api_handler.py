import requests
from stocks_show.libs.parse_secrets import ALPHA_ADVANTAGE_API_KEY


def get_stock_from_api(tickerInput, apiName="alphavantage") -> dict:
    stockData = {}
    if apiName == "alphavantage":
        stockData["ticker"] = tickerInput

        stockDataDaily = api_alphavantage_call(
            tickerInput, ALPHA_ADVANTAGE_API_KEY, "TIME_SERIES_DAILY"
        )
        if "Time Series (Daily)" in stockDataDaily:
            stockData["prices"] = get_stock_timeseries_alphavantage(
                stockDataDaily, "Time Series (Daily)"
            )
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
    if parentCategory == "Time Series (Daily)":
        data = []
        for key, val in stockDataAlphavantage[parentCategory].items():
            data.append(
                {
                    "date": key,
                    "open": val["1. open"],
                    "high": val["2. high"],
                    "low": val["3. low"],
                    "close": val["4. close"],
                    "volume": val["5. volume"],
                }
            )
    return data
