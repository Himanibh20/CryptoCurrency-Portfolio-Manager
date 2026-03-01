from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3


pyCrypto = Tk()
pyCrypto.title("My Crypto Portfolio")
for i in range(8):
    pyCrypto.grid_columnconfigure(i, weight=1, uniform="group1")
pyCrypto.iconbitmap('bitcoin.ico')

con = sqlite3.connect("crypto.db")
cursorobj = con.cursor()
cursorobj.execute("CREATE TABLE IF NOT EXISTS portfolio (id INTEGER PRIMARY KEY, symbol TEXT, amount_owned REAL, price_per_coin REAL)")
con.commit()

# cursorobj.execute("INSERT INTO portfolio VALUES (1, 'BTC', 2, 1000)")
# con.commit()

# cursorobj.execute("INSERT INTO portfolio VALUES (2, 'ETH', 100, 1)")
# con.commit()

# cursorobj.execute("INSERT INTO portfolio VALUES (3, 'LTC', 75, 20)")
# con.commit()

# cursorobj.execute("INSERT INTO portfolio VALUES (4, 'XMR', 10, 48)")
# con.commit()



def app_nav():
    def clear_all():
        cursorobj.execute("DELETE FROM portfolio")
        con.commit()
        messagebox.showinfo("Portfolio Message", "Portfolio cleared!")
        my_portfolio()  # Refresh the portfolio display after clearing
        
    def close_app():
        pyCrypto.destroy()

    menu = Menu(pyCrypto)
    file_item = Menu(menu)
    file_item.add_command(label="Clear Portfolio", command=clear_all)
    file_item.add_command(label="Close App", command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pyCrypto.config(menu=menu)

def my_portfolio():

    # Clear old rows except header
    for widget in pyCrypto.winfo_children():
        info = widget.grid_info()
        if info and int(info["row"]) > 0:
            widget.destroy()

    headers = {
        "X-CMC_PRO_API_KEY": "fbbca34c24f54db58fe41209e798c227",
        "Accepts": "application/json"
    }

    try:
        api_request = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
            headers=headers,
            params={"start": 1, "limit": 300, "convert": "USD"}
        )
        api = api_request.json()
    except Exception as e:
        print("API Error:", e)
        return

    cursorobj.execute("SELECT * FROM portfolio")
    coins = cursorobj.fetchall()

    price_lookup = {data["symbol"]: data["quote"]["USD"]["price"]
                    for data in api["data"]}

    total_profit_loss = 0
    total_current_value = 0
    total_amount_paid = 0
    coin_row = 1

    def insert_coin():
        symbol = symbol_txt.get().upper()
        try:
            price_per_coin = float(price_txt.get())
            amount_owned = float(amount_txt.get())
        except ValueError:
            print("Invalid input for price or amount")
            return

        cursorobj.execute(
          "INSERT INTO portfolio (symbol, amount_owned, price_per_coin)  VALUES (?, ?, ?)",(symbol, amount_owned, price_per_coin))
        con.commit()
        messagebox.showinfo("Portfolio Message", f"{symbol} added to portfolio!")
        my_portfolio()  # Refresh the portfolio display after inserting new coin
        app_nav()
    
    def update_coin():
        portid = portid_update.get()
        symbol = symbol_update.get().upper()
        try:
         price_per_coin = float(price_update.get())
         amount_owned = float(amount_update.get())
        except ValueError:
         messagebox.showerror("Error", "Invalid price or amount")
         return

        cursorobj.execute("UPDATE portfolio SET symbol=?, amount_owned=?, price_per_coin=? WHERE id=?", (symbol, amount_owned, price_per_coin, portid))
        con.commit()
        messagebox.showinfo("Portfolio Message", f"{symbol} updated in portfolio!")
        my_portfolio()  # Refresh the portfolio display after updating coin
        app_nav()

    def delete_coin():
        cursorobj.execute("DELETE FROM portfolio WHERE id=?", (portid_delete.get(),))
        con.commit()
        messagebox.showinfo("Portfolio Message", "Coin deleted from portfolio!")
        my_portfolio()  # Refresh the portfolio display after deleting coin
        app_nav()

    def font_color(amount):
        return "green" if amount >= 0 else "red"

    for coin in coins:
        coin_id = coin[0]
        symbol = coin[1]
        amount_owned = coin[2]
        price_per_coin = coin[3]

        if symbol not in price_lookup:
            continue

        current_price = price_lookup[symbol]
        total_paid = amount_owned * price_per_coin
        current_value = amount_owned * current_price
        profit_loss = current_value - total_paid
        pl_per_coin = current_price - price_per_coin

        total_profit_loss += profit_loss
        total_current_value += current_value
        total_amount_paid += total_paid

        # Column 0 → ID
        Label(pyCrypto, text=coin_id,
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5).grid(row=coin_row, column=0, sticky="nsew")

        # Column 1 → Coin Name
        Label(pyCrypto, text=symbol,
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5).grid(row=coin_row, column=1, sticky="nsew")

        # Column 2 → Price
        Label(pyCrypto, text=f"$ {current_price:.2f}",
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5,
         anchor="e").grid(row=coin_row, column=2, sticky="nsew")

        # Column 3 → Coin Owned
        Label(pyCrypto, text=amount_owned,
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5,
         anchor="center").grid(row=coin_row, column=3, sticky="nsew")

        # Column 4 → Amount Paid
        Label(pyCrypto, text=f"$ {total_paid:.2f}",
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5,
         anchor="e").grid(row=coin_row, column=4, sticky="nsew")

        # Column 5 → Current Value
        Label(pyCrypto, text=f"$ {current_value:.2f}",
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5,
         anchor="e").grid(row=coin_row, column=5, sticky="nsew")

        # Column 6 → Profit/Loss per Coin
        Label(pyCrypto, text=f"$ {pl_per_coin:.2f}",
         fg=font_color(pl_per_coin),
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5,
         anchor="e").grid(row=coin_row, column=6, sticky="nsew")

        # Column 7 → Total Profit/Loss
        Label(pyCrypto, text=f"$ {profit_loss:.2f}",
         fg=font_color(profit_loss),
         borderwidth=1,
         relief="solid",
         padx=5,
         pady=5,
         anchor="e").grid(row=coin_row, column=7, sticky="nsew")

        coin_row += 1

    #Insert data
    symbol_txt = Entry(pyCrypto,borderwidth=2, relief="groove")
    symbol_txt.grid(row=coin_row + 1, column=1)

    price_txt = Entry(pyCrypto,borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row + 1, column=2) 

    amount_txt = Entry(pyCrypto,borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row + 1, column=3)

    add_coin = Button(pyCrypto, text="Add Coin", bg="#033291", fg="white", command=insert_coin , font="Lato 12", borderwidth=2, relief="groove", padx=5, pady=5)
    add_coin.grid(row=coin_row + 1, column=4, sticky="nsew")

    #Update coin
    portid_update = Entry(pyCrypto,borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row + 2, column=0)

    symbol_update = Entry(pyCrypto,borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row + 2, column=1)

    price_update = Entry(pyCrypto,borderwidth=2, relief="groove")
    price_update.grid(row=coin_row + 2, column=2) 

    amount_update = Entry(pyCrypto,borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row + 2, column=3)

    update_coin_txt = Button(pyCrypto, text="Update Coin", bg="#033291", fg="white", command=update_coin , font="Lato 12", borderwidth=2, relief="groove", padx=5, pady=5)
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky="nsew")

    #Delete coin
    portid_delete = Entry(pyCrypto,borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row + 3, column=0)

    delete_coin_txt = Button(pyCrypto,
    text="Delete Coin",
    bg="#033291",
    fg="white",
    command=delete_coin,
    font="Lato 12",
    borderwidth=2,
    relief="groove",
    padx=5,
    pady=5)
    delete_coin_txt.grid(row=coin_row + 3, column=4, sticky="nsew")

    # Totals Row

    # Total Amount Paid → column 4
    Label(pyCrypto, text=f"$ {total_amount_paid:.2f}",
      font=("Arial", 11, "bold"),
      bg="#E2E8F0",
      borderwidth=1,
      relief="solid",
      anchor="e").grid(row=coin_row, column=4, sticky="nsew")

    # Total Current Value → column 5
    Label(pyCrypto, text=f"$ {total_current_value:.2f}",
      font=("Arial", 11, "bold"),
      bg="#E2E8F0",
      borderwidth=1,
      relief="solid",
      anchor="e").grid(row=coin_row, column=5, sticky="nsew")

    # Total Profit/Loss → column 7
    Label(pyCrypto, text=f"$ {total_profit_loss:.2f}",
      fg=font_color(total_profit_loss),
      font=("Arial", 11, "bold"),
      bg="#E2E8F0",
      borderwidth=1,
      relief="solid",
      anchor="e").grid(row=coin_row, column=7, sticky="nsew")

    # Refresh Button
    Button(pyCrypto,
       text="Refresh",
       bg="#033291",
       fg="white",
       font=("Arial", 10, "bold"),
       borderwidth=1,
       relief="solid",
       command=my_portfolio
       ).grid(row=coin_row + 1,
              column=7,
              sticky="nsew")
def app_header():
    headers = ["ID",
               "Coin Name",
               "Price",
               "Coin Owned",
               "Amount Paid",
               "Current Value",
               "Profit/Loss per Coin",
               "Total Profit/Loss"]

    for col, text in enumerate(headers):
        Label(pyCrypto, text=text, bg="#0B0694", fg="white",
              font="Lato 12 bold", padx=10, pady=10,
              borderwidth=2, relief="groove").grid(row=0, column=col, sticky=N+S+E+W)

app_nav() 
app_header()
my_portfolio()
pyCrypto.mainloop()
print("Program Completed Successfully")
cursorobj.close()
con.close()