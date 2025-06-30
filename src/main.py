import argparse
import json 

parser = argparse.ArgumentParser(description = "Market data Stream Analyzer")
parser.add_argument('--file',type = str , required = True,help = 'Path to the JSON data file')
parser.add_argument('--symbol', type = str , required = True, help = 'Stock symbol to analyze')
parser.add_argument('--window', type = int , default = 5 , help  = 'Time window in minutes')
args = parser.parse_args()
print('File:', args.file)
print('Symbol:', args.symbol)
print('Window:', args.window)
#loading file
with open(args.file,'r') as f:
    all_data = json.load(f)
#filtering
filtered = []
for entry in all_data:
    if entry.get('symbol') == args.symbol:
        if 'price' in entry:
            filtered.append(entry)
        else:
             print(" Skipping entry with missing 'price':", entry)
if not filtered:
    print(f"❌ No entries found for symbol '{args.symbol}' with valid price data.")
    exit()

if len(filtered) < args.window:
    print(f"❌ Not enough data for symbol '{args.symbol}' to calculate a {args.window}-point moving average.")
    print(f"✅ Only {len(filtered)} valid entries available.")
    exit()


def calculate_moving_average(data,window):
    if len(data) < window:
        print(f" Not enough data points for window size {window}")
        return []
    result = []
    for i in range(len(data)- window + 1):
        window_slice = data[i:i+window]
        avg_price = sum(item['price'] for item in window_slice)
        result.append({
            'timestamp': window_slice[-1]['timestamp'],
            'moving_avg' : round(avg_price, 2)
        })
    return result
#calculate moving average
ma = calculate_moving_average(filtered,args.window)
#result
print(f'\n {args.symbol} Moving averages (window = {args.window}):')
for row in ma:
    print(f'{row["timestamp"]} {row["moving_avg"]}')
