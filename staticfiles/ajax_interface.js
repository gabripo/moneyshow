import { update_plot, show_text_below_canvas, toggle_lag_days_dropdown, is_json_response } from "./helper_functions.js";

export function ajax_call_show(targetUrl, tickerText, checkboxVal, apiProvider, daysToDownload) {
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {
            'ticker': tickerText,
            'update': checkboxVal,
            'api': apiProvider,
            'days': daysToDownload,
        },
        success: function (res, status) {
            if (is_json_response(res) && targetUrl === "/get_stock_data/") {
                update_plot(res)
            } else {
                alert(res)
            }
        }
    });
}

export function ajax_call_generic(targetUrl, dataInput) {
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {
            'inputGeneric': dataInput,
        },
        success: function (res, status) {
            if (targetUrl === "/clear_stock_data/") {
                console.log("Clearing database...")
                console.log(res)
            }
        }
    });
}

export function ajax_call_predict(targetUrl, tickerText, predictMethod, predictionDays, predictionLagDays) {
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {
            'ticker': tickerText,
            'predMet': predictMethod,
            'predDays': predictionDays,
            'predDaysLag': predictionLagDays
        },
        success: function (res, status) {
            update_plot(res)
            alert("Prediction Completed with method " + predictMethod);

            if (predictMethod === 'decisiontree' || predictMethod === 'randomforest') {
                show_text_below_canvas("Decision trees, at their core, are designed to capture patterns in the feature space at a given point in time, without considering the sequence of data points. They split the data based on feature values, creating if-then-else rules, but they don't account for the order in which data points appear. Temporal dependencies are all about the order and progression of data points. Think of it like this: a decision tree is like taking snapshots of moments and trying to piece them together, whereas time series models are more like watching a movie—they get the flow and progression of events. If the features are set to be the N delayed samples of the target timeseries, then the decision tree will follow the pattern defined by them - in the case of overfitting, the pattern will repeat as a multiple of N.")
            } else if (predictMethod === 'xgboost') {
                show_text_below_canvas("XGBoost, like other machine learning models, thrives on having relevant and informative features to make accurate predictions. In the context of time series data, time lags provide crucial historical information that the model needs to understand temporal dependencies and patterns. Without these lagged features, XGBoost lacks the context of past values and trends, which are essential for predicting future values in a time series. By incorporating time lags, we equip XGBoost with the necessary past data, enabling it to capture autocorrelation and learn from historical patterns. This leads to more robust and accurate predictions, as the model can recognize and leverage the temporal structure inherent in the data. Essentially, time lags transform raw time series data into a format that XGBoost can effectively utilize to uncover meaningful insights and relationships.")
            }
        }
    });
}

window.toggle_lag_days_dropdown = toggle_lag_days_dropdown;