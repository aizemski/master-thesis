import random
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import tensorflow as tf
from collections import deque
from tqdm import tqdm

from src.data import prepare_data_for_close


class RL_trader():
    def __init__(self, state_size, action_space=3):
        self.state_size = state_size
        self.action_space = action_space
        self.memory = deque(maxlen=200)
        self.inventory = []
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_final = 0.01
        self.epsilon_decay = 0.995
        self.model = self.model__init__()
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def model__init__(self):
        return Sequential([
            LSTM(units=64, activation='relu', return_sequences=True,
                 input_shape=(self.state_size[0], self.state_size[1])),
            Dropout(0.2),
            LSTM(units=64, activation='relu'),
            Dropout(0.2),
            Dense(units=self.action_space, activation='relu')]
        )

    def trade(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_space)
        return np.argmax(self.model.predict(state))

    def batch_train(self, batch_size):

        batch = []
        for i in range(len(self.memory) - batch_size + 1, len(self.memory)):
            batch.append(self.memory[i])

        for state, action, reward, next_state, done in batch:
            reward = reward
            if not done:
                reward = reward + self.gamma * (next_state[0][-1][3] - next_state[0][-2][3])

            target = self.model.predict(state)
            target[0][action] = reward

            self.model.fit(state, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_final:
            self.epsilon *= self.epsilon_decay


def train_rl(data, seq_len, epochs=100, batch_size=16):
    trader = RL_trader(state_size=(seq_len, data.shape[1]))

    for epoch in range(1, epochs + 1):

        print("epoch: {}/{}".format(epoch, epochs))
        x_data, y_data = prepare_data_for_close(data, seq_len)
        tmp = len(x_data) - 1
        state = x_data[1].reshape(1, seq_len, data.shape[1])

        total_profit = 1
        trader.inventory = []

        for t in tqdm(range(1, tmp)):

            action = trader.trade(state.reshape(1, seq_len, data.shape[1]))

            next_state = x_data[t + 1].reshape(1, seq_len, data.shape[1])
            reward = 0

            if action == 1:
                # Buy
                trader.inventory.append(y_data[t])

            elif action == 2 and len(trader.inventory) > 0:
                # Sell
                buy_price = trader.inventory.pop(0)

                reward = max(y_data[t] - buy_price, 0)
                total_profit *= np.exp(y_data[t] - buy_price)

            if t == tmp - 1:
                done = True
            else:
                done = False

            trader.memory.append((state, action, reward, next_state, done))

            state = next_state

            if done:
                print("Earnings: {0:2f}%".format((total_profit - 1) * 100))
                print(trader.epsilon)

            if len(trader.memory) > batch_size:
                trader.batch_train(batch_size)

        if epoch % 10 == 0:
            trader.model.save("rl_trader_{}.h5".format(epoch))
