from Algorithms import *
import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA',
                        FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA',
                        FutureWarning)

def arima(df):
    days = 30
    df_new = df['nav'].astype(float)                                #.iloc[:-30] #exclude last day nav

    # df_10 = df['nav'].iloc[-30:]                                  # to test with last 30 days
    # Y = df_10.values

    X = df_new.values
    size = int(len(X) * 0.90)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    prediction = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        prediction.append(yhat)
        obs = test[t]
        history.append(obs)
        # print('predicted=%f, expected=%f' % (yhat, obs))
    rmse = math.sqrt(mean_squared_error(test, prediction))
    # print('Test MSE: %.3f' % error)

    # Actual 30 days Forecasting
    history = [x for x in X]
    forecasting = []
    for i in range(days):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        forecasting.append(yhat)    #future day
        history.append(yhat)
    print("ARIMA",forecasting)

    # plot
    # pyplot.plot(Y[-30:])                      # last 30 days
    # pyplot.plot(test[], color='green')        # 10% data used as test
    # plt.plot(forecasting, color='red')        # 30 days forecasting
    # plt.show()
    return forecasting, rmse


def arima_new(df):
    df.index = df['date']
    df['rolling_av'] = df['nav'].rolling(10).mean()
    # df[['nav', 'rolling_av']].plot()

    def plot_acf_pacf(timeseries):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
        plot_acf(timeseries, ax=ax1, lags=100)
        plot_pacf(timeseries, ax=ax2, lags=100)
        # plt.show()

    # Plotting ACF and PACF of the closing value time series,
    # https://www.geeksforgeeks.org/understanding-the-moving-average-ma-in-time-series-data/
    # plot_acf_pacf(df['nav'])

    # creating the model
    MA_model = ARIMA(endog=df['nav'], order=(0, 0, 55))

    # fitting data to the model
    results = MA_model.fit()
    # values = arimaorder(results)
    # summary of the model
    print(results.summary())

    # prediction data
    start_date = df.iloc[-10].date
    end_date = df.iloc[-1].date
    # start_date = date.today().strftime('%Y-%m-%d')
    # end_date = (date.today() + timedelta(days=days)).strftime('%Y-%m-%d')
    df['prediction'] = results.predict(start=start_date, end=end_date)
    rmse = math.sqrt(mean_squared_error(df['nav'][-10:], df['prediction'][-10:]))

    # printing last 10 values of the prediction with original and rolling avg value
    print(df[['nav', 'prediction', 'rolling_av']].tail(10))

    # Forecast future values
    # Forecast future closing prices
    forecast_steps = 30  # Forecasting for the next 30 days
    forecast_index = pd.date_range(start=df['nav'].index[-1], periods=forecast_steps + 1, freq='D')[
                     1:]  # Generate datetime index for forecast
    forecast = results.forecast(steps=forecast_steps)

    # plotting the end results
    # df[['nav', 'rolling_av', 'prediction']].plot()
    # plt.plot(forecast_index, forecast, color='red', label='Forecast')

    return forecast.tolist(), rmse
