import argparse
import json 
from indicators.vwap import calculate_moving_average,calculate_vwap
from indicators.minmax import get_min_price,get_max_price

parser = argparse.ArgumentParser(description = "Market data Stream Analyzer")
parser.add_argument('--file',type = str , required = True,help = 'Path to the JSON data file')
parser.add_argument('--symbol', type = str , required = True, help = 'Stock symbol to analyze')
parser.add_argument('--window', type = int , default = 5 , help  = 'Time window in minutes')
parser.add_argument('--vwap',action = 'store_true',help = 'Calculate the volume weighted average price')
parser.add_argument('--min',action = 'store_true',help = 'Get minimum value')
parser.add_argument('--max',action = 'store_true', help = 'Get maximum vallue')
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
    print(f" No entries found for symbol '{args.symbol}' with valid price data.")
    exit()

if len(filtered) < args.window:
    print(f" Not enough data for symbol '{args.symbol}' to calculate a {args.window}-point moving average.")
    print(f" Only {len(filtered)} valid entries available.")
    exit()

#calculate moving average
ma = calculate_moving_average(filtered,args.window)
#result
print(f'\n {args.symbol} Moving averages (window = {args.window}):')
for row in ma:
    print(f'{row["timestamp"]} {row["moving_avg"]}')

if args.vwap:
    vwp = calculate_vwap(filtered)
    print(f'VWAP for {args.symbol}: {vwp}')
if args.min:
    min_price = get_min_price(filtered)
    print(f'Minimum price for {args.symbol}: {min_price}')
if args.max:
    max_price = get_max_price(filtered)
    print(f'Maximum price for {args.symbol}: {max_price}')

