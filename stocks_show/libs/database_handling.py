import json
from stocks_predict.constants import DEFAULT_DAYS_TO_DOWNLOAD
from stocks_show.libs.dummy_data import get_default_stock_data
from stocks_show.models import StockData


def write_data_to_db(tickerInput, stockData) -> None:
    query_set_ticker_input = list(filter_stock_in_db(tickerInput))
    if len(query_set_ticker_input) == 0:
        instance = StockData(ticker=tickerInput, prices=json.dumps(stockData))
    else:
        instance = query_set_ticker_input[0]
        instance.ticker = tickerInput
        instance.prices = json.dumps(stockData)
    instance.save()


def get_stock_from_db(tickerInput, nDaysToLoad=DEFAULT_DAYS_TO_DOWNLOAD) -> dict:
    """
    Django's way of saying SELECT * FROM StockData WHERE ticker = tickerInput
    """
    if not is_stock_in_db(tickerInput):
        stockData = get_default_stock_data(tickerInput)
        write_data_to_db(tickerInput, stockData)

    filteredDb = filter_stock_in_db(tickerInput)
    entry = filteredDb[0]
    if not entry:
        return {}
    entry_loaded = json.loads(entry.prices)

    nLastDaysToLoad = min(nDaysToLoad, len(entry_loaded["prices"]))
    entry_loaded["prices"] = entry_loaded["prices"][-nLastDaysToLoad:]
    return entry_loaded


def is_stock_in_db(tickerInput) -> bool:
    filteredDb = filter_stock_in_db(tickerInput)
    return filteredDb.exists()


def filter_stock_in_db(tickerInput):
    return StockData.objects.filter(ticker=tickerInput)


def clear_db() -> bool:
    clearedDb = True
    try:
        StockData.objects.all().delete()
    except:
        clearedDb = False
    return clearedDb
