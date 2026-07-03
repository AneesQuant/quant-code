# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================

import math


def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        pct_change = (prices[i] - prices[i - 1]) / prices[i - 1]
        returns.append(pct_change)
    return returns


def generate_signals(returns, threshold=0.01):
    signals = []
    for r in returns:
        if r > threshold:
            signals.append("BUY")
        elif r < -threshold:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def trend_confirmation(signals):
    confirmed = ["NO DATA"]
    for i in range(1, len(signals)):
        if signals[i] == signals[i - 1] == "BUY":
            confirmed.append("LONG CONFIRMED")
        elif signals[i] == signals[i - 1] == "SELL":
            confirmed.append("SHORT CONFIRMED")
        else:
            confirmed.append("NO CONFIRMATION")
    return confirmed


def backtest(prices, signals):
    position = None
    entry_price = 0
    total_profit = 0
    trades = 0
    wins = 0
    equity_curve = [0]

    for i in range(len(signals)):
        if i + 1 >= len(prices):
            break
        price = prices[i + 1]
        signal = signals[i]

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price

        elif signal == "SELL" and position == "LONG":
            profit = price - entry_price
            total_profit += profit
            trades += 1
            if profit > 0:
                wins += 1
            position = None

        equity_curve.append(total_profit)

    win_rate = (wins / trades * 100) if trades else 0
    avg_equity = sum(equity_curve) / len(equity_curve)
    returns_std = (
        sum((x - avg_equity) ** 2 for x in equity_curve) / len(equity_curve)) ** 0.5
    sharpe_like = ((total_profit / trades) /
                   returns_std if trades and returns_std != 0 else 0)

    print("\n===== BACKTEST SUMMARY =====")
    print(f"  Trades       : {trades}")
    print(f"  Wins         : {wins}")
    print(f"  Win Rate     : {round(win_rate, 2)}%")
    print(f"  Total Profit : {round(total_profit, 2)}")
    print(f"  Sharpe-like  : {round(sharpe_like, 3)}")
    print("============================\n")
    return equity_curve


def market_summary(prices, returns):
    print("\n===== MARKET DASHBOARD =====")
    print(f"  Highest Price     : {max(prices)}")
    print(f"  Lowest Price      : {min(prices)}")
    print(f"  Average Price     : {round(sum(prices) / len(prices), 2)}")
    print(f"  Best Return       : {round(max(returns) * 100, 2)}%")
    print(f"  Worst Return      : {round(min(returns) * 100, 2)}%")
    print(f"  Total Data Points : {len(prices)}")
    print("============================\n")


# ── DATA ────────────────────────────────────────────────────
prices = [180, 182, 178, 185, 190, 188, 195,
          197, 201, 199, 203, 208, 205, 209, 211]

# ── CALCULATIONS ────────────────────────────────────────────
returns = calculate_returns(prices)
signals = generate_signals(returns)
confirmed = trend_confirmation(signals)

# ── OUTPUT ───────────────────────────────────────────────────
market_summary(prices, returns)
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmed}")
print("\n===== BACKTEST =====")
equity = backtest(prices, signals)
