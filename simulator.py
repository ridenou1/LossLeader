import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import os
import sqlite3 as sl

import stockbuyer
import stockfinder

# Very incomplete simulator

def simulator():
    simulator_sqlite(5, 0, 3000, [])

def simulator_sqlite(DAYSBEHIND, DAYEND, CASH, OWNED):
    DAYSBEHIND = DAYSBEHIND + 220
    DAYEND = DAYEND + 220
    con = sl.connect('lossleader.db')
    with con: 
        print("Database connected successfully.")
        con.execute("DROP TABLE IF EXISTS PORTFOLIO")
        con.execute("""CREATE TABLE PORTFOLIO(tick TEXT, price REAL, quantity INTEGER);""")
    i = DAYSBEHIND
    while i > DAYEND:
        viable = stockfinder.identifyStocks()
        for tickdata in viable:
            price = tickdata[1]
            if CASH >= price:
                stockbuyer.sql_buy(con, tickdata, price)
                CASH = CASH - price
            else:
                # Incomplete
                stockbuyer.sql_sell()     
        i = i - 1
    con.commit()


if __name__ == "__main__":
    simulator()