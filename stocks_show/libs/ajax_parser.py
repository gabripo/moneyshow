from stocks_predict.constants import DEFAULT_PREDICTION_DAYS, DEFAULT_STOCK_SYMBOL


def is_ajax(request) -> bool:
    """
    function to ensure that a request is an AJAX POST request from the frontend
    """
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def get_ticker_from_request(request, tickerFieldName="ticker") -> str:
    tickerInput = request.POST.get(tickerFieldName, DEFAULT_STOCK_SYMBOL)
    tickerInput = tickerInput.upper()
    if not tickerInput:
        tickerInput = DEFAULT_STOCK_SYMBOL
    return tickerInput


def db_to_update(request, useDatabase=True) -> bool:
    updateDbInput = request.POST.get("update", "nothing")
    if useDatabase and updateDbInput == "update_db_values":
        return True
    return False


def get_api_name_from_request(request) -> str:
    apiName = request.POST.get("api", "database")
    return apiName


def get_prediction_method_from_generic_request(
    request, predMethFieldName="predMet"
) -> str:
    predictionMethodInput = request.POST.get(predMethFieldName, "none")
    return predictionMethodInput


def get_prediction_days_from_request(request) -> str:
    predictionDays = request.POST.get("predDays", DEFAULT_PREDICTION_DAYS)
    if not predictionDays:
        predictionDays = DEFAULT_PREDICTION_DAYS
    return int(predictionDays)
