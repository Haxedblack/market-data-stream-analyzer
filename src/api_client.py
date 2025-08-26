import os 
import requests
from typing import List,Dict

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_intraday_data(symbol: str, interval: str = '5min') -> List[Dict]:
    if not API_KEY:
        raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY environment variable.")
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": f"{interval}",
        "apikey": API_KEY,
        "outputsize": 'full'
    }
    print(f"Fetching live data for {symbol} ...")
    response = requests.get(BASE_URL, params= params)
    response.raise_for_status()

    data = response.json()
    if "Error Message" in data:
        raise ConnectionError(f'API Error: {data['Error Message']}')

    time_series_key = f"Time Series ({interval})"
    time_series_data = data.get(time_series_key, {})
    processed_data = []
    for timestamp, values in time_series_data.items():
        processed_data.append({
            "timestamp": timestamp,
            "symbol": symbol,
            "price": float(values["4. close"]),
            "volume": int(values["5. volume"])
        }) 
    return sorted(processed_data, key = lambda x: x["timestamp"])
if __name__ == "__main__":
    try:
        live_data = fetch_intraday_data('AAPL')
        if live_data:
            print(f"Successfully fetched {len(live_data)} data points.")
            print('Most recent entry:', live_data[-1])
    except (ValueError, ConnectionError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")