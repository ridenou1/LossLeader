import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import os
import sqlite3 as sl

import stockbuyer
import stockfinder

# Very incomplete simulator

def simulator(conn):
    simulator_sqlite(5, 0, 3000, [], conn)

def simulator_sqlite(DAYSBEHIND, DAYEND, CASH, OWNED, con):
    DAYSBEHIND = DAYSBEHIND + 220
    DAYEND = DAYEND + 220

    with con: 
        con.execute("DROP TABLE IF EXISTS PORTFOLIO")
        con.execute("""CREATE TABLE PORTFOLIO(tick TEXT, price REAL, quantity INTEGER);""")

    i = DAYSBEHIND
    while i > DAYEND:
        print("Cash " + str(CASH))
        viable = stockfinder.identifyStocks(con)
        for tickdata in viable:
            price = tickdata[1]
            if CASH >= price:
                stockbuyer.sql_buy(con, tickdata, price)
                CASH = CASH - price
            else:
                sold = stockbuyer.sql_sell(con)
                CASH = CASH + sold
        i = i - 1


if __name__ == "__main__":
    simulator()