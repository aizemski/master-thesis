from constants import *
from download import download_monthly_klines as download
import pandas as pd
import numpy as np
import os
import glob

from src.data import load_all_downloaded_data_for_pair, prepare_data_for_close
from src.dynamic import optimal_for_all_data

if __name__ == '__main__':
    i = 0
    # download(trading_type=TRADING_TYPE[0], symbols=[TICKERS[i] +
    #                                                 BASE], intervals=['15m'], years=[2020, 2022],
    #          months=list(range(1, 13)))
    frame = load_all_downloaded_data_for_pair(TICKERS[i], BASE)
    frame = frame[-300:]
    frame['Cash'], frame['Asset'] = optimal_for_all_data(frame)
