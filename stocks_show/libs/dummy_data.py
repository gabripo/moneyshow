import os
import json


def get_default_stock_data(tickerInput):
    stockData = {}
    stockData["ticker"] = tickerInput
    stockData["prices"] = get_default_stock_data_prices()
    stockData["sma"] = get_default_stock_sma()
    return stockData


def get_default_stock_data_prices(
    defaultFile="stock_prices.json", defaultFolder="stocks_show/dummies"
) -> dict:
    fullpath = os.path.join(os.getcwd(), defaultFolder, defaultFile)
    if os.path.isfile(fullpath):
        with open(fullpath, "r") as file:
            dataFromFile = json.load(file)
            data = dataFromFile["Time Series (Daily)"]
    else:
        # fallback to simple data
        data = {
            "default1": {"4. close": 1},
            "default2": {"4. close": 0},
        }
    return data


def get_default_stock_sma(
    defaultFile="stock_sma.json", defaultFolder="stocks_show/dummies"
) -> dict:
    fullpath = os.path.join(os.getcwd(), defaultFolder, defaultFile)
    if os.path.isfile(fullpath):
        with open(fullpath, "r") as file:
            dataFromFile = json.load(file)
            data = dataFromFile["Technical Analysis: SMA"]
    else:
        # fallback to simple data
        data = {
            "default1": {"SMA": 2},
            "default2": {"SMA": 1},
        }
    return data
