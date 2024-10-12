import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.pipeline import Pipeline


def predictor_linear(
    data: pd.DataFrame, nDays=10, useCrossValidation=True
) -> pd.DataFrame:
    dates = data.index
    X = pd.DataFrame({"index": range(len(data))}, index=dates)
    y = data["close"]  # only data at closing is considered for a day

    lastDay = data.index[-1]
    futureDates = generate_futureDates(lastDay, nDays)
    predictionDf = initialize_prediction_df(futureDates, len(data))
    if useCrossValidation:
        bestParams = model_best_parameters(LinearRegression, X, y)
        bestPipeline = build_pipeline(LinearRegression, bestParams)
        bestPipeline.fit(X, y)
        y_pred = bestPipeline.predict(predictionDf[["index"]])
    else:
        # 1-shot, training over the entire data-set
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(predictionDf[["index"]])
    predictionDf["close"] = y_pred

    data["index"] = np.arange(len(data))
    data = pd.concat(
        [data, predictionDf]
    )  # TODO make predictions for open, high, low, volume as well
    return data


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


def model_best_parameters(model, X: pd.DataFrame, y: pd.Series) -> dict:
    parametersGrid = model_parameters_combinations_linear()
    bestScore = float("-inf")
    bestParams = None
    for params in parametersGrid:
        scoreCurrParams = evaluate_model_cross_validation(model, params, X, y)
        if scoreCurrParams > bestScore:
            bestScore = scoreCurrParams
            bestParams = params
    return bestParams


def model_parameters_combinations_linear() -> list[dict]:
    parametersGridLinearRegressor = [
        {"fit_intercept": True},
        {"fit_intercept": False},
    ]
    return parametersGridLinearRegressor


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
