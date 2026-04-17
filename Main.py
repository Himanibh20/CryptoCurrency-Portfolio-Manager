import os
from tkinter import *
from tkinter import messagebox, Menu
import requests
import sqlite3

API_KEY = os.getenv("CMC_API_KEY")
if not API_KEY:
    raise ValueError("API Key not found. Please set CMC_API_KEY environment variable.")

pyCrypto = Tk()
pyCrypto.title("My Crypto Portfolio")
for i in range(8):
    pyCrypto.grid_columnconfigure(i, weight=1, uniform="group1")

# pyCrypto.iconbitmap('bitcoin.ico')  # uncomment if you have the icon

con = sqlite3.connect("crypto.db")
cursorobj = con.cursor()
cursorobj.execute(
    "CREATE TABLE IF NOT EXISTS portfolio "
    "(id INTEGER PRIMARY KEY, symbol TEXT, amount_owned REAL, price_per_coin REAL)"
)
con.commit()


# ── Helper: placeholder behaviour ────────────────────────────────────────────
def add_placeholder(entry, placeholder):
    """Grey placeholder text that disappears on focus."""
    entry.insert(0, placeholder)
    entry.config(fg="grey")

    def on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.config(fg="black")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    entry.bind("<FocusIn>",  on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def get_entry(entry, placeholder):
    """Return None if entry still holds placeholder or is empty, else real value."""
    val = entry.get().strip()
    return None if (val == placeholder or val == "") else val


# ── Navigation / menu (called ONCE at startup) ────────────────────────────────
def app_nav():
    def clear_all():
        cursorobj.execute("DELETE FROM portfolio")
        con.commit()
        messagebox.showinfo("Portfolio Message", "Portfolio cleared!")
        my_portfolio()

    def close_app():
        pyCrypto.destroy()

    menu = Menu(pyCrypto)
    file_item = Menu(menu, tearoff=0)
    file_item.add_command(label="Clear Portfolio", command=clear_all)
    file_item.add_command(label="Close App",       command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pyCrypto.config(menu=menu)


# ── Static column headers (called ONCE at startup) ───────────────────────────
def app_header():
    headers = [
        "ID", "Coin Name", "Price", "Coin Owned",
        "Amount Paid", "Current Value", "P/L per Coin", "Total P/L"
    ]
    for col, text in enumerate(headers):
        Label(
            pyCrypto, text=text, bg="#0B0694", fg="white",
            font=("Arial", 11, "bold"), padx=10, pady=10,
            borderwidth=2, relief="groove"
        ).grid(row=0, column=col, sticky="nsew")


# ── Main portfolio view (called on every refresh) ────────────────────────────
def my_portfolio():
    # Clear every widget below the header row
    for widget in pyCrypto.winfo_children():
        info = widget.grid_info()
        if info and int(info["row"]) > 0:
            widget.destroy()

    # ── Fetch live prices ─────────────────────────────────────────────────────
    req_headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accepts": "application/json"
    }
    try:
        api_request = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
            headers=req_headers,
            params={"start": 1, "limit": 300, "convert": "USD"}
        )
        api = api_request.json()
    except Exception as e:
        messagebox.showerror("API Error", str(e))
        return

    price_lookup = {
        item["symbol"]: item["quote"]["USD"]["price"]
        for item in api.get("data", [])
    }

    # ── Load portfolio from DB ────────────────────────────────────────────────
    cursorobj.execute("SELECT * FROM portfolio")
    coins = cursorobj.fetchall()

    total_profit_loss   = 0.0
    total_current_value = 0.0
    total_amount_paid   = 0.0
    coin_row = 1

    def font_color(amount):
        return "green" if amount >= 0 else "red"

    # ── Coin rows ─────────────────────────────────────────────────────────────
    for coin in coins:
        coin_id, symbol, amount_owned, price_per_coin = coin

        if symbol not in price_lookup:
            # Still show the row so user knows the coin exists but price is unavailable
            Label(pyCrypto, text=str(coin_id), borderwidth=1, relief="solid",
                  padx=5, pady=5, anchor="center"
                  ).grid(row=coin_row, column=0, sticky="nsew")
            Label(pyCrypto, text=f"{symbol}  (price N/A)", fg="orange",
                  borderwidth=1, relief="solid", padx=5, pady=5
                  ).grid(row=coin_row, column=1, columnspan=7, sticky="nsew")
            coin_row += 1
            continue

        current_price = price_lookup[symbol]
        total_paid    = amount_owned * price_per_coin
        current_value = amount_owned * current_price
        profit_loss   = current_value - total_paid
        pl_per_coin   = current_price - price_per_coin

        total_profit_loss   += profit_loss
        total_current_value += current_value
        total_amount_paid   += total_paid

        row_data = [
            (0, str(coin_id),             "center", "black"),
            (1, symbol,                   "center", "black"),
            (2, f"${current_price:,.2f}", "e",      "black"),
            (3, str(amount_owned),        "center", "black"),
            (4, f"${total_paid:,.2f}",    "e",      "black"),
            (5, f"${current_value:,.2f}", "e",      "black"),
            (6, f"${pl_per_coin:,.2f}",   "e",      font_color(pl_per_coin)),
            (7, f"${profit_loss:,.2f}",   "e",      font_color(profit_loss)),
        ]
        for col, text, anchor, fg in row_data:
            Label(
                pyCrypto, text=text, fg=fg,
                borderwidth=1, relief="solid",
                padx=5, pady=5, anchor=anchor
            ).grid(row=coin_row, column=col, sticky="nsew")

        coin_row += 1

    # ── Totals row ────────────────────────────────────────────────────────────
    for col in range(8):
        Label(pyCrypto, bg="#E2E8F0", borderwidth=1, relief="solid"
              ).grid(row=coin_row, column=col, sticky="nsew")

    totals = [
        (4, f"${total_amount_paid:,.2f}",   "black"),
        (5, f"${total_current_value:,.2f}", "black"),
        (7, f"${total_profit_loss:,.2f}",   font_color(total_profit_loss)),
    ]
    for col, text, fg in totals:
        Label(
            pyCrypto, text=text, fg=fg,
            font=("Arial", 11, "bold"),
            bg="#E2E8F0", borderwidth=1, relief="solid", anchor="e", padx=5
        ).grid(row=coin_row, column=col, sticky="nsew")

    # Refresh button sits in totals row
    Button(
        pyCrypto, text="🔄 Refresh", bg="#033291", fg="white",
        font=("Arial", 10, "bold"), borderwidth=1, relief="solid",
        command=my_portfolio
    ).grid(row=coin_row, column=0, columnspan=3, sticky="nsew", padx=4, pady=2)

    # ════════════════════════════════════════════════════════════════════════
    # INPUT SECTION  –  LabelFrame per action for clean alignment
    # ════════════════════════════════════════════════════════════════════════
    INPUT_BG = "#F0F4FF"
    ENTRY_W  = 14
    BTN_CFG  = dict(bg="#033291", fg="white", font=("Arial", 10, "bold"),
                    borderwidth=2, relief="groove", padx=8, pady=4, cursor="hand2")

    # ── ADD ───────────────────────────────────────────────────────────────────
    add_frame = LabelFrame(pyCrypto, text=" ➕  Add Coin ",
                           bg=INPUT_BG, font=("Arial", 9, "bold"), padx=10, pady=8)
    add_frame.grid(row=coin_row + 1, column=0, columnspan=8,
                   sticky="ew", padx=12, pady=(10, 4))
    add_frame.grid_columnconfigure((1, 3, 5), weight=1)

    Label(add_frame, text="Symbol",    bg=INPUT_BG, anchor="e", width=9 ).grid(row=0, column=0, padx=(0, 4))
    Label(add_frame, text="Buy Price", bg=INPUT_BG, anchor="e", width=11).grid(row=0, column=2, padx=(14, 4))
    Label(add_frame, text="Amount",    bg=INPUT_BG, anchor="e", width=9 ).grid(row=0, column=4, padx=(14, 4))

    symbol_txt = Entry(add_frame, width=ENTRY_W, borderwidth=2, relief="groove")
    symbol_txt.grid(row=0, column=1, sticky="ew")
    add_placeholder(symbol_txt, "e.g. BTC")

    price_txt = Entry(add_frame, width=ENTRY_W, borderwidth=2, relief="groove")
    price_txt.grid(row=0, column=3, sticky="ew")
    add_placeholder(price_txt, "e.g. 30000")

    amount_txt = Entry(add_frame, width=ENTRY_W, borderwidth=2, relief="groove")
    amount_txt.grid(row=0, column=5, sticky="ew")
    add_placeholder(amount_txt, "e.g. 0.5")

    def insert_coin():
        sym = get_entry(symbol_txt, "e.g. BTC")
        prc = get_entry(price_txt,  "e.g. 30000")
        amt = get_entry(amount_txt, "e.g. 0.5")
        if not sym:
            messagebox.showerror("Error", "Please enter a coin symbol"); return
        try:
            price_val  = float(prc)
            amount_val = float(amt)
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Price and Amount must be numbers"); return
        cursorobj.execute(
            "INSERT INTO portfolio (symbol, amount_owned, price_per_coin) VALUES (?, ?, ?)",
            (sym.upper(), amount_val, price_val)
        )
        con.commit()
        messagebox.showinfo("Portfolio", f"{sym.upper()} added to portfolio!")
        my_portfolio()

    Button(add_frame, text="Add Coin", command=insert_coin, **BTN_CFG
           ).grid(row=0, column=6, padx=(18, 0))

    # ── UPDATE ────────────────────────────────────────────────────────────────
    upd_frame = LabelFrame(pyCrypto, text=" ✏️  Update Coin ",
                           bg=INPUT_BG, font=("Arial", 9, "bold"), padx=10, pady=8)
    upd_frame.grid(row=coin_row + 2, column=0, columnspan=8,
                   sticky="ew", padx=12, pady=4)
    upd_frame.grid_columnconfigure((1, 3, 5, 7), weight=1)

    Label(upd_frame, text="ID",        bg=INPUT_BG, anchor="e", width=4 ).grid(row=0, column=0, padx=(0, 4))
    Label(upd_frame, text="Symbol",    bg=INPUT_BG, anchor="e", width=9 ).grid(row=0, column=2, padx=(14, 4))
    Label(upd_frame, text="Buy Price", bg=INPUT_BG, anchor="e", width=11).grid(row=0, column=4, padx=(14, 4))
    Label(upd_frame, text="Amount",    bg=INPUT_BG, anchor="e", width=9 ).grid(row=0, column=6, padx=(14, 4))

    portid_update = Entry(upd_frame, width=6,       borderwidth=2, relief="groove")
    portid_update.grid(row=0, column=1, sticky="ew")
    add_placeholder(portid_update, "ID")

    symbol_update = Entry(upd_frame, width=ENTRY_W, borderwidth=2, relief="groove")
    symbol_update.grid(row=0, column=3, sticky="ew")
    add_placeholder(symbol_update, "e.g. BTC")

    price_update  = Entry(upd_frame, width=ENTRY_W, borderwidth=2, relief="groove")
    price_update.grid(row=0, column=5, sticky="ew")
    add_placeholder(price_update, "e.g. 30000")

    amount_update = Entry(upd_frame, width=ENTRY_W, borderwidth=2, relief="groove")
    amount_update.grid(row=0, column=7, sticky="ew")
    add_placeholder(amount_update, "e.g. 0.5")

    def update_coin():
        pid = get_entry(portid_update, "ID")
        sym = get_entry(symbol_update, "e.g. BTC")
        prc = get_entry(price_update,  "e.g. 30000")
        amt = get_entry(amount_update, "e.g. 0.5")
        if not pid:
            messagebox.showerror("Error", "Please enter the coin ID"); return
        try:
            price_val  = float(prc)
            amount_val = float(amt)
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Price and Amount must be numbers"); return
        cursorobj.execute(
            "UPDATE portfolio SET symbol=?, amount_owned=?, price_per_coin=? WHERE id=?",
            (sym.upper(), amount_val, price_val, pid)
        )
        con.commit()
        messagebox.showinfo("Portfolio", f"Coin ID {pid} updated!")
        my_portfolio()

    Button(upd_frame, text="Update Coin", command=update_coin, **BTN_CFG
           ).grid(row=0, column=8, padx=(18, 0))

    # ── DELETE ────────────────────────────────────────────────────────────────
    del_frame = LabelFrame(pyCrypto, text=" 🗑️  Delete Coin ",
                           bg=INPUT_BG, font=("Arial", 9, "bold"), padx=10, pady=8)
    del_frame.grid(row=coin_row + 3, column=0, columnspan=8,
                   sticky="ew", padx=12, pady=(4, 14))
    del_frame.grid_columnconfigure(1, weight=0)

    Label(del_frame, text="Coin ID", bg=INPUT_BG, anchor="e", width=8
          ).grid(row=0, column=0, padx=(0, 4))

    portid_delete = Entry(del_frame, width=12, borderwidth=2, relief="groove")
    portid_delete.grid(row=0, column=1, sticky="w")
    add_placeholder(portid_delete, "Enter coin ID")

    def delete_coin():
        pid = get_entry(portid_delete, "Enter coin ID")
        if not pid:
            messagebox.showerror("Error", "Please enter the coin ID"); return
        cursorobj.execute("DELETE FROM portfolio WHERE id=?", (pid,))
        con.commit()
        messagebox.showinfo("Portfolio", f"Coin ID {pid} deleted!")
        my_portfolio()

    Button(del_frame, text="Delete Coin", command=delete_coin, **BTN_CFG
           ).grid(row=0, column=2, padx=(18, 0))


# ── Bootstrap ─────────────────────────────────────────────────────────────────
app_nav()
app_header()
my_portfolio()

pyCrypto.mainloop()

print("Program Completed Successfully")
cursorobj.close()
con.close()