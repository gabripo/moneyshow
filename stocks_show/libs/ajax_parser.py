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
