
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

def calculate_volatility(prices: list[float]) -> float:
    if len(prices)<2:
        return 0.0
    price_changes = [(prices[i]-prices[i-1])/ prices[i-1] for i in range(1, len(prices))]
    if len(price_changes) < 2:
        return 0.0 # Not enough data points to calculate stdev
        
    # 2. Return the standard deviation of those changes
    return statistics.stdev(price_changes) * 100 # Returned as a percentage