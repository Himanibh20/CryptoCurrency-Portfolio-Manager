# CryptoCurrency Portfolio Manager

A desktop application for managing cryptocurrency portfolios, built with Python and Tkinter. This application uses the CoinMarketCap API for live price tracking and SQLite3 to store user-selected coins.

## Features

- 🪙 **Portfolio Management**: Add, view, and remove cryptocurrencies from your portfolio
- 💰 **Live Price Tracking**: Real-time cryptocurrency prices (via CoinMarketCap API or demo mode)
- 📊 **Portfolio Valuation**: Automatic calculation of total portfolio value
- 📈 **24h Change Tracking**: Monitor price changes over the last 24 hours
- 💾 **Persistent Storage**: SQLite3 database for storing your portfolio data
- 🎨 **User-Friendly GUI**: Clean and intuitive Tkinter interface
- 🔄 **Auto-Refresh**: Automatic price updates every 60 seconds

## Screenshots

The application features:
- Portfolio overview with current prices
- Add/Remove coin functionality
- Real-time price updates
- Total portfolio value calculation

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Himanibh20/CryptoCurrency-Portfolio-Manager.git
cd CryptoCurrency-Portfolio-Manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Using the Application

1. **Adding Coins to Portfolio**:
   - Click the "➕ Add Coin" button
   - Enter the coin symbol (e.g., BTC, ETH)
   - Enter the coin name (e.g., Bitcoin, Ethereum)
   - Enter the amount you own
   - Click "Add" to save

2. **Viewing Your Portfolio**:
   - All your coins are displayed in the main table
   - View symbol, name, amount, current price, total value, and 24h change
   - Total portfolio value is shown at the top

3. **Removing Coins**:
   - Select a coin from the list
   - Click the "🗑️ Remove Coin" button
   - Confirm the deletion

4. **Refreshing Prices**:
   - Click the "🔄 Refresh Prices" button for manual refresh
   - Prices auto-refresh every 60 seconds

### Demo Mode

The application runs in demo mode by default with mock price data for common cryptocurrencies:
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- XRP
- Cardano (ADA)
- Dogecoin (DOGE)
- Solana (SOL)
- Polygon (MATIC)
- Polkadot (DOT)
- Litecoin (LTC)

### Using Real API (Optional)

To use real-time data from CoinMarketCap:

1. Get a free API key from [CoinMarketCap](https://coinmarketcap.com/api/)
2. Modify `main.py` to pass your API key:
```python
self.api = CoinMarketCapAPI(api_key="YOUR_API_KEY_HERE")
```

## Project Structure

```
CryptoCurrency-Portfolio-Manager/
├── main.py          # Main GUI application
├── database.py      # SQLite3 database operations
├── api.py           # CoinMarketCap API integration
├── requirements.txt # Python dependencies
├── .gitignore      # Git ignore file
└── README.md       # This file
```

## Technologies Used

- **Python 3**: Programming language
- **Tkinter**: GUI framework (built-in with Python)
- **SQLite3**: Database for persistent storage (built-in with Python)
- **CoinMarketCap API**: Cryptocurrency price data
- **Requests**: HTTP library for API calls

## Database Schema

The application uses a simple SQLite3 database with one table:

```sql
CREATE TABLE portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_symbol TEXT NOT NULL,
    coin_name TEXT NOT NULL,
    amount REAL NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This application is for educational and informational purposes only. It is not financial advice. Always do your own research before making investment decisions.
