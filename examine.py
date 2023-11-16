import sys
import os
import yfinance as yf
import datetime as dt
import sqlite3 as sl

import csvreader

class Stock:
    def __init__(self, pp, ti, gain):
        self.pp = pp        # Simulator decision price
        self.ti = ti        # Ticker
        self.gain = gain    # Amount gain/loss

class Bank:
    def __init__(self, balance, held):
        self.balance = balance  # Cash balance to start
        self.held = held        # Stock portfolio

account = Bank(1000000, [])

def find_gains(st_item):
    global account

    # Initialization
    today = dt.date.today()
    start = today - dt.timedelta(3*30)  # 3 months ago
    stock_name = yf.Ticker(st_item.ti)

    current_stock = stock_name.history(start=start, end=today, interval="1d")
    count = 0
    new = 0
    broken = 0

    # Iterate for the current value every 3 months
    for j in current_stock['Close']:
        if count >= 1:
            day_loss = ((j / new) * 100) - 100

            total_loss = ((j / st_item.pp) * 100) - 100

            # If it loses more than 5% in a day, it is time to sell
            if day_loss <= -5:
                print("Day losses on " + st_item.ti + " found to exceed 5%: " + str(round(day_loss, 2)) + "%")
                account.balance += st_item.pp + j
                account.held.remove(st_item)
                print(st_item.ti + " sold! $" + str(round(st_item.pp, 2)) + " -> $" + str(round((j), 2)) + ", Gains: $" + str(round(j - st_item.pp, 2)))
                broken = 1
                break
            
            # If it has lost more then 10% overall, it is time to sell
            if total_loss <= -10:
                print("Total losses on " + st_item.ti + " found to exceed 10%: " + str(round(day_loss, 2)) + "%")
                account.balance += st_item.pp + j
                account.held.remove(st_item)
                print(st_item.ti + " sold to prevent further losses. $" + str(round(st_item.pp, 2)) + " -> $" + str(round((j), 2)) + ", Gains: $" + str(round(j - st_item.pp, 2)))
                broken = 1
                break


        count += 1  
        new = j

    if broken == 0:
        st_item.gain = round(new - st_item.pp, 2)
    percent = round(((new / st_item.pp) * 100) - 100, 2)
    print("Stock " + str(st_item.ti) + " Gains $" + str(st_item.gain) + " - " + str(percent) + "%")



def find_minimum(st_item):
    global account
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
        for j in current_stock['Close']:
            if j < lowest:
                lowest = j
            previous = j
        first_end += dt.timedelta(1)
        start_date += dt.timedelta(1)

    # The most recent price (as of 3 months ago) is the lowest price in the last 3 months    
    if lowest == previous:
        print("Stock name " + str(st_item) + " end date " + str(first_end))
        # eligible.append(Stock(previous, st_item, 0))
        account.held.append(Stock(previous, st_item, 0))
        account.balance = account.balance - previous

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
    for i in account.held:
        find_gains(i)

    for i in account.held:
        value = i.pp + i.gain
        account.balance += value
        account.held.remove(i)

    print("New account balance = $" + str(round(account.balance, 2)))