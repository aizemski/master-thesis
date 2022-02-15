from constants import *
from download import download_monthly_klines as download
import pandas as pd
import os
import glob

if __name__ == '__main__':
    i= 0
    # download(trading_type=TRADING_TYPE[0], symbols=[TICKERS[i] +
    #          BASE],intervals=['15m'], years=[2020, 2021], months=list(range(1, 13)))
    all_files = glob.glob(f'../data/{TICKERS[i] + BASE}/15m/*.csv')
    # print(all_files)
    # pd.read_csv(f'../data/{TICKERS[i] + BASE}/15m')
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=1)
        li.append(df)
        break

    frame = pd.concat(li, axis=0, ignore_index=True)
    print(frame)