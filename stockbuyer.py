import sqlite3 as sl

def sql_buy(con, tickdata, price):
    current_tick = tickdata[0]
    tick_table = con.execute("SELECT * FROM PORTFOLIO WHERE TICK=\'" + str(current_tick) + "\'")
    
    # This will either run once or nonce, depending on if the tick exists in the table
    found = 0
    for row in tick_table:
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

def sql_sell(con):
    print("\rIncorporate sell algorithm later...", end="\r")
    current_table = con.execute("SELECT * FROM CURRENT")
    portfolio_table = con.execute("SELECT * FROM PORTFOLIO")
    for row in current_table:
        print(row[1])
    print("\n Finish current, start portfolio")
    for row in portfolio_table:
        print(row)
    print("\n Finish portfolio")
    max_differential = 0
    max_quantity = 0
    max_stock = "AAAAAAA"
    for a in current_table:
        for o in portfolio_table:
            if a[0] == o[0]:
                differential = o[1] / a[1]
                if differential > max_differential:
                    max_differential = differential
                    max_quantity = o[2]
                    max_stock = a[0]

    print("Max diff " + str(max_differential))
                
    return 0

def fetch_current(con, tickdata):
    con.execute()
    
if __name__ == "__main__":
    con = sl.connect('lossleader.db')
    # sql_sell(con)
    # fetch_current(con)
    # con.commit()