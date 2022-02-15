import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from keras.models import Sequential,load_model
from keras.layers import LSTM, Dense, Dropout
from pathlib import Path
import matplotlib.pyplot as plt
from data import *


def train(ticker,path='../data',k_fold=5,seq_len=20,batch_size=50,epochs=100):
    print('{} start'.format(ticker))
    
    x_data, y_data =  prepare_data(ticker,path,seq_len)

    #K fold
    skf = KFold(n_splits=k_fold, shuffle=True)
    i=0
    for train, test in skf.split(x_data):
        print('{}-{}'.format(ticker,i+1))
        x_train, x_test = x_data[train],x_data[test]
        y_train, y_test = y_data[train],y_data[test]
        
        #Tworzenie modelu 
        model = Sequential()
        model.add(LSTM(units=128, activation='relu',return_sequences=True,
                input_shape=(x_train.shape[1],x_train.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(units=128,activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(units=1))
        model.compile(optimizer='adam',loss='mean_squared_error')

        #cwiczenie modelu
        history = model.fit(x_train,y_train, epochs=epochs,batch_size=batch_size,
                validation_data=(x_test,y_test),verbose=0)

        #zapisanie wyniku modlu
        # save(model,ticker,i,seq_len,epochs)

        i+=1
    print('{} stop'.format(ticker))