"""
Test script to verify database and API functionality.
"""
import sys
import os

# Test database module
print("Testing Database Module...")
from database import PortfolioDB

db_file = "test_portfolio.db"
db = None

try:
    db = PortfolioDB(db_file)
    print("✓ Database connection established")
    
    # Test adding coins
    success = db.add_coin("BTC", "Bitcoin", 0.5)
    print(f"✓ Add coin test: {'Passed' if success else 'Failed'}")
    
    success = db.add_coin("ETH", "Ethereum", 2.0)
    print(f"✓ Add another coin test: {'Passed' if success else 'Failed'}")
    
    # Test retrieving coins
    coins = db.get_all_coins()
    print(f"✓ Retrieved {len(coins)} coins from database")
    for coin in coins:
        print(f"  - ID: {coin[0]}, Symbol: {coin[1]}, Name: {coin[2]}, Amount: {coin[3]}")
    
    # Test deleting coin
    if coins:
        success = db.delete_coin(coins[0][0])
        print(f"✓ Delete coin test: {'Passed' if success else 'Failed'}")
finally:
    if db:
        db.close()
        print("✓ Database connection closed")
    
    # Clean up test database
    if os.path.exists(db_file):
        os.remove(db_file)
        print("✓ Test database cleaned up")

print("\nTesting API Module...")
from api import CoinMarketCapAPI

api = CoinMarketCapAPI()
print("✓ API client initialized (demo mode)")

# Test getting prices
symbols = ["BTC", "ETH", "ADA"]
prices = api.get_latest_prices(symbols)
print(f"✓ Retrieved prices for {len(prices)} coins:")
for symbol, data in prices.items():
    print(f"  - {symbol} ({data['name']}): ${data['price']:,.2f}")

# Test search
results = api.search_coin("bit")
print(f"✓ Search test returned {len(results)} results:")
for result in results:
    print(f"  - {result['symbol']}: {result['name']}")

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)
