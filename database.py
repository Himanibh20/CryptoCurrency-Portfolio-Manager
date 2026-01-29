"""
Database module for managing cryptocurrency portfolio data using SQLite3.
"""
import sqlite3
from typing import List, Tuple, Optional


class PortfolioDB:
    """Handles all database operations for the cryptocurrency portfolio."""
    
    def __init__(self, db_name: str = "crypto_portfolio.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_symbol TEXT NOT NULL,
                coin_name TEXT NOT NULL,
                amount REAL NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_coin(self, coin_symbol: str, coin_name: str, amount: float) -> bool:
        """
        Add a coin to the portfolio.
        
        Args:
            coin_symbol: Symbol of the cryptocurrency (e.g., 'BTC')
            coin_name: Full name of the cryptocurrency (e.g., 'Bitcoin')
            amount: Amount of coins owned
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute('''
                INSERT INTO portfolio (coin_symbol, coin_name, amount)
                VALUES (?, ?, ?)
            ''', (coin_symbol.upper(), coin_name, amount))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding coin: {e}")
            return False
    
    def get_all_coins(self) -> List[Tuple]:
        """
        Retrieve all coins from the portfolio.
        
        Returns:
            List of tuples containing (id, coin_symbol, coin_name, amount, date_added)
        """
        try:
            self.cursor.execute('SELECT * FROM portfolio ORDER BY date_added DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving coins: {e}")
            return []
    
    def update_coin_amount(self, coin_id: int, new_amount: float) -> bool:
        """
        Update the amount of a specific coin.
        
        Args:
            coin_id: Database ID of the coin
            new_amount: New amount of coins
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute('''
                UPDATE portfolio SET amount = ? WHERE id = ?
            ''', (new_amount, coin_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating coin: {e}")
            return False
    
    def delete_coin(self, coin_id: int) -> bool:
        """
        Delete a coin from the portfolio.
        
        Args:
            coin_id: Database ID of the coin to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute('DELETE FROM portfolio WHERE id = ?', (coin_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting coin: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
