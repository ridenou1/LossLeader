import sys
import os
import yfinance as yf
import datetime as dt
import sqlite3 as sl
# import threading
import multiprocessing
import concurrent.futures

import csvreader

class Stock:
    def __init__(self, pp, ti):
        self.pp = pp
        self.ti = ti

eligible = []

def find_gains(st_item):
    today = dt.date.today()
    start = today - dt.timedelta(3*30)
    stock_name = yf.Ticker(st_item.ti)
    current_stock = stock_name.history(start=start, end=today, interval="1d")
    # previous = 0
    count = 0
    original = 0
    for j in current_stock['Close']:
        if count == 0:
            original = j
        # previous = j
        count += 1
    print("Stock " + str(st_item.ti) + " Gains " + str(st_item.pp - original))

def find_minimum(st_item):
    global eligble
    stock_name = yf.Ticker(st_item)
    today = dt.date.today()
    first_end = today - dt.timedelta(3*30)
    start_date = first_end - dt.timedelta(3*30)
    print(st_item)
    current_stock = stock_name.history(start=start_date, end=first_end, interval="1d")
    lowest = 84593485903485093459348509345809345 * 45885
    previous = 0
    while first_end != today:
        # print(first_end)
        for j in current_stock['Close']:
            if j < lowest:
                print("Lowest sets")
                lowest = j
            previous = j
        if lowest == previous:
            print("Stock name " + str(st_item) + " end date " + str(first_end))
            eligible.append(Stock(previous, st_item))
        first_end += dt.timedelta(1)
        start_date += dt.timedelta(1)

    # print(hist)

def run_days():
    print("Running days simulation...")
    # Decide which database to start out with
    # Russell 2000, S&P 500, DOW

    stocks = csvreader.identifyList()
    print(stocks)

    for item in stocks:
        find_minimum(item)

    # Multithreading Experimentation
    # executor = concurrent.futures.ProcessPoolExecutor(10)
    # futures = [executor.submit(find_minimum, item) for item in stocks]
    # concurrent.futures.wait(futures)
    
    # print(eligible)
    for i in eligible:
        find_gains(i)