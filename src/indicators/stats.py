from typing import List
import statistics
def median_price(prices: List[float]) -> float:
    #Returns the median of the given list of prices.
    if not prices:
        raise ValueError("No prices to calculate the median")
    return statistics.median(prices)

def std_dev(prices: List[float]) -> float:
    #Returns the standard deviation from the prices.
    if len(prices) < 2:
        raise ValueError("Not enough data")
    return statistics.stdev(prices)
    
def price_change_pct(prices: List[float]) -> float:
    #Returns the change in percentage from starting to end price
    if len(prices) < 2:
        raise ValueError("Not enough data")
    return ((prices[-1]-prices[0])*100)/prices[0]