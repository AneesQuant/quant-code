# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================

def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        pct_change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(pct_change)
    return returns


def generate_signals(returns):
    signals = []
    for r in returns:
        if r > 1:
            signals.append("BUY")
        elif r < -1:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def calculate_average(prices):
    total = 0
    for price in prices:
        total += price
    average = total / len(prices)
    return round(average, 3)


prices = [124, 1232, 2323, 24234, 32534, 32534]
returns = calculate_returns(prices)
signals = generate_signals(returns)

print("Average:", calculate_average(prices))
print("Returns:", [round(r, 2) for r in returns])
print("Signals:", signals)
