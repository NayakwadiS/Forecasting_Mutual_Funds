from Algorithms import *


def getDataFrame(scheme_code):
    def decorate(func):
        def decorated(*args,**kwargs):
            df = yf.download(str(scheme_code)+".BO",period='max')
            df = df.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
            df = df.rename(columns={'Close': 'nav'})
            df.reset_index(inplace=True)
            df['date'] = df['Date'].dt.strftime('%Y-%m-%d')

            info = yf.Ticker(str(scheme_code)+".BO").get_info()
            details = {'scheme_name': info['longName'], 'scheme_code': str(scheme_code)}
            return func(df,details)
        return decorated
    return decorate


def data_frame(func):
    def decorated(*args,**kwargs):
        df = yf.download(str(*args) + ".BO", period='max')
        df = df.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
        df = df.rename(columns={'Close': 'nav'})
        df.reset_index(inplace=True)
        df['date'] = df['Date'].dt.strftime('%Y-%m-%d')
        info = yf.Ticker(str(*args) + ".BO").get_info()
        details = {'scheme_name': info['longName'], 'scheme_code': str(*args)}
        return func(df,details)
    return decorated
