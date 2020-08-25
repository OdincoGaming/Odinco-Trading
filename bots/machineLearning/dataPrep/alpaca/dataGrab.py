import alpaca_trade_api as tradeapi
import os
import csv
import json
import random
from datetime import datetime
from datetime import time
import time

def GetAssets():
    input_file = open ('assets.json')
    assets = json.load(input_file)
    assetsShuffled = ShuffleList(assets)
    return assetsShuffled

def ShuffleList(test_list):
    for i in range(len(test_list)-1, 0, -1):   
        # Pick a random index from 0 to i  
        j = random.randint(0, i + 1)     
        # Swap arr[i] with the element at random index  
        test_list[i], test_list[j] = test_list[j], test_list[i]  
    return test_list

def GetData(symbol):
    limit = 1000

    #a list with a list which is a lists of lists (I assume you can send in multiple symbols at once to get a list of lists that are lists of lists)
    barset = api.get_barset(symbol, 'minute', limit=limit)

    #top level list in barset
    bars = barset[symbol]

    filename = symbol + '.csv'
    path = os.getcwd() + "\\data\\csv\\" + filename

    try:
        with open(path, 'w+', newline='') as file:
            i = 0
            fieldnames = ['time', 'open', 'high', 'low', 'close', 'volume']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            while i < limit:
                dt = bars[i].t
                timeStr = str(str(dt.hour) + str(dt.minute))
                t = int(timeStr)
                o = bars[i].o
                h = bars[i].h
                l = bars[i].l
                c = bars[i].c
                v = bars[i].v
                writer.writerow({'time' : t, 'open' : o,'high' : h,'low' : l,'close' : c,'volume' : v})
                i += 1
    except:
        print("not enough data for " + symbol)

api = tradeapi.REST(
    base_url="http://paper-api.alpaca.markets",
    key_id="PKA3G204E3WWS555WJ09",
    secret_key="g6mMfSPU1F9SuKHrG0GfN2HS5loLAEDKbMtnabpX"
)
assets = GetAssets()
length = len(assets)
for i in range(length):
    GetData(assets[i])
    time.sleep(5)
