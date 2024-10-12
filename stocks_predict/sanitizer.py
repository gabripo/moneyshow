from stocks_show.libs.dummy_data import get_default_stock_data
from stocks_predict.constants import INVALID_STOCK_POINT
import random


def sanitize_prediction(stockData):
    if "ticker" not in stockData:
        stockData["ticker"] = "GOOG"
    if "prices" not in stockData:
        stockData = get_default_stock_data(stockData["ticker"])
    else:
        for dayIndex, dayPoint in enumerate(stockData["prices"]):
            validVal = find_first_valid_daypoint_val(dayPoint)
            for key in dayPoint.keys():
                if dayPoint.get(key, INVALID_STOCK_POINT) == INVALID_STOCK_POINT:
                    print(
                        f"{key} value of day {dayIndex} is invalid and will be overwritten"
                    )
                    stockData["prices"][dayIndex][key] = validVal + random.random()
    return


def find_first_valid_daypoint_val(dayPoint: dict):
    valueNames = ("open", "high", "low", "close")
    for name in valueNames:
        if dayPoint.get(name, INVALID_STOCK_POINT) != INVALID_STOCK_POINT:
            return dayPoint[name]
    return INVALID_STOCK_POINT
