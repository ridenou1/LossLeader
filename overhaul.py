# Used to store data
import sqlite3 as sl
# Used to fetch dates
from datetime import datetime, timedelta
# Used to fetch stock data
import yfinance as yf
# Used to read csv files
import csv
import os

DAYSBEHIND = 105
DAYSEND = 100
FLEXIBILITY = 90

def main():
    # print("Enters main")
    conn = database_connection()
    createTables(conn)
    start_date, end_date = dateAllocation()
    identifyBuy(conn, start_date, end_date)

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

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

# identifyBuy decides what stocks to buy
def identifyBuy(conn, start, end):
    demo = csvSearcher('demo.csv', start, end)

def csvSearcher(filename, start, end, current_date):
    stocks = []
    
    # Read CSV full of stocks
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ticker = row['Ticker']
            tick = yf.Ticker(ticker)
            # print(tick.history(period='90d'))
            flex = str(str(FLEXIBILITY) + 'd')
            # print(tick.history(start=start, end=end)["High"])
            # print(min(tick.history(period=flex, end=end)["High"]))
            print(tick.history(start=end, period='1d')["High"])

