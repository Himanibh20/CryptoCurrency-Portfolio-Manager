"""
CryptoCurrency Portfolio Manager - Main GUI Application
Desktop application for managing cryptocurrency portfolios using Tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import PortfolioDB
from api import CoinMarketCapAPI
import threading
from typing import Dict


class CryptoPortfolioApp:
    """Main application class for the Cryptocurrency Portfolio Manager."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("CryptoCurrency Portfolio Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Initialize database and API
        self.db = PortfolioDB()
        self.api = CoinMarketCapAPI()  # Using demo mode without API key
        
        # Store current prices
        self.current_prices: Dict = {}
        
        # Flag to track if application is running
        self.is_running = True
        
        # Setup UI
        self.setup_ui()
        
        # Load initial data
        self.refresh_portfolio()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg="#2C3E50", height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🪙 CryptoCurrency Portfolio Manager",
            font=("Arial", 18, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#ECF0F1")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control Panel
        control_frame = tk.Frame(main_container, bg="#ECF0F1")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        btn_style = {"font": ("Arial", 10), "width": 15, "height": 2}
        
        self.add_btn = tk.Button(
            control_frame,
            text="➕ Add Coin",
            command=self.add_coin_dialog,
            bg="#27AE60",
            fg="white",
            **btn_style
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh Prices",
            command=self.refresh_portfolio,
            bg="#3498DB",
            fg="white",
            **btn_style
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = tk.Button(
            control_frame,
            text="🗑️ Remove Coin",
            command=self.delete_coin,
            bg="#E74C3C",
            fg="white",
            **btn_style
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Portfolio Summary
        summary_frame = tk.Frame(main_container, bg="#34495E", relief=tk.RAISED, borderwidth=2)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.total_value_label = tk.Label(
            summary_frame,
            text="Total Portfolio Value: $0.00",
            font=("Arial", 14, "bold"),
            bg="#34495E",
            fg="white"
        )
        self.total_value_label.pack(pady=10)
        
        # Portfolio Table
        table_frame = tk.Frame(main_container, bg="#ECF0F1")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ("Symbol", "Name", "Amount", "Price", "Value", "Change 24h")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        column_widths = {"Symbol": 80, "Name": 150, "Amount": 100, "Price": 120, "Value": 120, "Change 24h": 100}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Style for treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ECF0F1", foreground="black", rowheight=25, fieldbackground="#ECF0F1")
        style.map("Treeview", background=[("selected", "#3498DB")])
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#34495E", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready | Using demo mode (no API key)",
            font=("Arial", 9),
            bg="#34495E",
            fg="white",
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10)
    
    def add_coin_dialog(self):
        """Show dialog to add a new coin to the portfolio."""
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Cryptocurrency")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Content frame
        content = tk.Frame(dialog, bg="#ECF0F1")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Symbol
        tk.Label(content, text="Coin Symbol (e.g., BTC):", bg="#ECF0F1", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        symbol_entry = tk.Entry(content, font=("Arial", 12))
        symbol_entry.pack(fill=tk.X, pady=(0, 15))
        symbol_entry.focus()
        
        # Name
        tk.Label(content, text="Coin Name (e.g., Bitcoin):", bg="#ECF0F1", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        name_entry = tk.Entry(content, font=("Arial", 12))
        name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Amount
        tk.Label(content, text="Amount:", bg="#ECF0F1", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        amount_entry = tk.Entry(content, font=("Arial", 12))
        amount_entry.pack(fill=tk.X, pady=(0, 20))
        
        def submit():
            symbol = symbol_entry.get().strip().upper()
            name = name_entry.get().strip()
            amount_str = amount_entry.get().strip()
            
            if not symbol or not name or not amount_str:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showwarning("Input Error", "Amount must be greater than 0.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Amount must be a valid number.")
                return
            
            if self.db.add_coin(symbol, name, amount):
                messagebox.showinfo("Success", f"Added {amount} {symbol} to portfolio!")
                dialog.destroy()
                self.refresh_portfolio()
            else:
                messagebox.showerror("Error", "Failed to add coin to database.")
        
        # Buttons
        button_frame = tk.Frame(content, bg="#ECF0F1")
        button_frame.pack(fill=tk.X)
        
        tk.Button(
            button_frame,
            text="Add",
            command=submit,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10),
            width=10
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#95A5A6",
            fg="white",
            font=("Arial", 10),
            width=10
        ).pack(side=tk.LEFT)
        
        # Bind Enter key to submit
        dialog.bind('<Return>', lambda e: submit())
    
    def delete_coin(self):
        """Delete selected coin from the portfolio."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a coin to remove.")
            return
        
        item = self.tree.item(selected[0])
        coin_id = item['tags'][0] if item['tags'] else None
        coin_symbol = item['values'][0]
        
        if coin_id is None:
            messagebox.showerror("Error", "Could not identify coin to delete.")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove {coin_symbol} from your portfolio?"
        )
        
        if confirm:
            if self.db.delete_coin(coin_id):
                messagebox.showinfo("Success", f"Removed {coin_symbol} from portfolio.")
                self.refresh_portfolio()
            else:
                messagebox.showerror("Error", "Failed to remove coin from database.")
    
    def refresh_portfolio(self):
        """Refresh the portfolio display with current prices."""
        self.status_label.config(text="Refreshing prices...")
        self.root.update()
        
        # Get portfolio from database
        portfolio = self.db.get_all_coins()
        
        if portfolio:
            # Get unique symbols
            symbols = list(set([coin[1] for coin in portfolio]))
            
            # Fetch prices (in a thread to avoid UI freezing)
            def fetch_prices():
                self.current_prices = self.api.get_latest_prices(symbols)
                if self.is_running:
                    try:
                        self.root.after(0, self.update_display, portfolio)
                    except tk.TclError:
                        pass  # Window was destroyed
            
            thread = threading.Thread(target=fetch_prices, daemon=True)
            thread.start()
        else:
            self.update_display([])
    
    def update_display(self, portfolio):
        """Update the treeview with portfolio data."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_value = 0.0
        
        for coin in portfolio:
            coin_id, symbol, name, amount, date_added = coin
            
            price_data = self.current_prices.get(symbol, {})
            price = price_data.get('price', 0.0)
            percent_change = price_data.get('percent_change_24h', 0.0)
            
            value = price * amount
            total_value += value
            
            # Format values
            amount_str = f"{amount:.8g}" if amount < 1 else f"{amount:.6g}"
            price_str = f"${price:,.2f}" if price > 0 else "N/A"
            value_str = f"${value:,.2f}"
            change_str = f"{percent_change:+.2f}%" if percent_change != 0 else "0.00%"
            
            # Insert into treeview
            self.tree.insert(
                "",
                tk.END,
                values=(symbol, name, amount_str, price_str, value_str, change_str),
                tags=(coin_id,)
            )
        
        # Update total value
        self.total_value_label.config(text=f"Total Portfolio Value: ${total_value:,.2f}")
        
        # Update status
        self.status_label.config(text=f"Last updated: {self.get_current_time()} | Portfolio: {len(portfolio)} coins")
    
    def auto_refresh(self):
        """Automatically refresh prices every 60 seconds."""
        if self.is_running:
            self.refresh_portfolio()
            self.root.after(60000, self.auto_refresh)  # 60000 ms = 60 seconds
    
    def get_current_time(self):
        """Get current time as a formatted string."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def on_closing(self):
        """Handle application closing."""
        self.is_running = False
        self.db.close()
        self.root.destroy()


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = CryptoPortfolioApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start auto-refresh after window is fully initialized
    app.auto_refresh()
    
    root.mainloop()


if __name__ == "__main__":
    main()
