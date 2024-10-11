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
                // stock price and SMA data for the user-specified ticker is now in the "res" object
                var tickerDisplay = res['ticker'];
                var priceSeries = res['prices'];
                var graphTitle = tickerDisplay

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
                            text: graphTitle
                        },
                        tooltip: {
                            enabled: true,
                            mode: 'nearest',
                            intersect: false,
                            callbacks: {
                                label: function (context) {
                                    const point = context.raw;
                                    return [
                                        `Open: ${point.o}`,
                                        `High: ${point.h}`,
                                        `Low: ${point.l}`,
                                        `Close: ${point.c}`
                                    ];
                                }
                            }
                        },
                        zoom: {
                            pan: {
                                enabled: true,
                                mode: 'xy'
                            },
                            zoom: {
                                enabled: true,
                                mode: 'xy',
                                drag: {
                                    enabled: true,
                                    borderColor: 'rgba(0, 0, 0, 0.5)',
                                    borderWidth: 1,
                                    backgroundColor: 'rgba(225,225,225,0.3)'
                                }
                            }
                        }
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