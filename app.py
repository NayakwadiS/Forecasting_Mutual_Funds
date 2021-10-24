from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import HTTPException
from io import BytesIO
import base64
from Algorithms import *
import matplotlib.pyplot as plt
import matplotlib as plot
import warnings
import json

warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA', FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA', FutureWarning)

app = Flask(__name__)
plot.use('Agg')
m = Mftool()


@getData.data_frame
def main(df, details):
    df_new = df['nav'].iloc[-100:].astype(float)
    Y = [np.nan for i in range(len(df_new))]
    global detail
    global df_30
    detail, df_30 = details, df_new
    return Y, df


def get_plot(Y, pred):
    img = BytesIO()
    plt.figure(figsize=(12, 5))
    plt.style.use('seaborn-notebook')
    plt.plot(np.append(Y, pred), color='blue', label="Prediction")
    plt.xlabel('Next 30 Days')
    plt.ylabel('NAV')
    plt.legend()
    plt.savefig(img, format='png')
    plt.close()
    return base64.b64encode(img.getvalue()).decode('utf8')


def get_trend(Y, pred, type):
    img = BytesIO()
    plt.figure(figsize=(12, 5))
    plt.style.use('seaborn-notebook')
    plt.xlabel('Last 100 days + 30 Forecasting')
    plt.ylabel('NAV')
    plt.plot(df_30.values, color='black', label='Trend')
    plt.plot(np.append(Y, pred), color='blue', label=type)
    plt.title(type + " Forecasting for " + detail['scheme_name'])
    plt.legend()
    plt.savefig(img, format='png')
    plt.close()
    return base64.b64encode(img.getvalue()).decode('utf8')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req = request.data
        req = json.loads(req.decode('utf8').replace("'", '"'))
        # if m.is_valid_code(req['scheme']):
        Y, df = main(req['scheme'])

        def switch(x):
            return {'Linear': linear, 'Auto Regression': AutoR,
                    'ARIMA': arima, 'LSTM': lstm}[x]  # return switcher.get(x,linear)
        try:
            call = switch(req['type'])
            pred, asd = call(df)
            plot = get_trend(Y, pred, req['type'])
            trend = get_plot(Y, pred)
            return jsonify({'trend': trend, 'plot': plot})
        except Exception as e:
                raise 500
    #     raise 404
    else:
        return render_template('plot.html')


@app.errorhandler(Exception)
def internal_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return '',code


app.run(port=5000, debug=False)
