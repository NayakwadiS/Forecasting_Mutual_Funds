from Algorithms import *


def linear(df):
    days = 30
    last_week = df.iloc[-days:]
    last_day = df.iloc[-1:]

    df_new = df
    df_new['date'] = pd.to_datetime(df_new['date'], dayfirst=True)
    df_new['Prev CloseNAV'] = df_new['nav']
    df_new['NAV'] = df_new['nav'].shift(1)
    df_new.set_index('date', inplace=True)

    X = df_new[['Prev CloseNAV']][1:]
    y = df_new['NAV'][1:]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # To Train model on previous data
    model = LinearRegression().fit(X_train, y_train)
    r_sq = model.score(X_test, y_test)
    # print('confidence of determination:', r_sq)
    # print('intercept:', model.intercept_)
    # print('slope:', model.coef_)

    # for Test purpose to check confidence of model
    y_pred_test = model.predict(X_test)
    #RMSE
    rmse= math.sqrt(mean_squared_error(y_test,y_pred_test))

    # Actual prediction
    pre_date = date.today()
    day_index = [(pre_date + dt.timedelta(days=i)) for i in range(1,31)]
    last_week = [float(row['nav']) for index,row in last_week.iterrows()]

    # 1 day forecasting
    X_new = pd.DataFrame(float(last_day['nav']),columns =['Prev CloseNAV'],index=[pre_date])
    y_pred = model.predict(X_new)
    # print("1 day prediction :",y_pred)

    y_pred_30 = [y_pred]
    # month forecasting
    for i in range(0,29):
        X_new = pd.DataFrame(y_pred,columns =['Prev CloseNAV'],index=[day_index[i]])
        y_pred = model.predict(X_new)
        y_pred_30.append(y_pred)

    return y_pred_30, rmse