from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stocks_predict.forwarder import forward_to_prediction
from stocks_predict.sanitizer import sanitize_prediction
from stocks_show.libs.ajax_parser import (
    db_to_update,
    get_days_from_request,
    get_prediction_days_from_request,
    get_prediction_lag_days_from_request,
    get_prediction_method_from_generic_request,
    get_ticker_from_request,
    is_ajax,
    get_api_name_from_request,
)
from stocks_show.libs.api_handler import get_stock_from_api, is_valid_api_data
from stocks_show.libs.database_handling import (
    clear_db,
    get_stock_from_db,
    is_stock_in_db,
    write_data_to_db,
)
import json

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
        apiName = get_api_name_from_request(request)
        daysToDownload = get_days_from_request(request)

        if DATABASE_ACCESS and is_stock_in_db(tickerInput) and not dbToUpdate:
            stockData = get_stock_from_db(tickerInput, daysToDownload)
        else:
            stockData = get_stock_from_api(tickerInput, apiName, daysToDownload)

        if not is_valid_api_data(stockData):
            invalidStockNameMessage = f"Stock prices for symbol {tickerInput} could not be dowloaded.\n\nIs the symbol valid?\n\nAre you connected to internet?"
            return HttpResponse(invalidStockNameMessage)
        elif not is_stock_in_db(tickerInput) or dbToUpdate:
            write_data_to_db(tickerInput, stockData)

        return HttpResponse(json.dumps(stockData), content_type="application/json")
    else:
        message = "Not Ajax"
        return HttpResponse(message)


@csrf_exempt  # decorator to protect agains CSRF
def clear_stock_data(request):
    """
    function to clear a database
    """
    if is_ajax(request):
        isDatabaseCleared = clear_db()
        if isDatabaseCleared:
            message = "Database successfully cleared"
        else:
            message = "Database not cleared"
    else:
        message = "Not Ajax"
    return HttpResponse(message)


@csrf_exempt
def predict_stock_data(request):
    """
    function to call a prediction over the available stocks
    """
    if is_ajax(request):
        predictionMethod = get_prediction_method_from_generic_request(request)
        if predictionMethod == "none":
            message = f"Invalid prediction method {predictionMethod} selected! No prediction will occur"
        else:
            ticker = get_ticker_from_request(request)
            stockData = get_stock_from_db(ticker)

            predictionArgs = {
                "stockData": stockData,
                "predictionMode": predictionMethod,
                "predictionDays": get_prediction_days_from_request(request),
                "predictionLagDays": get_prediction_lag_days_from_request(request),
            }
            predictionWorked = forward_to_prediction(**predictionArgs)
            if predictionWorked:
                sanitize_prediction(stockData)
                print(f"Prediction of {ticker} achieved with method {predictionMethod}")
            else:
                print(
                    f"Prediction of {ticker} not worked with method {predictionMethod}"
                )
            return HttpResponse(json.dumps(stockData), content_type="application/json")
    else:
        message = "Not Ajax"
    return HttpResponse(message)
