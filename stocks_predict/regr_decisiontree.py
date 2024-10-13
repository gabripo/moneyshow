import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from stocks_predict.regr_linear import (
    build_pipeline,
    generate_futureDates,
    initialize_prediction_df,
)


def predictor_decisiontree(
    data: pd.DataFrame, nDaysToPredict=10, useCrossValidation=True, appendToInitDf=False
) -> pd.DataFrame:
    dates = data.index
    nDays = len(data)
    X = pd.DataFrame({"index": range(nDays)}, index=dates)

    lastDay = data.index[-1]
    futureDates = generate_futureDates(lastDay, nDaysToPredict)
    predictionDf = initialize_prediction_df(futureDates, nDays)

    elementsToPredict = ("open", "high", "low", "close")
    for key in elementsToPredict:
        predictionDf[key] = predict_day_element(
            X, data[key], predictionDf[["index"]], useCrossValidation
        )

    if appendToInitDf:
        data["index"] = np.arange(nDays)  # needed to append values afterwards
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
        bestParams = model_best_parameters(DecisionTreeRegressor(), X_train, y_train)
        bestPipeline = build_pipeline(DecisionTreeRegressor, bestParams)
        bestPipeline.fit(X_train, y_train)
        y_pred = bestPipeline.predict(X_pred)
    else:
        # 1-shot, training over the entire data-set
        model = DecisionTreeRegressor()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_pred)
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
