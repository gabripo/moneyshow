import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from stocks_predict.common_regr import (
    build_pipeline,
    evaluate_model_cross_validation,
    initialize_prediction_df,
)


def predictor_linear(
    data: pd.DataFrame,
    elementsToPredict: tuple,
    nDaysToPredict=10,
    useCrossValidation=True,
    appendToInitDf=False,
    **kwargs,
) -> pd.DataFrame:
    dates = data.index
    nDatesAvailable = len(data)
    lastDate = data.index[-1]
    predictionDf = initialize_prediction_df(lastDate, nDatesAvailable, nDaysToPredict)

    X = pd.DataFrame({"index": range(nDatesAvailable)}, index=dates)
    for key in elementsToPredict:
        print(f"Predicting {key} for the following {nDaysToPredict}...")
        predictionDf[key] = predict_day_element(
            X, data[key], predictionDf[["index"]], useCrossValidation
        )
        print(f"Prediction of {key} for the following {nDaysToPredict} concluded!")

    if appendToInitDf:
        data["index"] = np.arange(nDatesAvailable)  # needed to append values afterwards
        data = pd.concat([data, predictionDf])
        return data
    else:
        return predictionDf


def predict_day_element(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_pred: pd.DataFrame,
    useCrossValidation=True,
) -> np.ndarray:
    if useCrossValidation:
        bestParams = model_best_parameters(LinearRegression, X_train, y_train)
        bestPipeline = build_pipeline(LinearRegression, bestParams)
        bestPipeline.fit(X_train, y_train)
        y_pred = bestPipeline.predict(X_pred)
    else:
        # 1-shot, training over the entire data-set
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_pred)
    return y_pred


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
