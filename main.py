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
