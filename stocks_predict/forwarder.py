import pandas as pd
from stocks_predict.constants import INVALID_STOCK_POINT
from stocks_predict.regr_decisiontree import predictor_decisiontree
from stocks_predict.regr_linear import predictor_linear
from stocks_predict.regr_randomforest import predictor_randomforest


def forward_to_prediction(
    stockData: dict, predictionMode="linear", predictionDays=10
) -> bool:
    """
    function to forward stock data to a prediction function
    the input stock data will be changed in-place
    """
    stockDataFrame = convert_data_to_pandas_dataframe(stockData)

    predictorMapping = {
        "linear": predictor_linear,
        "decisiontree": predictor_decisiontree,
        "randomforest": predictor_randomforest,
    }
    predictorArgs = {
        "data": stockDataFrame,
        "nDaysToPredict": predictionDays,
        "useCrossValidation": True,
        "appendToInitDf": False,
    }

    prediction_function = predictorMapping.get(predictionMode)
    if prediction_function:
        predictionDataFrame = prediction_function(**predictorArgs)
    else:
        predictionDataFrame = pd.DataFrame()

    if len(predictionDataFrame) != 0:
        append_pandas_dataframe_to_data(stockData, predictionDataFrame)
        return True
    return False


def convert_data_to_pandas_dataframe(data: dict) -> pd.DataFrame:
    if "prices" in data:
        df = pd.DataFrame(data["prices"])
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
    else:
        df = pd.DataFrame()
    return df


def append_pandas_dataframe_to_data(data: dict, df: pd.DataFrame) -> dict:
    df = df.reset_index().set_index("index")
    indexesToAppend = df.index
    for i in indexesToAppend:
        dictToAppend = df.loc[i].to_dict()
        sanitize_dict_to_append(dictToAppend)
        data["prices"].append(dictToAppend)
    return


def sanitize_dict_to_append(dictToAppend: dict) -> None:
    expectedKeys = ("date", "open", "high", "low", "close")
    for key in expectedKeys:
        if key == "date":
            dictToAppend[key] = dictToAppend.get(key, "").strftime("%Y-%m-%d")
        dictToAppend[key] = dictToAppend.get(key, INVALID_STOCK_POINT)
    return
