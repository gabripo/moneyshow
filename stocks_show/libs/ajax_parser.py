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


def get_api_name_from_request(request) -> str:
    apiName = request.POST.get("api", "database")
    return apiName


def get_prediction_method_from_request(request) -> str:
    predictionMethodInput = request.POST.get("inputGeneric[predMethod]", "none")
    return predictionMethodInput
