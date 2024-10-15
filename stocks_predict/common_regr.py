import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline


def initialize_prediction_df(
    lastDate: pd.Timestamp, nDatesAvailable: int, nDaysToPredict: int
) -> pd.DataFrame:
    futureDates = generate_futureDates(lastDate, nDaysToPredict)

    predictionDf = pd.DataFrame({"date": futureDates})
    predictionDf["index"] = np.arange(nDatesAvailable, nDatesAvailable + nDaysToPredict)
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


def predict_future_days(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    nDaysToPredict: int,
    bestPipeline: Pipeline,
) -> list:
    y_pred = []
    lastDay_X = X_train.tail(1).copy()
    lastDay_y = y_train.iloc[-1]
    for _ in range(nDaysToPredict):
        newDay_X = lastDay_X.shift(axis=1)
        newDay_X["y_lag_1"] = lastDay_y

        predictedValue = bestPipeline.predict(newDay_X)[0]
        y_pred.append(predictedValue)

        lastDay_X = newDay_X
        lastDay_y = predictedValue
    return y_pred


def timeshift_pandaseries_to_dataframe(yToShift: pd.Series, nLags: int) -> pd.DataFrame:
    resDf = pd.DataFrame()
    for lag in range(1, nLags + 1):
        featureName = f"y_lag_{lag}"
        resDf[featureName] = yToShift.shift(lag)

    # filling NaN values due to timeshift
    resDf.dropna(inplace=True)
    return resDf


def timeshift_pandaseries_remove_lags(y: pd.Series, nSamplesToRemove: int) -> None:
    y.drop(y.tail(nSamplesToRemove).index, inplace=True)
