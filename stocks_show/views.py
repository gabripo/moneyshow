from django.shortcuts import render
from django.http import HttpResponse
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY
from django.views.decorators.csrf import csrf_exempt
from stocks_show.libs.ajax_parser import db_to_update, get_ticker_from_request, is_ajax
from stocks_show.libs.database_handling import (
    get_stock_from_db,
    is_stock_in_db,
    write_data_to_db,
)
import requests
import json
import os

# making possible to load stock prices from the database instead of from the AlphaVantage APIs
DATABASE_ACCESS = True


# Create your views here.
def home(request):
    return render(request, "stocks_plot/home.html", {})


@csrf_exempt  # decorator to protect agains CSRF
def get_stock_data(request):
    """
    function that:
    - takes an AJAX POST request from the .html file where it is invoked
    - returns a JSON dictionary of stock data back to the AJAX loop
    """
    if is_ajax(request):
        tickerInput = get_ticker_from_request(request)
        dbToUpdate = db_to_update(request, DATABASE_ACCESS)

        if DATABASE_ACCESS and is_stock_in_db(tickerInput) and not dbToUpdate:
            stockData = get_stock_from_db(tickerInput)
        else:
            stockData = get_stock_from_api(tickerInput, "alphavantage")
            if not is_valid_api_data(stockData):
                print("Fall back to stock data, as data invalid from the APIs...")
                stockData = get_default_stock_data(tickerInput)
            elif not is_stock_in_db(tickerInput) or dbToUpdate:
                write_data_to_db(tickerInput, stockData)

        return HttpResponse(json.dumps(stockData), content_type="application/json")
    else:
        message = "Not Ajax"
        return HttpResponse(message)


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


def get_default_stock_data(tickerInput):
    stockData = {}
    stockData["prices"] = get_default_stock_data_prices()
    stockData["prices"]["Meta Data"]["2. Symbol"] = tickerInput
    stockData["sma"] = get_default_stock_sma()
    stockData["sma"]["Meta Data"]["2. Symbol"] = tickerInput
    return stockData


def get_default_stock_data_prices(
    defaultFile="stock_prices.json", defaultFolder="stocks_show/dummies"
) -> dict:
    fullpath = os.path.join(os.getcwd(), defaultFolder, defaultFile)
    if os.path.isfile(fullpath):
        with open(fullpath, "r") as file:
            data = json.load(file)
    else:
        # fallback to simple data
        data["Meta Data"] = {}
        data["Time Series (Daily)"] = {
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
            data = json.load(file)
    else:
        # fallback to simple data
        data["Technical Analysis: SMA"] = {
            "default1": {"SMA": 2},
            "default2": {"SMA": 1},
        }
    return data
