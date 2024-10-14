import os
import json
from stocks_show.libs.api_handler import (
    get_stock_timeseries_alphavantage,
    sort_stock_data_by_date,
)


def get_default_stock_data(tickerInput):
    stockData = {}
    stockData["ticker"] = tickerInput
    stockData["prices"] = get_default_stock_data_prices()
    sort_stock_data_by_date(stockData)
    return stockData


def get_default_stock_data_prices(
    defaultFile="stock_prices.json", defaultFolder="stocks_show/dummies"
) -> dict:
    fullpath = os.path.join(os.getcwd(), defaultFolder, defaultFile)
    if os.path.isfile(fullpath):
        with open(fullpath, "r") as file:
            dataFromFile = json.load(file)
            data = get_stock_timeseries_alphavantage(
                dataFromFile, "Time Series (Daily)"
            )
    else:
        # fallback to simple data
        data = [
            {
                "date": "date1",
                "open": 0,
                "high": 1,
                "low": 2,
                "close": 3,
                "volume": 100,
            },
            {
                "date": "date2",
                "open": 1,
                "high": 2,
                "low": 3,
                "close": 4,
                "volume": 200,
            },
        ]
    return data
