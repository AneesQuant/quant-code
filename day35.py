# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================

prices = [180, 182, 178, 185]

for i in range(1, len(prices)):
    change = prices[i] - prices[i-1]
    pct_change = (change / prices[i-1]) * 100
    print("Change:", change, "| %:", round(pct_change, 2))


def calculate_average(prices):
    total = 0
    for price in prices:
        total += price
    average = total / len(prices)
    return (round(average, 3))


prices = [124, 1232, 2323, 24234, 32534, 32534]

print("Average:", calculate_average(prices))
