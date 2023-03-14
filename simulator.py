import yfinance as yf
import pendulum
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

import stockbuyer
import stockfinder

# Very incomplete simulator

def simulator():
    # Clears any old data
    if os.path.isfile('./owned.csv'):
        os.remove('./owned.csv')

    # Setup
    DAYSBEHIND = 90 # Adapt to pass to stockbuyer
    DAYEND = 0      # Adapt to pass to stockbuyer   
    CASH = 3000
    OWNED = []

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

if __name__ == "__main__":
    simulator()