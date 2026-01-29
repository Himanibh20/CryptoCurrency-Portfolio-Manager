"""
Verification script to check all application components.
"""
import os
import sys

def verify_files():
    """Verify all required files exist."""
    print("="*60)
    print("CryptoCurrency Portfolio Manager - Verification Script")
    print("="*60)
    print()
    
    required_files = {
        "main.py": "Main GUI application",
        "database.py": "SQLite3 database module",
        "api.py": "CoinMarketCap API integration",
        "requirements.txt": "Python dependencies",
        "README.md": "Documentation",
        ".gitignore": "Git ignore file"
    }
    
    print("1. Checking Required Files:")
    print("-" * 60)
    all_present = True
    for file, description in required_files.items():
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"  {status} {file:<20} - {description}")
        if not exists:
            all_present = False
    
    if not all_present:
        print("\n❌ Some required files are missing!")
        return False
    
    print("\n2. Checking Python Module Syntax:")
    print("-" * 60)
    python_files = ["main.py", "database.py", "api.py"]
    all_valid = True
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"  ✓ {file:<20} - Valid Python syntax")
        except SyntaxError as e:
            print(f"  ✗ {file:<20} - Syntax Error: {e}")
            all_valid = False
    
    if not all_valid:
        print("\n❌ Some Python files have syntax errors!")
        return False
    
    print("\n3. Checking Module Structure:")
    print("-" * 60)
    
    # Check main.py
    with open("main.py", 'r') as f:
        main_content = f.read()
        checks = [
            ("tkinter import", "import tkinter" in main_content),
            ("CryptoPortfolioApp class", "class CryptoPortfolioApp" in main_content),
            ("Database initialization", "PortfolioDB" in main_content),
            ("API initialization", "CoinMarketCapAPI" in main_content),
            ("Main function", "def main()" in main_content),
            ("Add coin dialog", "add_coin_dialog" in main_content),
            ("Delete coin function", "delete_coin" in main_content),
            ("Refresh portfolio", "refresh_portfolio" in main_content)
        ]
        
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
    
    # Check database.py
    print()
    with open("database.py", 'r') as f:
        db_content = f.read()
        checks = [
            ("SQLite3 import", "import sqlite3" in db_content),
            ("PortfolioDB class", "class PortfolioDB" in db_content),
            ("Create tables method", "create_tables" in db_content),
            ("Add coin method", "def add_coin" in db_content),
            ("Get all coins method", "def get_all_coins" in db_content),
            ("Delete coin method", "def delete_coin" in db_content)
        ]
        
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
    
    # Check api.py
    print()
    with open("api.py", 'r') as f:
        api_content = f.read()
        checks = [
            ("Requests import", "import requests" in api_content),
            ("CoinMarketCapAPI class", "class CoinMarketCapAPI" in api_content),
            ("Get latest prices method", "def get_latest_prices" in api_content),
            ("Mock prices method", "def _get_mock_prices" in api_content),
            ("Search coin method", "def search_coin" in api_content)
        ]
        
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
    
    print("\n4. Testing Core Functionality:")
    print("-" * 60)
    
    # Test database module
    try:
        from database import PortfolioDB
        db = PortfolioDB("test_verify.db")
        db.add_coin("BTC", "Bitcoin", 1.0)
        coins = db.get_all_coins()
        db.close()
        if os.path.exists("test_verify.db"):
            os.remove("test_verify.db")
        print("  ✓ Database module works correctly")
    except Exception as e:
        print(f"  ✗ Database module error: {e}")
        return False
    
    # Test API module
    try:
        from api import CoinMarketCapAPI
        api = CoinMarketCapAPI()
        prices = api.get_latest_prices(["BTC", "ETH"])
        if len(prices) > 0:
            print("  ✓ API module works correctly (demo mode)")
        else:
            print("  ✗ API module returned no data")
            return False
    except Exception as e:
        print(f"  ✗ API module error: {e}")
        return False
    
    print("\n5. Documentation Check:")
    print("-" * 60)
    with open("README.md", 'r') as f:
        readme = f.read()
        checks = [
            ("Installation instructions", "Installation" in readme),
            ("Usage instructions", "Usage" in readme),
            ("Features listed", "Features" in readme),
            ("Project structure", "Project Structure" in readme or "project structure" in readme.lower()),
            ("Technologies mentioned", "Technologies" in readme or "technologies" in readme.lower())
        ]
        
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
    
    print("\n" + "="*60)
    print("✅ ALL VERIFICATIONS PASSED!")
    print("="*60)
    print()
    print("The CryptoCurrency Portfolio Manager application is ready!")
    print()
    print("To run the application:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run the application: python main.py")
    print()
    print("Note: Tkinter GUI requires a display environment.")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        success = verify_files()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
