from dataPrep import csv_to_dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout


# get dataset from csv
path = os.getcwd() + "\\data\\csv\\AAPL.csv"
ohn, tin, ndon, ndo, ynorm = csv_to_dataset(path)

test_split = .9
n = int(ohn.shape[0]*test_split)

ohn_train = ohn[:n]
tin_train = tin[:n]
next_price_train = ndon[:n]

ohn_test = ohn[n:]
tin_test = tin[n:]
next_price_test = ndon[n:]

real_next_price_test = ndo[n:]

regressor = Sequential()
regressor.add(LSTM(units=50,activation='relu',return_sequences=True,
                   input_shape=(ohn_train.shape[1],6)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units=60,activation='relu',return_sequences=True))
regressor.add(Dropout(0.3))

regressor.add(LSTM(units=80,activation='relu',return_sequences=True))
regressor.add(Dropout(0.4))

regressor.add(LSTM(units=120,activation='relu'))
regressor.add(Dropout(0.5))

regressor.add(Dense(units=1))

regressor.compile(optimizer='adam',loss='mean_squared_error')

regressor.fit(ohn_train,next_price_train,epochs=10,batch_size=32)

y_pred = regressor.predict(ohn_test)
y_pred = ynorm.inverse_transform(y_pred)
np_inverse = ynorm.inverse_transform(next_price_test)

plt.figure(figsize=(14,5))
plt.plot(np_inverse, color="red",label="real price")
plt.plot(y_pred,color='blue',label='predicted price')
plt.title('predicted vs real')
plt.xlabel('time')
plt.ylabel('price')
plt.legend()
plt.show()