import requests
from stocks_show.libs.parse_secrets import ALPHA_ADVANTAGE_API_KEY
import yfinance as yf


def get_stock_from_api(
    tickerInput, apiName="alphavantage", nLastDaysToLoad=100
) -> dict:
    stockData = {}
    if apiName == "alphavantage":
        stockData["ticker"] = tickerInput

        apiOptions = api_alphavantage_options(
            tickerInput, ALPHA_ADVANTAGE_API_KEY, "daily", nLastDaysToLoad
        )
        stockDataDaily = api_alphavantage_call(**apiOptions)
        if "Time Series (Daily)" in stockDataDaily:
            stockData["prices"] = get_stock_timeseries_alphavantage(
                stockDataDaily, "Time Series (Daily)"
            )
    elif apiName == "yfinance":
        stockData["ticker"] = tickerInput

        stockDataYfTicker = yf.Ticker(tickerInput)
        stockDataDaily = stockDataYfTicker.history(interval="1d", period="ytd")
        if len(stockDataDaily) != 0:
            stockData["prices"] = get_stock_timeseries_yfinance(stockDataDaily)

    sort_stock_data_by_date(stockData)
    return stockData


def is_valid_api_data(stockData, groups=["prices", "sma"]) -> bool:
    """
    function to check whether fetched API data is ok to be used
    """
    validApi = False
    for group in groups:
        validApi |= (group in stockData) and (len(stockData[group]) != 0)
    return validApi


def api_alphavantage_call(
    tickerInput, apiKey, dataType="TIME_SERIES_DAILY", outputSize="full"
):
    query = f"https://www.alphavantage.co/query?function={dataType}&symbol={tickerInput}&apikey={apiKey}&outputsize={outputSize}"
    return requests.get(query).json()


def api_alphavantage_options(
    tickerInput, apiKey, stockFrequency="daily", nLastDaysToLoad=100
) -> dict:
    if nLastDaysToLoad <= 100:
        outputSize = "compact"
    else:
        outputSize = "full"

    stockFrequenciesMap = {
        "daily": "TIME_SERIES_DAILY",
        "daily_adjusted": "TIME_SERIES_DAILY_ADJUSTED",
        "weekly": "TIME_SERIES_WEEKLY",
        "weekly_adjusted": "TIME_SERIES_WEEKLY_ADJUSTED",
        "monthly": "TIME_SERIES_MONTHLY",
        "monthly_adjusted": "TIME_SERIES_MONTHLY_ADJUSTED",
    }
    dataType = stockFrequenciesMap.get(stockFrequency, "TIME_SERIES_DAILY")

    return {
        "tickerInput": tickerInput,
        "apiKey": apiKey,
        "dataType": dataType,
        "outputSize": outputSize,
    }


def get_stock_timeseries_alphavantage(
    stockDataAlphavantage, parentCategory="Time Series (Daily)"
) -> list[dict]:
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
    sorted(data, key=lambda x: x["date"])
    return data


def get_stock_timeseries_yfinance(stockDataYfinance) -> list[dict]:
    data = []
    for index, day in stockDataYfinance.iterrows():
        data.append(
            {
                "date": index.strftime("%Y-%m-%d"),
                "open": day["Open"],
                "high": day["High"],
                "low": day["Low"],
                "close": day["Close"],
                "volume": day["Volume"],
            }
        )
    return data


def sort_stock_data_by_date(stockData) -> None:
    if "prices" not in stockData:
        return
    stockData["prices"] = sorted(stockData["prices"], key=lambda x: x["date"])
