import sys
import os
import yfinance as yf
import datetime as dt
import sqlite3 as sl
# import threading
# import multiprocessing
# import concurrent.futures

import csvreader

class Stock:
    def __init__(self, pp, ti, gain):
        self.pp = pp        # Simulator decision price
        self.ti = ti        # Ticker
        self.gain = gain    # Amount gain/loss

eligible = []

def find_gains(st_item):
    today = dt.date.today()
    start = today - dt.timedelta(3*30)
    stock_name = yf.Ticker(st_item.ti)
    current_stock = stock_name.history(start=start, end=today, interval="1d")
    # previous = 0
    count = 0
    original = 0
    new = 0
    for j in current_stock['Close']:
        # if count == 0:
        #     original = j
        count += 1   
        new = j
    st_item.gain = round(new - st_item.pp, 2)
    percent = round(((new / st_item.pp) * 100) - 100, 2)
    print("Stock " + str(st_item.ti) + " Gains $" + str(st_item.gain) + " - " + str(percent) + "%")

def find_minimum(st_item):
    global eligble
    # Pull the stock name
    stock_name = yf.Ticker(st_item)

    # Pick the dates
    today = dt.date.today()
    first_end = today - dt.timedelta(3*30)  # 3 months ago
    start_date = first_end - dt.timedelta(3*30) # 6 months ago
    print(st_item)

    # Pull stock data starting from 6 months ago ending 3 months ago
    current_stock = stock_name.history(start=start_date, end=first_end, interval="1d")
    lowest = 84593485903485093459348509345809345 * 45885
    previous = 0

    # Find if the 3 month in price is the lowest price
    while first_end != today:
        # print(current_stock)
        for j in current_stock['Close']:
            if j < lowest:
                lowest = j
            previous = j
        first_end += dt.timedelta(1)
        start_date += dt.timedelta(1)

    # The most recent price (as of 3 months ago) is the lowest price in the last 3 months    
    if lowest == previous:
        print("Stock name " + str(st_item) + " end date " + str(first_end))
        eligible.append(Stock(previous, st_item, 0))

    # print(hist)

def run_days():
    print("Running days simulation...")

    # Decide which database to start out with
    # Russell 2000, S&P 500, DOW
    stocks = csvreader.identifyList()
    print(stocks)

    # Find the minimum price for each value in the list
    for item in stocks:
        find_minimum(item)

    # Find the gains for each value in the list
    for i in eligible:
        find_gains(i)