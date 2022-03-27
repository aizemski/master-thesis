from sklearn.model_selection import KFold
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from src.data import prepare_data_for_close
from src.models.lstm import Lstm


class LSTM_classifier(Lstm):
    def __init__(self):
        super().__init__()

    def train(self, data, k_fold=5, seq_len=20, batch_size=64, epochs=10):
        if self.mode is None:
            self.model = Sequential([
                LSTM(units=128, activation='relu', return_sequences=True,
                     input_shape=(seq_len, data.shape[1])),
                Dropout(0.2),
                LSTM(units=128, activation='relu'),
                Dropout(0.2),
                Dense(units=2, activation='relu'),
                Dense(units=1, activation='sigmoid')
            ])
            self.model.compile(optimizer='adam', loss='mean_squared_error')
        super().train(data, k_fold, seq_len, batch_size, epochs)
