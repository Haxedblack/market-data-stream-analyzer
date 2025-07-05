import matplotlib.pyplot as plt
from typing import List,Dict
import os
from datetime import datetime
def plot_price_stats(bucket : Dict[datetime, List[float]], symbol : str,raw_ma: List[tuple],output_dir : str = 'output/plots/'):
    os.makedirs(output_dir,exist_ok = True)

    timestamps = []
    prices = []

    for ts_str, price_list in bucket.items():
        if not price_list:
            continue
        timestamps.append(ts_str)
        avg_pr = sum(price_list) / len(price_list)
        prices.append(avg_pr)
    x_ma , y_ma = zip(*raw_ma)
    plt.figure(figsize=(10,5))
    plt.plot(timestamps,prices, label = "Avg price", marker='o', color='blue')
    plt.plot(x_ma,y_ma,label = "Moving average", linestyle= "--", color = 'green')

    plt.title(f"{symbol} Price over time")
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    
    output_path = os.path.join(output_dir, f"{symbol}_combined_plot.png")
    plt.savefig(output_path)
    plt.close()
    print(f'Combined Plot saved to: {output_path}')
        
