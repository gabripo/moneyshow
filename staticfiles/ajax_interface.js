function ajax_call_show(targetUrl, tickerText, checkboxVal, apiProvider) {
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {
            'ticker': tickerText,
            'update': checkboxVal,
            'api': apiProvider,
        },
        success: function (res, status) {
            if (targetUrl === "/get_stock_data/") {
                update_plot(res)
            }
        }
    });
}

function ajax_call_generic(targetUrl, dataInput) {
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

function ajax_call_predict(targetUrl, tickerText, predictMethod, predictionDays) {
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {
            'ticker': tickerText,
            'predMet': predictMethod,
            'predDays': predictionDays
        },
        success: function (res, status) {
            console.log("Predicting...")
            update_plot(res)
            console.log("Prediction plotted")
            if (predictMethod === 'decisiontree') {
                console.log("Decision trees, at their core, are designed to capture patterns in the feature space at a given point in time, without considering the sequence of data points. They split the data based on feature values, creating if-then-else rules, but they don't account for the order in which data points appear. Temporal dependencies are all about the order and progression of data points. Think of it like this: a decision tree is like taking snapshots of moments and trying to piece them together, whereas time series models are more like watching a movie—they get the flow and progression of events.")
            }
        }
    });
}

function update_plot(res) {
    var tickerDisplay = res['ticker'];
    var priceSeries = res['prices'];
    $('#greatChart').remove(); // remove the canvas of the old plot
    $('#graph-area').append('<canvas id="greatChart"><canvas>'); // add the canvas of the new plot
    const priceSeriesFormatted = priceSeries.map(
        ({ date, open, high, low, close }) =>
        ({
            x: new Date(date).getTime(),
            o: open,
            h: high,
            l: low,
            c: close
        })
    );

    const closeDataFormatted = priceSeries.map(
        ({ date, close }) =>
        ({
            x: new Date(date).getTime(),
            y: close
        })
    )

    const dataToPlot = {
        datasets: [{
            label: 'OHLC for symbol ' + tickerDisplay,
            data: priceSeriesFormatted
        },
        {
            label: 'Close price',
            type: 'line',
            data: closeDataFormatted,
            borderColor: 'red',
            hidden: true,
        }]
    }

    const options = {
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            title: {
                display: true,
                text: tickerDisplay
            },
            tooltip: {
                enabled: true,
                mode: 'nearest',
                intersect: false,
                callbacks: {
                    label: function (context) {
                        const point = context.raw;
                        let labels = [];
                        if (point.o !== undefined) labels.push(`Open: ${point.o}`);
                        if (point.h !== undefined) labels.push(`High: ${point.h}`);
                        if (point.l !== undefined) labels.push(`Low: ${point.l}`);
                        if (point.c !== undefined) labels.push(`Close: ${point.c}`);
                        return labels.length ? labels : `Value: ${point.y}`;
                    }
                }
            },
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                }
            },
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    displayFormats: {
                        day: 'D'
                    },
                },
            },
            y: {
                beginAtZero: false
            }
        }
    };

    const ctx = document.getElementById('greatChart').getContext('2d');
    new Chart(ctx, {
        type: 'candlestick',
        data: dataToPlot,
        options: options
    });
}