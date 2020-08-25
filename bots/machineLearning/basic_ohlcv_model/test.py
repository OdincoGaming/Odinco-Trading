import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

def getData(path):
    #read as pandas dataframe
    data = pd.read_csv(path)
    #split dataset
    test_split = 0.7
    n = int(data.shape[0] * test_split)
    #create and return seperated datasets
    data_train = data[:n]
    data_test = data[n:]
    return data_train, data_test

def check_for_model():
    path = os.getcwd() + "\\data\\model"
    for file_path in list(filter(lambda x: x.endswith('.h5'), os.listdir(path))):
        if file_path == 'base_model.h5':
            return True
        else:
            return False

usableList = []
path = os.getcwd() + "\\data\\csv"
#find all csv files in csv data folder
for csv_file_path in list(filter(lambda x: x.endswith('.csv'), os.listdir(path))):
    #create string out of filepath for each csv file
    filepath = path + "\\" + csv_file_path
    #read csv as pandas dataframe and split into training and testing sets
    training_data, test_data = getData(filepath)
    #scale both sets of data between 0 and 1
    scaler = MinMaxScaler()
    training_data = scaler.fit_transform(training_data)
    test_data = scaler.fit_transform(test_data)
    
    #seperate training data into 30 day chunks
    x_train = []
    y_train = []
    for i in range(30, training_data.shape[0]):
        x_train.append(training_data[i-30:i])
        y_train.append(training_data[i, 1])
    x_train, y_train = np.array(x_train), np.array(y_train)
      
    #create model
    regressor = Sequential()

    regressor.add(LSTM(units = 20, activation = 'relu', return_sequences=True,
                       input_shape=(x_train.shape[1], 6)))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units = 40, activation = 'relu', return_sequences=True))
    regressor.add(Dropout(0.3))

    regressor.add(LSTM(units = 60, activation='relu', return_sequences=True))
    regressor.add(Dropout(0.4))

    regressor.add(LSTM(units=100,activation='relu'))
    regressor.add(Dropout(0.5))

    regressor.add(Dense(units=1))

    regressor.compile(optimizer='adam', loss='mean_squared_error')

    #train model
    regressor.fit(x_train,y_train,epochs=5, batch_size=32)


    #seperate test data into chunks
    x_test = []
    y_test = []
    for i in range(30, test_data.shape[0]):
        x_test.append(test_data[i-30:i])
        y_test.append(test_data[i, 1])
    x_test, y_test = np.array(x_test), np.array(y_test)

    #predict prices
    y_pred = regressor.predict(x_test)

    #scale up values
    scale_inverse = 1/scaler.scale_[1]
    y_pred = y_pred*scale_inverse
    y_test = y_test*scale_inverse

    #plot predicted values vs real values
    plt.figure(figsize=(14,5))
    plt.plot(y_test, color="red", label="Real Prices")
    plt.plot(y_pred, color="blue", label="Predicted Prices")
    plt.title("Predicted vs Real Prices")
    plt.xlabel("Time")
    plt.ylabel("Prices")
    plt.legend()
    plt.show()