# src/indicators/minmax.py

from typing import List, Dict, Any

def get_min_price(data: List[Dict[str, Any]]) -> float:
    prices = [item["price"] for item in data if "price" in item and item["price"] > 0]
    return round(min(prices), 2) if prices else 0.0

def get_max_price(data: List[Dict[str, Any]]) -> float:
    prices = [item["price"] for item in data if "price" in item and item["price"] > 0]
    return round(max(prices), 2) if prices else 0.0
