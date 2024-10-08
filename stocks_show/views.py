from django.shortcuts import render
from django.http import HttpResponse
from stocks_processing.parse_secrets import ALPHA_ADVANTAGE_API_KEY
from django.views.decorators.csrf import csrf_exempt
from .models import StockData
import requests
import json

# making possible to load stock prices from the database instead of from the AlphaVantage APIs
DATABASE_ACCESS = False


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
        tickerInput = request.POST.get(
            "ticker", "null"
        )  # get ticker from the AJAX POST request
        tickerInput = tickerInput.upper()

        if DATABASE_ACCESS == True:
            # checking if the database already has data stored for this ticker before querying the Alpha Vantage API
            if StockData.objects.filter(
                ticker=tickerInput
            ).exists():  # Django's way of saying SELECT * FROM StockData WHERE ticker = tickerInput
                # We have the data in our database! Get the data from the database directly and send it back to the frontend AJAX call
                entry = StockData.objects.filter(ticker=tickerInput)[0]
                return HttpResponse(entry.prices, content_type="application/json")

        # get adjusted close data from Alpha Vantage APIs , parse data into a JSON dictionary
        price_series = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={tickerInput}&apikey={ALPHA_ADVANTAGE_API_KEY}&outputsize=full"
        ).json()

        # get SMA (simple moving average) data from Alpha Vantage APIs , parse data into a JSON dictionary
        sma_series = requests.get(
            f"https://www.alphavantage.co/query?function=SMA&symbol={tickerInput}&interval=daily&time_period=10&series_type=close&apikey={ALPHA_ADVANTAGE_API_KEY}"
        ).json()

        output_dictionary = {}
        output_dictionary["prices"] = price_series
        output_dictionary["sma"] = sma_series

        # save the dictionary to database
        temp = StockData(ticker=tickerInput, prices=json.dumps(output_dictionary))
        temp.save()

        # return the data back to the frontend AJAX call
        return HttpResponse(
            json.dumps(output_dictionary), content_type="application/json"
        )

    else:
        message = "Not Ajax"
        return HttpResponse(message)


def is_ajax(request):
    """
    function to ensure that a request is an AJAX POST request from the frontend
    """
    return request.headers.get("x-requested-with") == "XMLHttpRequest"
