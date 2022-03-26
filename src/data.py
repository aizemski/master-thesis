from copy import copy
import pandas as pd
import numpy as np
import glob

DEFAULT_PARAMETERS = ["Open", "High", "Low", "Close", "Volume"]


def log_OHCLV(data):
    result = copy(data)
    result['Open'] = np.log(result['Open'])
    result['High'] = np.log(result['High'])
    result['Low'] = np.log(result['Low'])
    result['Close'] = np.log(result['Close'])
    result['Volume'] = np.log(result['Volume'])
    return result


def load_all_downloaded_data_for_pair(ticker, base, time='15m'):
    all_files = glob.glob(f'../data/{ticker + base}/{time}/*.csv')
    li = []

    for filename in all_files:
        df = load_data(filename)[["Open time", "Open", "High", "Low", "Close", "Volume"]]
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=False)
    frame['Open time'] = pd.to_datetime(frame['Open time'], unit='ms')
    frame.set_index(keys='Open time', inplace=True)
    frame = frame.sort_index(ascending=True)

    return frame


def load_data(filename):
    return pd.read_csv(filename, index_col=None,
                       names=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time",
                              "Quote asset volume", "Number of trades", "Taker buy base asset volume",
                              "Taker buy quote asset volume", "Ignore"])


def prepare_data_for_close(data, seq_len, parameters=DEFAULT_PARAMETERS):
    x_data = []
    y_data = []
    for i in range(seq_len + 1, len(data)):
        x_data.append(data.iloc[i - seq_len:i, :data.shape[1]][parameters])
        y_data.append(data.iloc[i]['Close'])
    return np.array(x_data), np.array(y_data)


def prepare_data_for_value_fuction(data, seq_len, parameters=DEFAULT_PARAMETERS):
    x_data = []
    y_data = []
    for i in range(seq_len + 1, len(data)):
        x_data.append(data.iloc[i - seq_len:i, :data.shape[1]][parameters])
        y_data.append(data.iloc[i]['Value function'])
    return np.array(x_data), np.array(y_data)
