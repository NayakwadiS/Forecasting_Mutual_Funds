import math
from mftool import Mftool
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.ar_model import AutoReg, AR
# from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import autocorrelation_plot,lag_plot
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import datetime as dt
from datetime import date
from datetime import timedelta
import yfinance as yf
import seaborn as sns

from Algorithms.getData import getDataFrame
from Algorithms.mf_MovingAvg import SMA
from Algorithms.mf_Linear import linear
from Algorithms.mf_AutoRegression import AutoR
from Algorithms.mf_LSTM import lstm
from Algorithms.mf_ARIMA import arima
