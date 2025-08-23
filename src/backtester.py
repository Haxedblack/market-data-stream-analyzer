from typing import List,Dict,Any
from colorama import Fore,init
init(autoreset = True)
class Strategy:

    def __init__(self, initial_cash: float = 100000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        
        self.position = 0
        self.is_long = False

        self.trades = 0 
        self.pnl = 0

    def generate_signals(self, data):
        pass
    def buy(self, price: float, timestamp):
        shares_to_buy = self.cash/price
        self.position = shares_to_buy
        self.cash = 0.0
        self.is_long = True
        self.trades += 1
        print(f"  EXECUTED BUY: {shares_to_buy:,.2f} shares @ ${price:,.2f} on {timestamp}")
    
    def sell(self, price: float, timestamp):
        market_value = self.position * price
        self.cash = market_value
        self.pnl = self.cash - self.initial_cash

        self.position = 0
        self.is_long = False
        self.trades += 1
        print(f"  EXECUTED SELL: closing position @ ${price:,.2f} | Final P&L: ${self.pnl:,.2f}")

    def print_summary(self):

        print("\n--- Backseat Summary ---")
        print(f"Initial Cash: {self.initial_cash:,.2f}")
        print(f"Final Cash: ${self.cash:,.2f}")
        print(f"Final P&L: ${self.pnl:,.2f}")
        print(f"Total Trades: {self.trades}")

from .indicators.vwap import calculate_moving_average

class SmaCrossoverStrategy(Strategy):
    
    def __init__(self, fast_period: int, slow_period: int, initial_cash: float = 100000.0):
        super().__init__(initial_cash)
        if fast_period >= slow_period:
            raise ValueError("Fast MA period must be less than Slow MA period")
        
        self.fast_period = fast_period
        self.slow_period = slow_period

        self.slow_ma_history = []
        self.fast_ma_history = []

    def generate_signals(self, entries: List[Dict]):
        
        if len(entries) < self.slow_period:
            return
        
        current_fast_ma = sum(e['price'] for e in entries[-self.fast_period:]) / self.fast_period
        current_slow_ma = sum(e['price'] for e in entries[-self.slow_period:]) / self.slow_period

        self.slow_ma_history.append(current_slow_ma)
        self.fast_ma_history.append(current_fast_ma)

        if len(self.fast_ma_history) < 2:
            return
        
        prev_fast = self.fast_ma_history[-2]
        prev_slow = self.slow_ma_history[-2]
        latest_price = entries[-1]['price']
        latest_timestamp = entries[-1]['timestamp'] 
        if prev_fast <= prev_slow and current_fast_ma > current_slow_ma and not self.is_long:
            print(Fore.GREEN + f'Buy Signal @ ${latest_price:,.2f} on {latest_timestamp}')
            self.buy(latest_price,latest_timestamp)
        if prev_fast >= prev_slow and current_fast_ma < current_slow_ma and self.is_long:
            print(Fore.RED + f"Sell Signal @ ${latest_price:,.2f} on {latest_timestamp}")
            self.sell(latest_price,latest_timestamp)