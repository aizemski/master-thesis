from constants import *
from src.data import load_all_downloaded_data_for_pair, prepare_data_for_close
from src.models.lstm_reggression import LSTM_reggression
from src.models.rl_trader import train_rl

if __name__ == '__main__':
    i = 0
    # download(trading_type=TRADING_TYPE[0], symbols=[TICKERS[i] +
    #                                                 BASE], intervals=['15m'], years=[2020, 2022],
    #          months=list(range(1, 13)))
    frame = load_all_downloaded_data_for_pair(TICKERS[i], BASE)
    frame = frame[-50:]
    # frame['Cash'], frame['Asset'] = optimal_for_all_data(frame)
    # reg = LSTM_reggression()
    # reg.train(frame)
    train_rl(frame, 10)
