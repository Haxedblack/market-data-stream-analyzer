from typing import List,Dict,Any
def calculate_vwap(data: List[Dict[str,Any]]) -> float:
    vwap = 0.00
    nsum = 0.00
    dsum = 0.00
    for i in data:
        if i["volume"] > 0 and i['price'] > 0:
            nsum += i["volume"]*i["price"]
            dsum += i["volume"]
    
    if dsum == 0:
        return 0.0
    vwap = nsum/dsum
    return round(vwap,2)
def calculate_moving_average(data: List[Dict[str, Any]], window: int) -> List[Dict[str, Any]]:
    if len(data) < window:
        print(f" Not enough data points for window size {window}")
        return []
    result = []
    for i in range(len(data)- window + 1):
        window_slice = data[i:i+window]
        avg_price = sum(item['price'] for item in window_slice)/window
        result.append({
            'timestamp': window_slice[-1]['timestamp'],
            'moving_avg' : round(avg_price, 2)
        })
    return result