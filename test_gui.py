"""
Test script to verify GUI functionality and take screenshots.
"""
import tkinter as tk
from main import CryptoPortfolioApp
import time
import sys

def test_gui():
    """Test the GUI application."""
    print("Initializing GUI application...")
    root = tk.Tk()
    app = CryptoPortfolioApp(root)
    
    print("✓ GUI initialized successfully")
    
    # Add some test data
    print("Adding test cryptocurrencies...")
    app.db.add_coin("BTC", "Bitcoin", 0.5)
    app.db.add_coin("ETH", "Ethereum", 2.0)
    app.db.add_coin("ADA", "Cardano", 1000.0)
    print("✓ Test data added")
    
    # Refresh to display the data
    print("Refreshing portfolio display...")
    app.refresh_portfolio()
    root.update()
    time.sleep(1)  # Wait for prices to load
    root.update()
    print("✓ Portfolio refreshed")
    
    # Try to take a screenshot if PIL is available
    try:
        import PIL.ImageGrab as ImageGrab
        # Update the display
        root.update()
        time.sleep(0.5)
        
        # Get window geometry
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        
        # Take screenshot
        screenshot = ImageGrab.grab(bbox=(x, y, x+w, y+h))
        screenshot.save("portfolio_screenshot.png")
        print("✓ Screenshot saved as portfolio_screenshot.png")
    except ImportError:
        print("ℹ PIL not available, skipping screenshot")
    except Exception as e:
        print(f"ℹ Screenshot failed: {e}")
    
    # Clean up
    print("Cleaning up...")
    app.db.close()
    root.quit()
    root.destroy()
    
    print("\n" + "="*50)
    print("GUI test completed successfully! ✓")
    print("="*50)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(test_gui())
    except Exception as e:
        print(f"Error during GUI test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
