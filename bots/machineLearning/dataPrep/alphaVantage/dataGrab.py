from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import json
import os
import time
import pandas as pd

def reset_my_index(df):
  res = df[::-1].reset_index(drop=False)
  return(res)

def saveCSV(symbol):
    api_key = "3ANCZRGOKEL9WGDK"
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
    df = data[::-1]
    df.to_csv(f'./{symbol}.csv')

# Open our JSON file and load it into python
input_file = open ('assets.json')
assets = json.load(input_file)
saveCSV("AAPL")
#for asset in assets:
#    saveCSV(asset)
#    time.sleep(30)
