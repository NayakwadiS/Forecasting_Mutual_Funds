from Algorithms import *


def _prepare_yf_nav_dataframe(symbol_code):
    df = yf.download(f"{symbol_code}.BO", period='max')
    if df.empty:
        raise ValueError(f"No market data found for code: {symbol_code}")

    # yfinance may return MultiIndex columns on newer versions; flatten them.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df.reset_index()
    drop_cols = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    if 'Close' not in df.columns:
        raise ValueError(f"'Close' column not found for code: {symbol_code}")

    df = df.rename(columns={'Close': 'nav'})
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df.dropna(subset=['Date', 'nav']).reset_index(drop=True)
    df['date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df


def getDataFrame(scheme_code):
    def decorate(func):
        def decorated(*args,**kwargs):
            df = _prepare_yf_nav_dataframe(scheme_code)

            info = yf.Ticker(str(scheme_code)+".BO").get_info()
            details = {'scheme_name': info.get('longName', str(scheme_code)), 'scheme_code': str(scheme_code)}
            return func(df,details)
        return decorated
    return decorate


def data_frame(func):
    def decorated(*args,**kwargs):
        df = _prepare_yf_nav_dataframe(str(*args))
        info = yf.Ticker(str(*args) + ".BO").get_info()
        details = {'scheme_name': info.get('longName', str(*args)), 'scheme_code': str(*args)}
        return func(df,details)
    return decorated
