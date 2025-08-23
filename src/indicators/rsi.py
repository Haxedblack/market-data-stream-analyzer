def calculate_rsi(prices: list[float],period: int = 14) -> float:
    if len(prices) < period:
        return float('nan')
    
    changes = [prices[i] - prices[i-1] for i in range(1,len(prices))]

    initial_gains= sum(change for change in changes[:period] if change>0)
    initial_losses = sum(abs(change) for change in changes[:period] if change<0)

    avg_gain = initial_gains/period
    avg_loss = initial_losses/period

    for i in range(period, len(changes)):
        change = changes[i]
        gain = change if change > 0 else 0 
        loss = abs(change) if change < 0 else 0
        avg_gain = (avg_gain * (period-1) + gain) / period
        avg_loss = (avg_loss * (period-1)+ loss) / period

    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain/ avg_loss
    rsi = 100 - (100/ (1+ rs))
    
    return rsi