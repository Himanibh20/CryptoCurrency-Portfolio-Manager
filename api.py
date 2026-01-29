"""
CoinMarketCap API integration module for fetching cryptocurrency prices.
"""
import requests
from typing import Dict, Optional, List


class CoinMarketCapAPI:
    """Handles API calls to CoinMarketCap for cryptocurrency data."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            api_key: CoinMarketCap API key (optional for demo mode)
        """
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.sandbox_url = "https://sandbox-api.coinmarketcap.com/v1"
        self.headers = {
            'Accepts': 'application/json',
        }
        if api_key:
            self.headers['X-CMC_PRO_API_KEY'] = api_key
    
    def get_latest_prices(self, symbols: List[str]) -> Dict:
        """
        Get latest prices for multiple cryptocurrencies.
        
        Args:
            symbols: List of cryptocurrency symbols (e.g., ['BTC', 'ETH'])
            
        Returns:
            Dictionary with symbol as key and price data as value
        """
        if not symbols:
            return {}
        
        # For demo purposes without API key, return mock data
        if not self.api_key:
            return self._get_mock_prices(symbols)
        
        try:
            url = f"{self.base_url}/cryptocurrency/quotes/latest"
            parameters = {
                'symbol': ','.join(symbols),
                'convert': 'USD'
            }
            
            response = requests.get(url, headers=self.headers, params=parameters, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {}
            if 'data' in data:
                for symbol in symbols:
                    if symbol in data['data']:
                        coin_data = data['data'][symbol]
                        result[symbol] = {
                            'name': coin_data['name'],
                            'symbol': symbol,
                            'price': coin_data['quote']['USD']['price'],
                            'percent_change_24h': coin_data['quote']['USD']['percent_change_24h'],
                            'market_cap': coin_data['quote']['USD']['market_cap']
                        }
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return self._get_mock_prices(symbols)
    
    def _get_mock_prices(self, symbols: List[str]) -> Dict:
        """
        Get mock prices for demo purposes when API key is not available.
        
        Args:
            symbols: List of cryptocurrency symbols
            
        Returns:
            Dictionary with mock price data
        """
        # Mock data for common cryptocurrencies
        mock_data = {
            'BTC': {'name': 'Bitcoin', 'price': 43250.50, 'percent_change_24h': 2.5, 'market_cap': 850000000000},
            'ETH': {'name': 'Ethereum', 'price': 2280.75, 'percent_change_24h': 3.2, 'market_cap': 275000000000},
            'BNB': {'name': 'Binance Coin', 'price': 315.20, 'percent_change_24h': 1.8, 'market_cap': 48000000000},
            'XRP': {'name': 'XRP', 'price': 0.52, 'percent_change_24h': -0.5, 'market_cap': 28000000000},
            'ADA': {'name': 'Cardano', 'price': 0.48, 'percent_change_24h': 4.1, 'market_cap': 17000000000},
            'DOGE': {'name': 'Dogecoin', 'price': 0.08, 'percent_change_24h': 5.2, 'market_cap': 11000000000},
            'SOL': {'name': 'Solana', 'price': 98.50, 'percent_change_24h': 6.7, 'market_cap': 42000000000},
            'MATIC': {'name': 'Polygon', 'price': 0.85, 'percent_change_24h': 2.3, 'market_cap': 8000000000},
            'DOT': {'name': 'Polkadot', 'price': 6.75, 'percent_change_24h': 1.9, 'market_cap': 9000000000},
            'LTC': {'name': 'Litecoin', 'price': 72.30, 'percent_change_24h': 0.8, 'market_cap': 5000000000},
        }
        
        result = {}
        for symbol in symbols:
            symbol_upper = symbol.upper()
            if symbol_upper in mock_data:
                data = mock_data[symbol_upper].copy()
                data['symbol'] = symbol_upper
                result[symbol_upper] = data
            else:
                # For unknown symbols, provide a placeholder
                result[symbol_upper] = {
                    'name': symbol_upper,
                    'symbol': symbol_upper,
                    'price': 0.0,
                    'percent_change_24h': 0.0,
                    'market_cap': 0.0
                }
        
        return result
    
    def search_coin(self, query: str) -> List[Dict]:
        """
        Search for cryptocurrencies by name or symbol.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching cryptocurrencies
        """
        # For demo purposes, return a filtered list of mock data
        mock_coins = [
            {'symbol': 'BTC', 'name': 'Bitcoin'},
            {'symbol': 'ETH', 'name': 'Ethereum'},
            {'symbol': 'BNB', 'name': 'Binance Coin'},
            {'symbol': 'XRP', 'name': 'XRP'},
            {'symbol': 'ADA', 'name': 'Cardano'},
            {'symbol': 'DOGE', 'name': 'Dogecoin'},
            {'symbol': 'SOL', 'name': 'Solana'},
            {'symbol': 'MATIC', 'name': 'Polygon'},
            {'symbol': 'DOT', 'name': 'Polkadot'},
            {'symbol': 'LTC', 'name': 'Litecoin'},
        ]
        
        query_lower = query.lower()
        results = [
            coin for coin in mock_coins
            if query_lower in coin['symbol'].lower() or query_lower in coin['name'].lower()
        ]
        
        return results
