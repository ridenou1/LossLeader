# Should eventually hold content currently in simulator

# import yfinance as yf
# import pendulum
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
# import csv
# import pandas as pd
# import os
import sqlite3 as sl

def sql_buy(con, tickdata, price):
    current_tick = tickdata[0]
    tick_table = con.execute("SELECT * FROM PORTFOLIO WHERE TICK=\'" + str(current_tick) + "\'")
    
    # This will either run once or nonce, depending on if the tick exists in the table
    found = 0
    for row in tick_table:
        # print("Enters despite nothing, row content " + str(row))
        found = 1
        exist_price = row[1]
        exist_count = row[2]
        new_count = exist_count + 1
        new_price = ((exist_price * exist_count) + price) / new_count
        con.execute("UPDATE PORTFOLIO SET price=" + str(new_price) + ", quantity=" + str(new_count) + " where tick=\'" + current_tick + "\';")
        
    if found == 0:
        si = 'INSERT INTO PORTFOLIO (tick, price, quantity) values(?, ?, ?)'
        data = [(current_tick, price, 1)]
        con.executemany(si, data)
    return

def sql_sell():
    print("\rIncorporate sell algorithm later...", end="\r")