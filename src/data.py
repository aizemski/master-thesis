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
    data = np.log(data)
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


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def state_creator(data, timestep, seq_len):
    starting_id = timestep - seq_len + 1

    if starting_id >= 0:
        windowed_data = data[starting_id:timestep + 1]
    else:
        windowed_data = starting_id * [data[0]] + list(data[0:timestep + 1])

    state = []
    for i in range(seq_len - 1):
        state.append(sigmoid(windowed_data[i + 1] - windowed_data[i]))

    return np.array([state])
