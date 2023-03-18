import yfinance as yf
# import pendulum
# import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import pandas as pd
import os
# from multiprocessing import Pool
import numpy as np
import sqlite3 as sl

# NEEDED FEATURES 3/13/2023:
# - Save Date of Found Stock
# - Write to CSV Purchased Stock
# - Calculate Overall Gains
# - Compare

DAYSBEHIND = 90
DAYEND = 0

def identifyStocks(con):
    print("\rIdentifying stocks...", end="\r")
    # Possible multiprocessing here?
    # with Pool(processes=4) as pool:
    demo = csvSearcher('demo.csv')
    # fortune = csvSearcher('fortune.csv')

    stocks = demo # Bypasses concatenation for multiprocessing
    # stocks = np.unique(np.concatenate((np.array(demo), np.array(fortune))))
    viable = []
    for i in stocks:
        print("\rPrice averaging " + str(i[0]) + "...                               ", end="\r")
        average = averageFinder(i[0])
        percent = 100 - ((i[1] / average) * 100)
        if percent >= 5:
            viable.append([i[0], i[1]])
    print("IdentifyStocks connected successfully.")
    con.execute("DROP TABLE IF EXISTS CURRENT")
    con.execute("""CREATE TABLE CURRENT(tick TEXT, price REAL);""")
    si = 'INSERT OR REPLACE INTO CURRENT (tick, price) values(?, ?)'
    con.executemany(si, viable)
    con.commit()
    return viable

def averageFinder(ticker):
    tick = yf.Ticker(ticker)
    start_date = (datetime.now() - timedelta(days=DAYSBEHIND)).strftime('%Y-%m-%d')
    end_date = (datetime.now() - timedelta(days=(DAYEND + 2))).strftime('%Y-%m-%d')
    ticker_hist = tick.history(start=start_date, end=end_date)
    ticker_hist.to_string()
    datecount = 0
    high = 0
    for i in ticker_hist["High"]:
        high = high + i
        datecount = datecount + 1
    return high / datecount
                
def csvSearcher(filename):
    stocks = []
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ticker = row['Ticker']
            print("\rEvaluating " + str(filename) + ", ticker " + str(ticker) + "...", end="\r")
            tick = yf.Ticker(ticker)
            start_date = (datetime.now() - timedelta(days=DAYSBEHIND)).strftime('%Y-%m-%d')
            end_date = (datetime.now() - timedelta(days=DAYEND)).strftime('%Y-%m-%d')
            ticker_hist = tick.history(start=start_date, end=end_date)
            ticker_hist.to_string()
            lowestHigh = 99999 * 99999
            datecount = 0
            lowHighDate = DAYSBEHIND * 2
            for i in ticker_hist["High"]:
                datecount = datecount + 1
            for i in ticker_hist["High"]:
                datecount = datecount - 1
                if i < lowestHigh:
                    lowHighDate = datecount
                    lowestHigh = i
            if lowHighDate <= 1:
                stocks.append([ticker,lowestHigh])
    return stocks

if __name__ == "__main__":
    con = sl.connect('lossleader.db')
    viable = identifyStocks(con)
    print(viable)