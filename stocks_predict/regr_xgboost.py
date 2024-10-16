import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from stocks_predict.common_regr import (
    predict_future_days,
    timeshift_pandaseries_remove_lags,
    timeshift_pandaseries_to_dataframe,
)
from stocks_predict.regr_linear import (
    build_pipeline,
    initialize_prediction_df,
)


def predictor_xgboost(
    data: pd.DataFrame,
    elementsToPredict: tuple,
    nDaysToPredict=10,
    useCrossValidation=True,
    appendToInitDf=False,
    **kwargs,
) -> pd.DataFrame:
    timeLagSamples = kwargs.get("timeLagSamples", 10)
    nDatesAvailable = len(data)
    lastDate = data.index[-1]
    predictionDf = initialize_prediction_df(lastDate, nDatesAvailable, nDaysToPredict)

    for key in elementsToPredict:
        print(f"Predicting {key} for the following {nDaysToPredict}...")
        y_train = data[key]
        X_train = timeshift_pandaseries_to_dataframe(y_train, timeLagSamples)
        timeshift_pandaseries_remove_lags(y_train, timeLagSamples)

        predictionDf[key] = predict_day_element(
            X_train,
            y_train,
            nDaysToPredict,
            useCrossValidation,
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
    nDaysToPredict: int,
    useCrossValidation=True,
) -> np.ndarray:
    if useCrossValidation:
        bestParams = model_best_parameters(XGBRegressor(), X_train, y_train)
    else:
        bestParams = {}
    bestPipeline = build_pipeline(XGBRegressor, bestParams)
    bestPipeline.fit(X_train, y_train)

    y_pred = predict_future_days(X_train, y_train, nDaysToPredict, bestPipeline)
    return y_pred


def model_best_parameters(model, X: pd.DataFrame, y: pd.Series) -> dict:
    parametersGrid = model_parameters_combinations_xgboost()
    grid_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=parametersGrid,
        cv=5,
        scoring="neg_mean_squared_error",
        # verbose=10,
    )
    grid_search.fit(X, y)
    bestParams = grid_search.best_params_
    return bestParams


def model_parameters_combinations_xgboost() -> list[dict]:
    parametersGridXGBRegressor = {
        "n_estimators": range(50, 500, 50),
        "learning_rate": np.arange(0.01, 0.2, 0.01),
        "max_depth": range(3, 10, 1),
        "min_child_weight": range(1, 6, 1),
        "subsample": np.arange(0.5, 1.0, 0.1),
        "colsample_bytree": np.arange(0.5, 1.0, 0.1),
        "gamma": np.arange(0, 0.5, 0.05),
    }
    return parametersGridXGBRegressor
