import yfinance as yf
import pendulum
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

# NEEDED FEATURES 3/13/2023:
# - Save Date of Found Stock
# - Write to CSV Purchased Stock
# - Calculate Overall Gains
# - Compare

DAYSBEHIND = 90
DAYEND = 0
# OWNED = []
# CASH = 3000

def identifyStocks():
    print("Identifying stocks...")
    stocks = csvSearcher('demo.csv')
    # stocks = csvSearcher('fortune.csv')
    # print(stocks)
    viable = []
    for i in stocks:
        # print(i + '\n')
        print("\rPrice averaging " + str(i[0]) + "...", end="\r")
        average = averageFinder(i[0])
        percent = 100 - ((i[1] / average) * 100)
        # print(str(i[0]) + " Percent - " + str(percent))
        if percent >= 5:
            viable.append([i[0], i[1]])
    # print(viable)
    return viable

def averageFinder(ticker):
    tick = yf.Ticker(ticker)
    start_date = (datetime.now() - timedelta(days=DAYSBEHIND)).strftime('%Y-%m-%d')
    end_date = (datetime.now() - timedelta(days=(DAYEND + 2))).strftime('%Y-%m-%d')
    print(end_date)
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
            # print(row['Ticker'])
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


    # print(amzn_hist)
    return

def amznTest():
    amzn = yf.Ticker("amzn")
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    amzn_hist = amzn.history(start=start_date, end=end_date)
    amzn_hist.to_string()
    lowestHigh = 99999 * 99999
    datecount = 0
    lowHighDate = DAYSBEHIND * 2
    for i in amzn_hist["High"]:
        datecount = datecount + 1
    for i in amzn_hist["High"]:
        datecount = datecount - 1
        if i < lowestHigh:
            lowHighDate = datecount
            lowestHigh = i
    if lowHighDate <= 1:
        readyToBuy = 1
    else:
        readyToBuy = 0
    print(readyToBuy)
    return readyToBuy
    
# def currentValue():

if __name__ == "__main__":
    # viable = identifyStocks()
    # simulator()
    viable = identifyStocks()
    print(viable)