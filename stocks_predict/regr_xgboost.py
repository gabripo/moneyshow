import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from stocks_predict.regr_linear import (
    build_pipeline,
    generate_futureDates,
    initialize_prediction_df,
)


def predictor_xgboost(
    data: pd.DataFrame,
    nDaysToPredict=10,
    useCrossValidation=True,
    appendToInitDf=False,
    **kwargs,
) -> pd.DataFrame:
    dates = data.index
    nDatesAvailable = len(data)
    X = pd.DataFrame({"index": range(nDatesAvailable)}, index=dates)
    # TODO add time lag!
    lastDate = data.index[-1]
    predictionDf = initialize_prediction_df(lastDate, nDatesAvailable, nDaysToPredict)

    elementsToPredict = ("open", "high", "low", "close")
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
        bestParams = model_best_parameters(XGBRegressor(), X_train, y_train)
        bestPipeline = build_pipeline(XGBRegressor, bestParams)
        bestPipeline.fit(X_train, y_train)
        y_pred = bestPipeline.predict(X_pred)
    else:
        # 1-shot, training over the entire data-set
        model = XGBRegressor()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_pred)
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
        "max_depth": range(3, 15, 2),
        "learning_rate": np.arange(0.01, 0.3, 0.05),
        "subsample": np.arange(0.5, 1.0, 0.1),
        "colsample_bytree": np.arange(0.5, 1.0, 0.1),
        "gamma": np.arange(0, 0.5, 0.1),
        "reg_alpha": np.arange(0, 1, 0.1),
        "reg_lambda": np.arange(0, 1, 0.1),
    }
    return parametersGridXGBRegressor
