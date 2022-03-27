from sklearn.model_selection import KFold
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from src.data import prepare_data_for_close


class Lstm():
    def __init__(self, verbose=0):
        self.model = None
        self.verbose = verbose

    def train(self, data, k_fold=5, seq_len=20, batch_size=64, epochs=10):
        x_data, y_data = prepare_data_for_close(data, seq_len)
        # K fold
        skf = KFold(n_splits=k_fold, shuffle=True)
        i = 0
        for train, test in skf.split(x_data):
            print('Split-{}'.format(i + 1))
            x_train, x_test = x_data[train], x_data[test]
            y_train, y_test = y_data[train], y_data[test]

            # Create model

            # cwiczenie modelu
            history = self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size,
                                     validation_data=(x_test, y_test), verbose=self.verbose)

            # save(model,ticker,i,seq_len,epochs)
            i += 1
