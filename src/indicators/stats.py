from typing import List,Dict,Any
import statistics
def median_price(prices: List[float]) -> float:
    if not prices:
        raise ValueError("No prices to calculate the median")
    return statistics.median(prices)

def std_dev(prices: List[float]) -> float:
    if len(prices) < 2:
        raise ValueError("Not enough data")
    return statistics.stdev(prices)
    
def price_change_pct(prices: List[float]) -> float:
    if len(prices) < 2:
        raise ValueError("Not enough data")
    return ((prices[-1]-prices[0])*100)/prices[0]