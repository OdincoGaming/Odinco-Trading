import os
import csv
import pandas as pd

symbol = "AAPL"
filename = "\\" + symbol + ".csv"
path = os.getcwd() + filename
with open(path, newline='') as csvfile:
    reader = list(csv.reader(csvfile, delimiter='', quotechar='|'))
    length = len(reader)
    for i in range(length):
        reader[i][0] = reader[i][0][5:]
    df = pd.DataFrame(reader)
    df.to_csv(f'./{symbol}_cleaned.csv')