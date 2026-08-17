from Algorithms import *


def linear(df):
    days = 30

    df_new = df.copy()
    df_new['date'] = pd.to_datetime(df_new['date'], errors='coerce')
    df_new['nav'] = pd.to_numeric(df_new['nav'], errors='coerce')
    df_new = df_new.dropna(subset=['date', 'nav']).reset_index(drop=True)

    df_new['Prev CloseNAV'] = df_new['nav']
    df_new['NAV'] = df_new['nav'].shift(1)
    df_new = df_new.dropna(subset=['Prev CloseNAV', 'NAV'])
    df_new = df_new.set_index('date')

    X = df_new[['Prev CloseNAV']]
    y = df_new['NAV']

    if len(X) < 2:
        raise ValueError("Not enough valid rows to train LinearRegression")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # To Train model on previous data
    model = LinearRegression().fit(X_train, y_train)
    # r_sq = model.score(X_test, y_test)
    # print('confidence of determination:', r_sq)
    # print('intercept:', model.intercept_)
    # print('slope:', model.coef_)

    # for Test purpose to check confidence of model
    y_pred_test = model.predict(X_test)
    rmse = math.sqrt(mean_squared_error(y_test, y_pred_test))

    # Actual prediction
    pre_date = date.today()
    day_index = [(pre_date + dt.timedelta(days=i)) for i in range(1, days)]

    # 1 day forecasting
    last_nav = float(df_new['Prev CloseNAV'].iloc[-1])
    X_new = pd.DataFrame([[last_nav]], columns=['Prev CloseNAV'], index=[pre_date])
    y_pred = float(model.predict(X_new)[0])

    y_pred_30 = [y_pred]
    # month forecasting
    for i in range(0, days - 1):
        X_new = pd.DataFrame([[y_pred]], columns=['Prev CloseNAV'], index=[day_index[i]])
        y_pred = float(model.predict(X_new)[0])
        y_pred_30.append(y_pred)

    return y_pred_30, rmse