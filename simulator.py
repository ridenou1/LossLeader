import yfinance as yf
import pendulum
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

import stockbuyer
import stockfinder

# Very incomplete simulator

DAYSBEHIND = 90 # Adapt to pass to stockbuyer
DAYEND = 0      # Adapt to pass to stockbuyer
CASH = 3000
OWNED = []

def simulator():
    if os.path.isfile('./owned.csv'):
        os.remove('./owned.csv')
    DAYSBEHIND = DAYSBEHIND + 220
    DAYEND = DAYEND + 220
    i = 220
    while i > 0:
        viable = stockfinder.identifyStocks()
        for i in viable:
            if CASH >= i[1]:
               if not os.path.isfile('./owned.csv'):
                   with open('./owned.csv', 'w', newline='') as createOwned:
                       writer = csv.writer(createOwned)
                       writer.writerow(["Ticker", "Shares"])
                       writer.writerow(i[0], i[1], 1)
               else:
                   # Need to write search function for existing shares
                   with open('./owned.csv', 'r', newline='') as ownedFile:
                       writer = csv.writer(ownedFile)       # No
                       writer.writerow([i[0], "Shares"])    # No
                   
                   
                
        DAYSBEHIND = DAYSBEHIND - 1
        DAYEND = DAYEND - 1
        i = i - 1
    stockfinder.currentValue()
    return

if __name__ == "__main__":
    simulator()