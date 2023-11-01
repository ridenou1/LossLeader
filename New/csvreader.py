import csv

def identifyList():
    stocks = []
    filename = 'fortune.csv'
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ticker = row['Ticker']
            stocks.append(ticker)

    return stocks
