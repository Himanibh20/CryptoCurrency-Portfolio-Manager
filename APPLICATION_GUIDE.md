# CryptoCurrency Portfolio Manager - Application Guide

## Application Overview

This is a complete desktop application for managing cryptocurrency portfolios built with Python and Tkinter.

## Application Components

### 1. Main Window Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  🪙 CryptoCurrency Portfolio Manager                            │  ← Title Bar
├─────────────────────────────────────────────────────────────────┤
│  [➕ Add Coin]  [🔄 Refresh Prices]  [🗑️ Remove Coin]         │  ← Control Panel
├─────────────────────────────────────────────────────────────────┤
│  Total Portfolio Value: $XXX,XXX.XX                             │  ← Portfolio Summary
├─────────────────────────────────────────────────────────────────┤
│  Symbol │ Name      │ Amount   │ Price      │ Value     │ 24h   │
│  ───────┼───────────┼──────────┼────────────┼───────────┼───────│
│  BTC    │ Bitcoin   │ 0.5      │ $43,250.50 │ $21,625.25│ +2.5% │  ← Portfolio
│  ETH    │ Ethereum  │ 2.0      │ $2,280.75  │ $4,561.50 │ +3.2% │    Table
│  ADA    │ Cardano   │ 1000.0   │ $0.48      │ $480.00   │ +4.1% │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
│  Ready | Using demo mode (no API key)                           │  ← Status Bar
└─────────────────────────────────────────────────────────────────┘
```

### 2. Add Coin Dialog

```
┌──────────────────────────────┐
│  Add Cryptocurrency          │
├──────────────────────────────┤
│                              │
│  Coin Symbol (e.g., BTC):    │
│  [________________]           │
│                              │
│  Coin Name (e.g., Bitcoin):  │
│  [________________]           │
│                              │
│  Amount:                     │
│  [________________]           │
│                              │
│  [Add]  [Cancel]             │
│                              │
└──────────────────────────────┘
```

## Features Demonstration

### 1. Adding a Cryptocurrency
- Click "➕ Add Coin"
- Enter coin details (symbol, name, amount)
- Coin is saved to SQLite database
- Price is automatically fetched

### 2. Viewing Portfolio
- All coins displayed in table format
- Shows current price, value, and 24h change
- Total portfolio value calculated automatically
- Color-coded 24h changes (green = up, red = down)

### 3. Removing Coins
- Select a coin from the table
- Click "🗑️ Remove Coin"
- Confirm deletion
- Coin removed from database

### 4. Price Updates
- Manual: Click "🔄 Refresh Prices"
- Automatic: Every 60 seconds
- Uses CoinMarketCap API or demo data

## Technical Details

### Database Schema
```sql
CREATE TABLE portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_symbol TEXT NOT NULL,
    coin_name TEXT NOT NULL,
    amount REAL NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Supported Cryptocurrencies (Demo Mode)
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

### API Integration
The application supports:
1. **Demo Mode** (default): Uses mock price data, no API key needed
2. **Live Mode**: Connect to CoinMarketCap API with your API key

### Files Structure
```
CryptoCurrency-Portfolio-Manager/
├── main.py              # GUI application (400+ lines)
│   ├── CryptoPortfolioApp class
│   ├── UI setup and styling
│   ├── Event handlers
│   └── Portfolio management
│
├── database.py          # Database operations (120+ lines)
│   ├── PortfolioDB class
│   ├── CRUD operations
│   └── SQLite3 integration
│
├── api.py               # API integration (150+ lines)
│   ├── CoinMarketCapAPI class
│   ├── Price fetching
│   ├── Mock data provider
│   └── Coin search
│
├── requirements.txt     # Dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

## Usage Examples

### Example 1: Starting with an Empty Portfolio
1. Launch application: `python main.py`
2. Click "➕ Add Coin"
3. Add your first coin (e.g., BTC, Bitcoin, 0.5)
4. See it appear in the portfolio table with current price

### Example 2: Managing Multiple Coins
1. Add multiple coins to your portfolio
2. Monitor total portfolio value in real-time
3. Track 24h price changes for each coin
4. Remove coins you no longer hold

### Example 3: Using with Real API
1. Get API key from CoinMarketCap
2. Edit main.py line: `self.api = CoinMarketCapAPI(api_key="YOUR_KEY")`
3. Run application with live prices

## Color Scheme
- **Title Bar**: Dark blue-gray (#2C3E50)
- **Add Button**: Green (#27AE60)
- **Refresh Button**: Blue (#3498DB)
- **Delete Button**: Red (#E74C3C)
- **Portfolio Summary**: Dark gray (#34495E)
- **Background**: Light gray (#ECF0F1)
- **Positive Changes**: Green
- **Negative Changes**: Red

## Key Features
✅ User-friendly GUI with Tkinter
✅ Persistent data storage with SQLite3
✅ Live price tracking (CoinMarketCap API)
✅ Demo mode with mock data
✅ Automatic price refresh (60 seconds)
✅ Portfolio value calculation
✅ 24h price change tracking
✅ Add/Remove coins easily
✅ Clean and modern interface
✅ Cross-platform (Windows, Mac, Linux)
