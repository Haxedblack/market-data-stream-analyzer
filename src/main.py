import argparse
import json 
from indicators.vwap import calculate_moving_average,calculate_vwap
from indicators.minmax import get_min_price,get_max_price
from indicators.stats import median_price,std_dev,price_change_pct
from datetime import datetime
from collections import defaultdict
from colorama import init, Style, Fore
def floor_timestamp_to_window(ts: datetime, window: int) -> datetime:
    floored_minute = (ts.minute // window )* window 
    return ts.replace(minute= floored_minute, second = 0 ,microsecond = 0)
init(autoreset= True)
parser = argparse.ArgumentParser(description = "Market data Stream Analyzer")
parser.add_argument('--file',type = str , required = True,help = 'Path to the JSON data file')
parser.add_argument('--symbol', type = str , required = True, help = 'Stock symbol to analyze')
parser.add_argument('--window', type = int , default = 5 , help  = 'Time window in minutes')
parser.add_argument('--vwap',action = 'store_true',help = 'Calculate the volume weighted average price')
parser.add_argument('--min',action = 'store_true',help = 'Get minimum value')
parser.add_argument('--max',action = 'store_true', help = 'Get maximum vallue')
parser.add_argument('--stats',type = str , default = None ,help = "Get the median,deviation and change in percent")

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
             print(Fore.RED+" Skipping entry with missing 'price':", entry)
if not filtered:
    print(Fore.RED+f" No entries found for symbol '{args.symbol}' with valid price data.")
    exit()

if len(filtered) < args.window:
    print(Fore.RED+f" Not enough data for symbol '{args.symbol}' to calculate a {args.window}-point moving average.")
    print(Fore.RED+f" Only {len(filtered)} valid entries available.")
    exit()

#calculate moving average
ma = calculate_moving_average(filtered,args.window)
#result
print(Fore.GREEN+f'\n{args.symbol} Moving averages (window = {args.window}):')
for row in ma:
    print(f'{row["timestamp"]} {row["moving_avg"]}')
buckets = defaultdict(list)
for entry in filtered:
    # Parse the timestamp string to a datetime object
    ts = datetime.fromisoformat(entry['timestamp'])
    floored_time = floor_timestamp_to_window(ts, args.window)
    buckets[floored_time].append(entry)
if args.stats:
        stat_set = set(map(str.strip , args.stats.split(',')))
invalid = [x for x in stat_set if x not in {'median','std','change'}]
if invalid:
    print(f"Invalid stat flag: {','.join(invalid)}")
    exit()
for time_key in sorted(buckets):
    print(Style.BRIGHT+Fore.GREEN+f"\nTime Window: {time_key}")
    entries = buckets[time_key]
    if args.vwap:
        vwp = calculate_vwap(entries)
        print(f'VWAP for {args.symbol}: {vwp:.2f}')
    if args.min:
        min_price = get_min_price(entries)
        print(f'Minimum price for {args.symbol}: {min_price:.2f}')
    if args.max:
        max_price = get_max_price(entries)
        print(f'Maximum price for {args.symbol}: {max_price:.2f}')
    prices_stat = [entry['price'] for entry in entries]
    try:
        if 'median' in stat_set:
            print(f"Median : {median_price(prices_stat):.2f}")
        if 'std' in stat_set:
            print(f"Standard deviation : {std_dev(prices_stat):.2f}")
        if "change" in stat_set:
            print(f'Percentage change : {price_change_pct(prices_stat):+.2f}%')
    except ValueError as e:
        print(Fore.RED + f'   Skipping stat: {e}')

