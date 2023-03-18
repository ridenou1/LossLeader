import yfinance as yf
# import pendulum
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import pandas as pd
import os
import sqlite3 as sl

import stockbuyer
import stockfinder

# Very incomplete simulator

def simulator():
    # simulator_csv(90, 0, 3000, [])
    simulator_sqlite(5, 0, 3000, [])

def simulator_csv(DAYSBEHIND, DAYEND, CASH, OWNED):
    # Clears any old data
    # if os.path.isfile('./owned.csv'):
    #     os.remove('./owned.csv')

    # Setup
    # DAYSBEHIND = 90 # Adapt to pass to stockbuyer
    # DAYEND = 0      # Adapt to pass to stockbuyer   
    # CASH = 3000
    # OWNED = []

    # Pulls the viable stocks for the day
    viable = stockfinder.identifyStocks()

    # Updates the amount of time focused on in the simulator
    DAYSBEHIND = DAYSBEHIND + 220
    DAYEND = DAYEND + 220
    i = 220
    while i > 0:
        viable = stockfinder.identifyStocks()
        for tickdata in viable:
            if CASH >= tickdata[1]:
               if not os.path.isfile('./owned.csv'):
                   with open('./owned.csv', 'w', newline='') as createOwned:
                       writer = csv.writer(createOwned)
                       writer.writerow(["Ticker", "Cost", "Amount"])
                       print("i[0] - " + str(tickdata[0]) + "\n" + "i[1] - " + str(tickdata[1]) + "\n")
                    #    writer.writerow(str(i[0]) + "," + str(i[1]) + "," + str(1) + "\n")
                       writer.writerow([str(tickdata[0]), str(tickdata[1]), str(1)])
               else:
                   # Need to write search function for existing shares
                #    with open('./owned.csv', 'r', newline='') as ownedFile:
                #        writer = csv.writer(ownedFile)       # No
                #        writer.writerow([i[0], "Shares"])    # No
                    with open('./owned.csv', newline='') as csvfile:
                        csvreader = csv.reader(csvfile, delimiter=',')
                        # Printing for debug
                        for row in csvreader:
                            if row[0] == tickdata:
                                print("Modifying" + row[1])
                                this_amount = row[2]
                                last_price = row[1]
                                new_price = ((last_price * this_amount) + tickdata[1]) / (this_amount + 1)
                                # Outline of what from here:
                                # Find where this stock exists already, remove the line
                                # Add the new line with the added amount
                                # Move this algorithm to stockbuyer.py
                            # else:
                            #     print(row[0])
        DAYSBEHIND = DAYSBEHIND - 1
        DAYEND = DAYEND - 1
        i = i - 1
    stockfinder.currentValue()
    return

# def database_test():
#     con = sl.connect('lossleader.db')
#     with con:
#         print("Database connected successfully")
#         con.execute("DROP TABLE IF EXISTS PORTFOLIO")
#         con.execute("""CREATE TABLE PORTFOLIO(tick TEXT, price REAL, quantity INTEGER);""")

#         si = 'INSERT INTO PORTFOLIO (tick, price, quantity) values(?, ?, ?)'
#         data = [('APPL', 32.22, 4), ('NVDA', 333.32, 89), ('GME', 2.14, 3)]
#         con.executemany(si, data)
#         table = con.execute("SELECT * FROM PORTFOLIO WHERE tick=\'GME\'")
#         for row in table:
#             print(row[2])
#     con.close()

# def sql_buy(con, tickdata, price):
#     current_tick = tickdata[0]
#     tick_table = con.execute("SELECT * FROM PORTFOLIO WHERE TICK=\'" + str(current_tick) + "\'")
    
#     # This will either run once or nonce, depending on if the tick exists in the table
#     found = 0
#     for row in tick_table:
#         # print("Enters despite nothing, row content " + str(row))
#         found = 1
#         exist_price = row[1]
#         exist_count = row[2]
#         new_count = exist_count + 1
#         new_price = ((exist_price * exist_count) + price) / new_count
#         con.execute("UPDATE PORTFOLIO SET price=" + str(new_price) + ", quantity=" + str(new_count) + " where tick=\'" + current_tick + "\';")
        
#     if found == 0:
#         si = 'INSERT INTO PORTFOLIO (tick, price, quantity) values(?, ?, ?)'
#         data = [(current_tick, price, 1)]
#         con.executemany(si, data)
#     return



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
    # print("\n\nOutput check:")
    # table = con.execute("SELECT * FROM PORTFOLIO")
    # for row in table:
    #     print(row)
    con.commit()


if __name__ == "__main__":
    simulator()