# 📈 My Crypto Portfolio Tracker

A Python-based desktop application that tracks cryptocurrency investments using live market data from the CoinMarketCap API. The application calculates portfolio value, profit/loss, and displays real-time cryptocurrency prices through a user-friendly Tkinter GUI.

---

## 🚀 Features

- Live cryptocurrency price tracking using CoinMarketCap API
- Portfolio value calculation
- Profit/Loss analysis for each cryptocurrency
- Overall portfolio performance tracking
- Interactive Tkinter-based GUI
- Manual portfolio refresh using the Update button
- Color-coded profit and loss indicators

---

## 🛠️ Technologies Used

- Python
- Tkinter
- Requests
- JSON
- CoinMarketCap API

---

## 📂 Project Structure

```text
My-Crypto-Portfolio/
│
├── crypto_portfolio.py
├── bitcoin.ico
├── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/my-crypto-portfolio.git
cd my-crypto-portfolio
```

### Install dependencies

```bash
pip install requests
```

---

## 🔑 API Setup

This project uses the CoinMarketCap API to fetch live cryptocurrency prices.

1. Create an account at CoinMarketCap.
2. Generate an API key.
3. Replace the API key in the code:

```python
headers = {
    "X-CMC_PRO_API_KEY": "YOUR_API_KEY",
    "Accepts": "application/json"
}
```

⚠️ Never expose your API key in public repositories.

---

## ▶️ Running the Application

```bash
python crypto_portfolio.py
```

---

## 🧮 How It Works

The application:

1. Fetches live cryptocurrency prices from CoinMarketCap.
2. Matches portfolio holdings with current market prices.
3. Calculates:
   - Amount Invested
   - Current Value
   - Profit/Loss per Coin
   - Total Portfolio Profit/Loss
4. Displays results in a structured table.

---

## 📊 Sample Metrics

- Coin Name
- Current Price
- Quantity Owned
- Amount Paid
- Current Value
- Profit/Loss per Coin
- Total Portfolio Profit/Loss

---

## 🎯 Key Learning Outcomes

Through this project, I gained hands-on experience with:

- REST API Integration
- JSON Data Processing
- Desktop Application Development
- GUI Design using Tkinter
- Financial Data Calculations
- Error Handling and Debugging

---

## 🔮 Future Enhancements

- SQLite database integration
- Add/Edit/Delete portfolio holdings
- Auto-refresh functionality
- Profit percentage tracking
- Portfolio performance charts
- Export reports to CSV/PDF
- Multi-currency support
- Web-based version using Flask

---

## 👨‍💻 Author

**Himani**

Aspiring Software Developer | Python Developer | Data Analytics Enthusiast

If you found this project interesting, consider giving it a ⭐ on GitHub.
