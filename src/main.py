import argparse
import json 
from src.indicators.vwap import calculate_moving_average,calculate_vwap
from src.indicators.minmax import get_min_price,get_max_price
from src.indicators.stats import median_price,std_dev,price_change_pct,calculate_volatility
from datetime import datetime
from collections import defaultdict
from colorama import init, Style, Fore
from src.plotting import plot_price_stats
import sys
import csv
def floor_timestamp_to_window(ts: datetime, window: int) -> datetime:
    floored_minute = (ts.minute // window )* window 
    return ts.replace(minute= floored_minute, second = 0 ,microsecond = 0)

def process_entry(entry, args, buckets, stat_set, writer):
    """
    Filters a single data entry, updates its bucket, and calculates/prints/exports stats.
    """
    # 1. Filter the entry to ensure it's the correct symbol
    if entry.get('symbol') != args.symbol:
        return  # Skip this entry if the symbol doesn't match

    # 2. Add the entry to its corresponding time bucket
    ts = datetime.fromisoformat(entry['timestamp'])
    floored_time = floor_timestamp_to_window(ts, args.window)
    bucket_entries = buckets[floored_time]
    bucket_entries.append(entry)
    # 3. Calculate all requested stats for the updated bucket
    print(f"\n--- Updated Stats for Time Window: {floored_time} ---")
    # Initialize all possible CSV columns to None to avoid missing key errors
    row_data = {
        'time': floored_time.isoformat(),
        'vwap': None,
        'min': None,
        'max': None,
        'median': None,
        'std': None,
        'change': None,
        'volatility': None
    }
    prices = [e['price'] for e in bucket_entries]

    if args.vwap:
        vwap = calculate_vwap(bucket_entries)
        print(f"  VWAP: {vwap:.2f}")
        row_data['vwap'] = vwap

    if args.min:
        min_price = get_min_price(bucket_entries)
        print(f"  Min Price: {min_price:.2f}")
        row_data['min'] = min_price

    if args.max:
        max_price = get_max_price(bucket_entries)
        print(f"  Max Price: {max_price:.2f}")
        row_data['max'] = max_price

    if args.volatility:
        vol = calculate_volatility(prices)
        print(f"  Volatility: {vol:.2f}%")
        row_data['volatility'] = vol

    if args.stats:
        try:
            if 'median' in stat_set:
                median = median_price(prices)
                print(f"  Median: {median:.2f}")
                row_data['median'] = median
            if 'std' in stat_set:
                std = std_dev(prices)
                print(f"  Std Dev: {std:.2f}")
                row_data['std'] = std
            if 'change' in stat_set:
                change = price_change_pct(prices)
                print(f"  Change: {change:+.2f}%")
                row_data['change'] = change
        except ValueError:
            pass # Silently ignore stat errors for small data sets

    # 4. Write the results to the CSV file if exporting is enabled
    if writer:
        writer.writerow(row_data)
init(autoreset= True)
parser = argparse.ArgumentParser(description = "Market data Stream Analyzer")
parser.add_argument('--file',type = str , required = False,help = 'Path to the JSON data file')
parser.add_argument('--symbol', type = str , required = True, help = 'Stock symbol to analyze')
parser.add_argument('--window', type = int , default = 5 , help  = 'Time window in minutes')
parser.add_argument('--vwap',action = 'store_true',help = 'Calculate the volume weighted average price')
parser.add_argument('--min',action = 'store_true',help = 'Get minimum value')
parser.add_argument('--max',action = 'store_true', help = 'Get maximum vallue')
parser.add_argument('--stats',type = str , default = None ,help = "Get the median,deviation and change in percent")
parser.add_argument('--plot', action = 'store_true', help = 'Generate a line chart of prices and stats')
parser.add_argument('--export',type = str , help = 'Export per-bucket stats to CSV file')
parser.add_argument('--volatility',action = 'store_true', help = 'Calculate the price volatility per bucket')
args = parser.parse_args()

print('File:', args.file)
print('Symbol:', args.symbol)
print('Window:', args.window)

symbols_to_process = {s.strip.upper() for s in args.symbol.split(',')}
print(f'Symbols to process: {','.join(symbols_to_process)}')
if args.plot and not args.file:
    print("Error: Plotting requires an input file. Please use the --file argument.")
    sys.exit(1)
csv_writer = None
csv_file = None
if args.export:
    try:
        # Open the file and keep it open
        csv_file = open(args.export, 'w', newline='')
        
        # Define the full set of possible headers
        fieldnames = ['time', 'vwap', 'min', 'max', 'median', 'std', 'change', 'volatility']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    except IOError as e:
        print(f"Error opening export file: {e}")
        # We can choose to exit or just disable exporting
        csv_writer = None
#loading file
all_data = []
buckets = defaultdict(lambda: defaultdict(list))
# --- Stat Flag Handling ---
VALID_STATS = {'median', 'std', 'change'}
stat_set = set() # Default to an empty set

if args.stats:
    # Create a set from the user's comma-separated input
    user_stats = set(map(str.strip, args.stats.split(',')))
    
    # Find any stats the user provided that are not in our valid list
    invalid = user_stats - VALID_STATS
    
    if invalid:
        print(f"Error: Invalid stat(s) provided: {', '.join(invalid)}")
        sys.exit(1)
    
    # If we get here, all stats are valid
    stat_set = user_stats
if args.file:
    # Logic for reading from a file
    print(f"Reading from file: {args.file}")
    with open(args.file, 'r') as f:
        all_data = json.load(f)
    # Now, process each entry from the file
    for entry in all_data:
        process_entry(entry, args, buckets, stat_set , csv_writer, symbols_to_process)
else:
    # Logic for reading from a stream
    print("Listening to stdin stream... (Ctrl+C to stop)")
    for line in sys.stdin:
        try:
            entry = json.loads(line)
            # Process each entry from the stream
            process_entry(entry, args, buckets, stat_set, csv_writer, symbols_to_process)
        except (json.JSONDecodeError, KeyError):
            continue
