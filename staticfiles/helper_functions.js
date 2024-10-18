export function update_plot(res) {
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

    const openDataFormatted = format_data_priceseries(priceSeries, 'open')
    const highDataFormatted = format_data_priceseries(priceSeries, 'high')
    const lowDataFormatted = format_data_priceseries(priceSeries, 'low')
    const closeDataFormatted = format_data_priceseries(priceSeries, 'close')


    const dataToPlot = {
        datasets: [{
            label: 'OHLC for symbol ' + tickerDisplay,
            data: priceSeriesFormatted
        },
        {
            label: 'Open price',
            type: 'line',
            data: openDataFormatted,
            borderColor: 'blue',
            hidden: true,
        },
        {
            label: 'High price',
            type: 'line',
            data: highDataFormatted,
            borderColor: 'yellow',
            hidden: true,
        },
        {
            label: 'Low price',
            type: 'line',
            data: lowDataFormatted,
            borderColor: 'orange',
            hidden: true,
        },
        {
            label: 'Close price',
            type: 'line',
            data: closeDataFormatted,
            borderColor: 'red',
            hidden: true,
        }
        ]
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
            annotation: {
                annotations: {
                    verticalLine: {
                        type: 'line',
                        xMin: get_today_date(),
                        xMax: get_today_date(),
                        borderColor: 'red',
                        borderWidth: 2
                    }
                }
            },
            zoom: {
                zoom: {
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                    drag: {
                        enabled: true
                    }
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
    const chart = new Chart(ctx, {
        type: 'candlestick',
        data: dataToPlot,
        options: options
    });

    document.getElementById('reset_zoom').addEventListener('click', function () {
        chart.resetZoom();
    });
}

export function is_json_response(response) {
    if (typeof response !== "string") {
        var value = JSON.stringify(response);
    } else {
        var value = response;
    }

    try {
        value = JSON.parse(value);
    } catch (error) {
        return false;
    }

    if (typeof value === "object" && value !== null) {
        return true;
    } else {
        return false;
    }
}

export function format_data_priceseries(priceSeries, fieldName) {
    const dataFormatted = priceSeries.map(
        ({ date, [fieldName]: fieldValue }) =>
        ({
            x: new Date(date).getTime(),
            y: fieldValue
        })
    )

    return dataFormatted;
}


export function get_today_date() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');

    const todayDateFormatted = `${year}-${month}-${day}`;

    return todayDateFormatted;
}

export function show_text_below_canvas(textToShow) {
    const textElement = document.getElementById("text_field");

    textElement.innerText = textToShow;
}


export function toggle_lag_days_dropdown() {
    const mainDropdown = document.getElementById('selection_ml');
    const secondaryDropdownContainer = document.getElementById('prediction_lag_days_dropdown');

    const regressorRequiringLagDays = ['decisiontree', 'randomforest', 'xgboost'];

    if (regressorRequiringLagDays.includes(mainDropdown.value)) {
        secondaryDropdownContainer.classList.remove('hidden');
    } else {
        secondaryDropdownContainer.classList.add('hidden');
    }
}