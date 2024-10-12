import pandas as pd
from stocks_predict.regr_linear import predictor_linear


def forward_to_prediction(stockData: dict, predictionMode="linear", predictionDays=10):
    """
    function to forward stock data to a prediction function
    the input stock data will be changed in-place
    """
    stockDataFrame = convert_data_to_pandas_dataframe(stockData)
    if predictionMode == "linear":
        stockDataFrame = predictor_linear(stockDataFrame, predictionDays)
    elif predictionMode == "decisiontree":
        pass
    elif predictionMode == "randomforest":
        pass
    elif predictionMode == "xgboost":
        pass
    # TODO ensure pass by reference, overwrite stockData before returning
    return


def convert_data_to_pandas_dataframe(data: dict) -> pd.DataFrame:
    if "prices" in data:
        df = pd.DataFrame(data["prices"])
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
    else:
        df = pd.DataFrame()
    return df
