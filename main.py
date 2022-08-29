import matplotlib.pyplot as plt
import pandas as pd

from Algorithms import *
from tabulate import tabulate

scheme_code = input('Enter the MF Scheme code:- ')


@getDataFrame(scheme_code)
def forecasting_mutual_fund(df, details):
    # pred_SMA = SMA(df)
    pred_linear, rmse_linear = linear(df)
    pred_autoReg, rmse_auto = AutoR(df)
    pred_arima, rmse_arima = arima(df)
    pred_LSTM, rmse_lstm = lstm(df)

    data = [
        ['Linear', pred_linear[0], pred_linear[1], pred_linear[2], pred_linear[3], pred_linear[4]
            , min(pred_linear), max(pred_linear)],
        ['Auto Regression',pred_autoReg[0], pred_autoReg[1],pred_autoReg[2],pred_autoReg[3]
            ,pred_autoReg[4],min(pred_autoReg),max(pred_autoReg)],
        ['ARIMA', pred_arima[0], pred_arima[1], pred_arima[2], pred_arima[3], pred_arima[4],
         min(pred_arima), max(pred_arima)],
        ['LSTM', pred_LSTM[0], pred_LSTM[1],pred_LSTM[2],pred_LSTM[3],pred_LSTM[4]
            ,min(pred_LSTM),max(pred_LSTM)]
    ]
    print("\n  Time Series Forecasting for " + details['scheme_name'] + " (" + str(details['scheme_code']) + ")\n")
    print(tabulate(data, headers=["Algorithm", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5",
                                  "1 Month Low", "1 Month High"], tablefmt='orgtbl'))

    df_30 = df['nav'].iloc[-100:].astype(float)
    Y = [np.nan for i in range(len(df_30))]

    # plt.plot(df_30.values, color='black', label='Trend')  # last 100 days
    # plt.plot(np.append(Y, pred_linear), color='green', label="Linear")
    # plt.plot(np.append(Y, pred_autoReg), color='blue', label="Auto Regression")
    # plt.plot(np.append(Y,pred_arima), color='red',label='ARIMA')
    # plt.plot(np.append(Y, pred_LSTM), color='orange', label='LSTM')
    plt.xlabel('Days [last 100 + 30 forecasted]')
    plt.ylabel('NAV')
    plt.title("Forecasting for " + details['scheme_name'])
    plt.legend()
    s = df_30.append(pd.Series([np.nan for i in range(30)]))
    sns.set(style="ticks")
    data_preproc = pd.DataFrame({
        'Trends': s.values,
        'Linear': np.append(Y, pred_linear),
        'Auto Regression': np.append(Y, pred_autoReg),
        'ARIMA': np.append(Y, pred_arima),
        'LSTM': np.append(Y, pred_LSTM),
    })
    sns.lineplot(data=data_preproc)
    plt.show()

forecasting_mutual_fund()
