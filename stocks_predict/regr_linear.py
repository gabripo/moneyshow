import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np


def predictor_linear(data: pd.DataFrame):
    dates = data.index
    X = pd.DataFrame({"index": range(len(data))}, index=dates)
    y = data["close"]  # only data at closing is considered for a day

    pipeline = Pipeline([("regressor", LinearRegression())])
    cv_scores = cross_val_score(pipeline, X, y, cv=5)
    pipeline.fit(
        X, y
    )  # TODO use cross validation to find the best set of parameters before fit

    future_dates = pd.date_range(
        start=data.index[-1] + pd.Timedelta(days=1), periods=10
    )
    future_df = pd.DataFrame({"date": future_dates})
    future_df["index"] = np.arange(len(data), len(data) + len(future_df))
    future_df.set_index("date", inplace=True)
    future_df["close"] = pipeline.predict(future_df[["index"]])

    data = pd.concat(
        [data, future_df]
    )  # TODO make predictions for open, high, low, volume as well
    return
