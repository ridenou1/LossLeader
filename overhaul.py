# Used to store data
import sqlite3 as sl
# Used to fetch dates
from datetime import datetime, timedelta
# Used to fetch stock data
import yfinance as yf
# Used to read csv files
import csv
# yfinance dependency
import pandas as pd
import os

DAYSBEHIND = 105            # How many days ago to start the simulation
DAYSEND = 50                # How many days ago to end the simulation
FLEXIBILITY = 90            # How many days to look through for buying purposes
VARIANCETHRESHOLD = 50      # Allowed variability between high costs in percent
MAXCASH = 5000              # Starting cash for the simulation

def main():
    # print("Enters main")
    conn = database_connection()
    createTables(conn)
    start_date, end_date = dateAllocation()
    simulator(conn, end_date)


# Connects to sqlite database
def database_connection():
    # Connect to sqlite tables
    database = 'lossleader.db'
    try:
        conn = sl.connect(database)
    except:
        print("Connection to database " + database + " failed.")
    with conn:
        print("Database connected successfully...")
    return conn

# createTable creates/resets the tables data are stores in
def createTables(conn):
    # Owned stock data
    conn.execute("DROP TABLE IF EXISTS PORTFOLIO")
    conn.execute("""CREATE TABLE PORTFOLIO(tick TEXT, price REAL, quantity INTEGER);""")
    # What to sell
    conn.execute("DROP TABLE IF EXISTS CURRENTSELL")
    conn.execute("CREATE TABLE CURRENTSELL(tick TEXT, price REAL);")
    # What is being evaluated
    conn.execute("DROP TABLE IF EXISTS CURRENT")
    conn.execute("""CREATE TABLE CURRENT(tick TEXT, price REAL);""")
    # Save new tables
    conn.commit()
    return

# dateAllocation sets the date window to look through
def dateAllocation():
    start_date = datetime.now() - timedelta(days=DAYSBEHIND)
    end_date = datetime.now() - timedelta(days=DAYSEND)

    # Sets start date to next Monday if falling on weekend
    if start_date.weekday() == 5:
        start_date = start_date + timedelta(days=2)
    elif start_date.weekday() == 6:
        start_date = start_date + timedelta(days=1)
    
    # Sets end date to previous Friday if falling on weekend.
    if end_date.weekday() == 5:
        end_date = end_date - timedelta(days=1)
    elif end_date.weekday() == 6:
        end_date = end_date - timedelta(days=2)

    return start_date, end_date

# simulator runs the simulation
def simulator(conn, end):
    cash = MAXCASH
    dayCount = DAYSBEHIND - DAYSEND
    while dayCount >= 0:
        print("Cash " + str(cash) + " Days left - " + str(dayCount))
        if (end - timedelta(days=dayCount)).weekday() > 4:
            # print("Weekend, skipping")
            dayCount = dayCount - 1
            continue
        # print("Weekday")
        viable = csvSearcher('demo.csv', end, dayCount)
        conn.execute("DROP TABLE IF EXISTS CURRENT")
        conn.execute("""CREATE TABLE CURRENT(tick TEXT, price REAL);""")
        if len(viable) != 0:
            # print(str(viable))
            si = 'INSERT INTO CURRENT (tick, price) values(?, ?)'
            conn.executemany(si, viable)
            conn.commit()
            cash = buyProcess(conn, cash, dateForm(end - timedelta(days=dayCount)))
        dayCount = dayCount - 1

def buyProcess(conn, cash, currentDate):
    tickTable = conn.execute('SELECT * FROM CURRENT')
    for row in tickTable:
        # print("tick - " + row[0])
        if cash < row[1]:
            # Sell something
            if MAXCASH < row[1]:
                continue
            else:
                cash = sellSteps(conn, row, cash, currentDate)
                cash = buySteps(conn, row, cash)
        else:
            cash = buySteps(conn, row, cash) 
    return cash

def sellSteps(conn, row, cash, currentDate):
    high = fetchCurrentHigh(row, currentDate)

def fetchCurrentHigh(row, currentDate):
    ticker = row[0]
    tick = yf.Ticker(ticker)
    tickHist = tick.history(start=currentDate, end=currentDate)
    print(str(tickHist["High"]))
           
def buySteps(conn, row, cash):
    portTable = conn.execute('SELECT * FROM PORTFOLIO WHERE TICK=\'' + str(row[0]) + "\'")
    found = 0
    print(str(row))
    for owrow in portTable:
        found = 1
        exist_price = owrow[1]
        exist_count = owrow[2]
        new_count = exist_count + 1
        new_price = ((exist_price * exist_count) + row[1]) / new_count
        conn.execute("UPDATE PORTFOLIO SET price=" + str(new_price) + ", quantity=" + str(new_count) + " where tick=\'" + row[0] + "\';")
        print("Cash " + str(type(cash)) + " " + str(cash) + " Row " + str(type(row[1])))
        cash = cash - row[1]
    if found == 0:
        si = 'INSERT INTO PORTFOLIO (tick, price, quantity) values(?, ?, ?)'
        data = [(row[0], row[1], 1)]
        conn.executemany(si, data)
        cash = cash - row[1]
    return cash

def dateForm(date):
    return date.strftime('%Y-%m-%d')

def percentage(costA, costB):
    division = abs(costA / costB)
    thres = VARIANCETHRESHOLD / 100
    lThres = 1 - thres
    hThres = 1 + thres
    if lThres <= division <= hThres:
        # print("Passed: minHigh - " + str(costA) + " mostRecent - " + str(costB) + " division - " + str(division) + " thres " + str(lThres) + "/" + str(hThres))
        return True
    else:
        # print("Failed: minHigh - " + str(costA) + " mostRecent - " + str(costB) + " division - " + str(division) + " thres " + str(lThres) + "/" + str(hThres))
        return False
    

def csvSearcher(filename, date, dateOffset):
    viable = []
    
    # Read CSV full of stocks
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Finding the data for a particular tick
            ticker = row['Ticker']
            print("\rEvaluating " + str(filename) + ", ticker " + str(ticker) + "...", end="\r")
            tick = yf.Ticker(ticker)
            tickHist = tick.history(start=dateForm(date - timedelta(days=(FLEXIBILITY + dateOffset))), end=dateForm(date - timedelta(days=dateOffset)))["High"]
           
            # Finding the lowest high value in the range of FLEXIBILITY up until that day
            minHigh = min(tickHist)

            # Finding the high value on the previous day
            for i in range(0, tickHist.size):
                if i == tickHist.size-1:
                    mostRecent = tickHist[i]

            # Is the high value on the previous day within X percent of the lowest value?
            if percentage(minHigh, mostRecent):
                # If yes, append to viable
                viable.append([ticker, minHigh])

    return viable

