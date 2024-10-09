from django.shortcuts import render
from django.http import HttpResponse
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY
from django.views.decorators.csrf import csrf_exempt
from .models import StockData
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

        if DATABASE_ACCESS and is_stock_in_db(tickerInput):
            stockData = get_stock_from_db(tickerInput)
        else:
            stockData = get_stock_from_api(tickerInput, "alphavantage")

        if is_valid_api_data(stockData):
            if dbToUpdate:
                write_data_to_db(tickerInput, stockData)
        else:
            stockData = get_default_stock_data(tickerInput)

        return HttpResponse(json.dumps(stockData), content_type="application/json")
    else:
        message = "Not Ajax"
        return HttpResponse(message)


def is_ajax(request) -> bool:
    """
    function to ensure that a request is an AJAX POST request from the frontend
    """
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def get_ticker_from_request(request, tickerFieldName="ticker") -> str:
    tickerInput = request.POST.get(tickerFieldName, "null")
    tickerInput = tickerInput.upper()
    return tickerInput


def db_to_update(request, useDatabase=True) -> bool:
    updateDbInput = request.POST.get("update", "nothing")
    if useDatabase and updateDbInput == "update_db_values":
        return True
    return False


def filter_stock_in_db(tickerInput):
    return StockData.objects.filter(ticker=tickerInput)


def is_stock_in_db(tickerInput) -> bool:
    filteredDb = filter_stock_in_db(tickerInput)
    return filteredDb.exists()


def get_stock_from_db(tickerInput) -> dict:
    """
    Django's way of saying SELECT * FROM StockData WHERE ticker = tickerInput
    """
    filteredDb = filter_stock_in_db(tickerInput)
    entry = filteredDb[0]
    if not entry:
        return {}
    entry_loaded = json.loads(entry.prices)
    return entry_loaded


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
            validApi &= "Time Series (Daily)" in stockData
        elif group == "sma":
            validApi &= "Technical Analysis: SMA" in stockData
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


def write_data_to_db(tickerInput, stockData) -> None:
    query_set_ticker_input = list(filter_stock_in_db(tickerInput))
    if len(query_set_ticker_input) == 0:
        instance = StockData(ticker=tickerInput, prices=json.dumps(stockData))
    else:
        instance = query_set_ticker_input[0]
        instance.ticker = tickerInput
        instance.prices = json.dumps(stockData)
    instance.save()
