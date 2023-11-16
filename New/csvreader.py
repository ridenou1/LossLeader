import csv

def identifyList():
    stocks = []
    # Default is fortune 500
    filename = 'demo.csv'
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ticker = row['Ticker']
            stocks.append(ticker)

    return stocks
