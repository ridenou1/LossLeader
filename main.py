import os

try:
    import yfinance as yf
except ImportError:
    os.system("python3 -m pip install --upgrade yfinance")

try:
    import matplotlib.pyplot as plt
except ImportError:
    os.system("python3 -m pip install --upgrade matplotlib")

try:
    import pendulum
except ImportError:
    os.system("python3 -m pip install --upgrade pendulum")

try:
    from datetime import datetime, timedelta
except ImportError:
    os.system("python3 -m pip install --upgrade datetime")

try:
    import csv
except ImportError:
    os.system("python3 -m pip install --upgrade csv")

try:
    import pandas as pd
except ImportError:
    os.system("python3 -m pip install --upgrade pandas")

import simulator
import stockbuyer
import stockfinder

def main():
    print("Enters main")
    # Main will eventually hold calls to algorithm code

if __name__ == "__main__":
    # Runs simulator by default first
    simulator.simulator()
    main()