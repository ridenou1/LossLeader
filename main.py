import yfinance as yf
import pendulum
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

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