from constants import *
from download import download_monthly_klines as download
import pandas as pd
import numpy as np
import os
import glob

from src.dynamic import optimal

if __name__ == '__main__':
    i = 0
    # download(trading_type=TRADING_TYPE[0], symbols=[TICKERS[i] +
    #                                                 BASE], intervals=['15m'], years=[2020, 2022],
    #          months=list(range(1, 13)))
    all_files = glob.glob(f'../data/{TICKERS[i] + BASE}/15m/*.csv')

    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None,
                         names=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time",
                                "Quote asset volume", "Number of trades", "Taker buy base asset volume",
                                "Taker buy quote asset volume", "Ignore"])
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=False)
    frame['Open time'] = pd.to_datetime(frame['Open time'], unit='ms')
    frame.set_index(keys='Open time', inplace=True)
    frame = frame.sort_index(ascending=True)
    frame_dynamic = frame[['Open', 'Close']]

    state = []
    portfolio = np.log(1)

    state.append([portfolio, portfolio])
    optimal(state, (frame_dynamic.iloc[:]['Close'].pct_change().fillna(0) + 1), prediction_period=5)
    print(len(state))
    print(len(frame))
