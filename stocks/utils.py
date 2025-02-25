import requests
from django.conf import settings


def get_stock_price(ticker):
    """
    Fetch the current stock price for the given ticker using Alpha Vantage API.
    """
    API_KEY = "CSQMSRBL0MITN2J3"  # Replace with your API key
    BASE_URL = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": ticker,
        "interval": "1min",
        "apikey": API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract the latest stock price
        time_series = data.get("Time Series (1min)")
        if not time_series:
            return None
        latest_timestamp = list(time_series.keys())[0]
        return float(time_series[latest_timestamp]["1. open"])
    except (requests.RequestException, KeyError, ValueError):
        return None

def get_real_price(ticker):
    """
    Fetches the real-time stock price for a given ticker symbol using Alpha Vantage API.
    """
    try:
        response = requests.get(
            'https://www.alphavantage.co/query',
            params={
                'function': 'GLOBAL_QUOTE',
                'symbol': ticker,
                'apikey': settings.ALPHA_VANTAGE_API_KEY,
            }
        )
        response.raise_for_status()
        print("fetching form the api ")
        data = response.json()
        print(data)
        return data  # Return the entire response dictionary
    except (KeyError, ValueError, requests.RequestException) as e:
        print(f"Error fetching price for ticker {ticker}: {e}")
        return None