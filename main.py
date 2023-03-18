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

# try:
#     from datetime import datetime, timedelta
# except ImportError:
#     os.system("python3 -m pip install --upgrade datetime")

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
    

if __name__ == "__main__":
    # Runs simulator by default first
    simulator.simulator()
    # main()