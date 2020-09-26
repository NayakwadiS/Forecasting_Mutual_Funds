from Algorithms import *


def getDataFrame(scheme_code):
    def decorate(func):
        def decorated(*args,**kwargs):
            m = Mftool()
            details = m.get_scheme_details(scheme_code)
            data = m.get_scheme_historical_nav(scheme_code)['data']
            df = pd.DataFrame(data[::-1])  # To reverse data before creating df
            return func(df,details)
            # return details, df
        return decorated
    return decorate