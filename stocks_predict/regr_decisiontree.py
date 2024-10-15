import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from stocks_predict.common_regr import (
    timeshift_pandaseries_remove_lags,
    timeshift_pandaseries_to_dataframe,
)
from stocks_predict.regr_linear import (
    build_pipeline,
    generate_futureDates,
    initialize_prediction_df,
)


def predictor_decisiontree(
    data: pd.DataFrame,
    nDaysToPredict=10,
    useCrossValidation=True,
    appendToInitDf=False,
    timeLagSamples=5,
) -> pd.DataFrame:
    nDays = len(data)

    lastDay = data.index[-1]
    futureDates = generate_futureDates(lastDay, nDaysToPredict)
    predictionDf = initialize_prediction_df(futureDates, nDays)

    elementsToPredict = ("open", "high", "low", "close")
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
        data["index"] = np.arange(nDays)  # needed to append values afterwards
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
        bestParams = model_best_parameters(DecisionTreeRegressor(), X_train, y_train)
        bestPipeline = build_pipeline(DecisionTreeRegressor, bestParams)
        bestPipeline.fit(X_train, y_train)
    else:
        # 1-shot, training over the entire data-set
        bestPipeline = DecisionTreeRegressor()
        bestPipeline.fit(X_train, y_train)

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


def model_best_parameters(model, X: pd.DataFrame, y: pd.Series) -> dict:
    parametersGrid = model_parameters_combinations_decisiontree()
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


def model_parameters_combinations_decisiontree() -> list[dict]:
    parametersGridDecisionTreeRegressor = {
        "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"],
        "splitter": ["best", "random"],
        "max_depth": [None, 10, 20, 30, 40, 50],
        "min_samples_split": [2, 10, 20, 30],
        "min_samples_leaf": [1, 5, 10, 15],
        "min_weight_fraction_leaf": [0.0, 0.1, 0.2],
        "max_features": [None, "sqrt", "log2"],
        "max_leaf_nodes": [None, 5, 10, 20],
        "min_impurity_decrease": [0.0, 0.1, 0.2],
        "ccp_alpha": [
            0.0,
            0.1,
            0.2,
        ],  # complexity parameter used for Minimal Cost-Complexity Pruning
    }
    return parametersGridDecisionTreeRegressor
