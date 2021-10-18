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
