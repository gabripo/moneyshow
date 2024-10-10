import os
import json
from stocks_show.libs.api_handler import get_stock_timeseries_alphavantage


def get_default_stock_data(tickerInput):
    stockData = {}
    stockData["ticker"] = tickerInput
    stockData["prices"] = get_default_stock_data_prices()
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
        data["open"] = {"default1": 1, "default2": 0}
        data["high"] = {"default1": 1, "default2": 0}
        data["low"] = {"default1": 1, "default2": 0}
        data["close"] = {"default1": 1, "default2": 0}
        data["volume"] = {"default1": 1, "default2": 0}
    return data
