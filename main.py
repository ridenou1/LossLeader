<<<<<<< HEAD
import os

# If any potential employer is reading how I'm force installing the modules,
# no you didn't.
try:
    import yfinance as yf
except ImportError:
    os.system("python3 -m pip install --upgrade yfinance")

# try:
#     import matplotlib.pyplot as plt
# except ImportError:
#     os.system("python3 -m pip install --upgrade matplotlib")

# try:
#     import pendulum
# except ImportError:
#     os.system("python3 -m pip install --upgrade pendulum")

try:
    from datetime import datetime, timedelta
except ImportError:
    os.system("python3 -m pip install --upgrade datetime")

# try:
#     import pandas as pd
# except ImportError:
#     os.system("python3 -m pip install --upgrade pandas")

try:
    import sqlite3 as sl
except ImportError:
    os.system("python3 -m pip install --upgrade sqlite3")

import simulator

def main():
    print("Enters main")
    database_test()
    # Main will eventually hold calls to algorithm code

def database_test():
    con = sl.connect('lossleader.db')
    with con:
        print("Database connected successfully")
        con.execute("DROP TABLE IF EXISTS PORTFOLIO")
        con.execute("""CREATE TABLE PORTFOLIO(tick TEXT, price REAL, quantity INTEGER);""")

        si = 'INSERT INTO PORTFOLIO (tick, price, quantity) values(?, ?, ?)'
        data = [('APPL', 32.22, 4), ('NVDA', 333.32, 89), ('GME', 2.14, 3)]
        con.executemany(si, data)
        table = con.execute("SELECT * FROM PORTFOLIO WHERE tick=\'GME\'")
        for row in table:
            print(row[2])
    con.commit()

def database_connection():
    conn = sl.connect('lossleader.db')
    with conn:
        print("Database connected successfully...")
    return conn

if __name__ == "__main__":
    # Runs simulator by default first
    conn = database_connection()
    simulator.simulator(conn)
    conn.commit()
    # main()
=======
#!/usr/bin/env python3

# Import Packages
# Standard
import sys
import os
try:
    import yfinance as yf
except ImportError:
    exit("yfinance not installed")
try:
    from datetime import datetime, timedelta
except ImportError:
    exit("datetime not installed")
try:
    import sqlite3 as sl
except ImportError:
    exit("sqlite3 not installed")
# try:
#     import threading
# except ImportError:
#     exit("threading not installed")

# Custom
import examine

test_mode = 1

def main():
    print("Necessary packages installed successfully.")
    if test_mode == 1:
        simulator()
    else:
        api_connection()

def simulator():
    # Set up the table for testing
    # connection = sl.connect("lossleadersimulator.db")
    # cur = connection.cursor()
    # cur.execute("DROP TABLE IF EXISTS PORTFOLIO")
    # cur.execute("DROP TABLE IF EXISTS DAYS")
    # cur.execute("CREATE TABLE DAYS(tick TEXT, price REAL, quantity INTEGER);")
    examine.run_days()


def api_connection():
    exit("API connection not implemented yet.")

if __name__ == "__main__":
    main()
>>>>>>> revamp
