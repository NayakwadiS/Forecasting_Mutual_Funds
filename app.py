from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import HTTPException
from Algorithms import *
import matplotlib as plot
import warnings
import json

warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA', FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA', FutureWarning)

app = Flask(__name__)
plot.use('Agg')
m = Mftool()


def _normalize_predictions(pred):
    flat = []
    arr = np.array(pred, dtype=float).reshape(-1)
    for value in arr:
        flat.append(float(value))
    return flat


def _build_chart_payload(df, pred, algo_name):
    history_df = df.tail(100).copy()
    history_df['Date'] = pd.to_datetime(history_df['Date'], errors='coerce')
    history_df['nav'] = pd.to_numeric(history_df['nav'], errors='coerce')
    history_df = history_df.dropna(subset=['Date', 'nav'])

    history_nav = history_df['nav'].astype(float).tolist()
    history_labels = history_df['Date'].dt.strftime('%Y-%m-%d').tolist()

    pred_values = _normalize_predictions(pred)
    if len(pred_values) > 30:
        pred_values = pred_values[:30]

    last_date = history_df['Date'].iloc[-1] if len(history_df) else pd.Timestamp.today()
    future_labels = [
        (last_date + pd.Timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(1, len(pred_values) + 1)
    ]

    labels = history_labels + future_labels
    actual_series = history_nav + [None] * len(pred_values)
    forecast_series = [None] * len(history_nav) + pred_values

    return {
        'algorithm': algo_name,
        'labels': labels,
        'actual': actual_series,
        'forecast': forecast_series,
        'history_count': len(history_nav),
        'forecast_count': len(pred_values)
    }


@getData.data_frame
def main(df, details):
    global detail
    detail = details
    return df


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req = request.data
        req = json.loads(req.decode('utf8').replace("'", '"'))
        # if m.is_valid_code(req['scheme']):
        df = main(req['scheme'])

        def switch(x):
            return {'Linear': linear, 'Auto Regression': AutoR,
                    'ARIMA': arima, 'LSTM': lstm}[x]  # return switcher.get(x,linear)
        try:
            call = switch(req['type'])
            pred, asd = call(df)
            chart_data = _build_chart_payload(df, pred, req['type'])
            return jsonify({'chart_data': chart_data, 'details': detail, 'rmse': float(asd)})
        except Exception as e:
            return jsonify({'error': 'Internal forecasting error'}), 500
    #     raise 404
    else:
        return render_template('plot.html')


@app.errorhandler(Exception)
def internal_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return '',code

app.run(port=5000, debug=True)
