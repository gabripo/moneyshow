import pandas as pd


def forward_to_prediction(stockData: dict, predictionMode="linear"):
    """
    function to forward stock data to a prediction function
    the input stock data will be changed in-place
    """
    stockDataFrame = convert_data_to_pandas_dataframe(stockData)
    pass


def convert_data_to_pandas_dataframe(data: dict) -> pd.DataFrame:
    if "prices" in data:
        df = pd.DataFrame(data["prices"])
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
    else:
        df = pd.DataFrame()
    return df
