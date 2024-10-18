import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from stocks_predict.common_regr import (
    predict_future_days,
    timeshift_pandaseries_remove_lags,
    timeshift_pandaseries_to_dataframe,
)
from stocks_predict.constants import CROSS_VALIDATION_SETS
from stocks_predict.regr_linear import (
    build_pipeline,
    initialize_prediction_df,
)


def predictor_randomforest(
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
    if useCrossValidation and len(y_train) > CROSS_VALIDATION_SETS:
        bestParams = model_best_parameters(RandomForestRegressor(), X_train, y_train)
    else:
        bestParams = {}  # default parameters will be used
    bestPipeline = build_pipeline(RandomForestRegressor, bestParams)
    bestPipeline.fit(X_train, y_train)

    y_pred = predict_future_days(X_train, y_train, nDaysToPredict, bestPipeline)
    return y_pred


def model_best_parameters(model, X: pd.DataFrame, y: pd.Series) -> dict:
    parametersGrid = model_parameters_combinations_randomforest()
    grid_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=parametersGrid,
        cv=CROSS_VALIDATION_SETS,
        scoring="neg_mean_squared_error",
        # verbose=10,
    )
    grid_search.fit(X, y)
    bestParams = grid_search.best_params_
    return bestParams


def model_parameters_combinations_randomforest() -> list[dict]:
    parametersGridRandomForestRegressor = {
        "n_estimators": [50, 100, 200, 300],
        "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"],
        "max_depth": [None, 10, 20, 30, 40, 50],
        "min_samples_split": [2, 10, 20, 30],
        "min_samples_leaf": [1, 5, 10, 15],
        "min_weight_fraction_leaf": [0.0, 0.1, 0.2],
        "max_features": [None, "sqrt", "log2"],
        "max_leaf_nodes": [None, 5, 10, 20],
        "min_impurity_decrease": [0.0, 0.1, 0.2],
        "bootstrap": [False],
        "n_jobs": [-1],  # use all the possible processors
        "warm_start": [True, False],
        "ccp_alpha": [
            0.0,
            0.1,
            0.2,
        ],  # complexity parameter used for Minimal Cost-Complexity Pruning
    }
    return parametersGridRandomForestRegressor
