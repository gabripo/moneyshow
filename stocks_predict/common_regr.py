import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline


def initialize_prediction_df(
    datesArray: pd.DatetimeIndex, startIndex: int
) -> pd.DataFrame:
    predictionDf = pd.DataFrame({"date": datesArray})
    predictionDf["index"] = np.arange(startIndex, startIndex + len(predictionDf))
    predictionDf.set_index("date", inplace=True)
    return predictionDf


def generate_futureDates(
    startDay: pd.Timestamp, nDays=10, onlyBusinessDays=True
) -> pd.DatetimeIndex:
    if onlyBusinessDays:
        futureDates = pd.date_range(
            start=startDay + pd.Timedelta(days=1), periods=nDays, freq="B"
        )
    else:
        futureDates = pd.date_range(
            start=startDay + pd.Timedelta(days=1), periods=nDays
        )
    return futureDates


def evaluate_model_cross_validation(
    model, params: dict, X: pd.DataFrame, y: pd.Series, nFolds=5
) -> float:
    pipeline = build_pipeline(model, params)
    scores = cross_val_score(
        pipeline, X, y, cv=nFolds, scoring="neg_mean_absolute_error"
    )
    return scores.mean()


def build_pipeline(model, params: dict) -> Pipeline:
    pipeline = Pipeline([("regressor", model(**params))])
    return pipeline
