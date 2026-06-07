# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================


def calculate_returns(prices):
    """Calculate percentage returns between each price."""
    returns = []
    for i in range(1, len(prices)):
        pct_change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(round(pct_change, 2))
    return returns


def generate_signals(returns, buy_threshold=1.0, sell_threshold=-1.0):
    """Generate BUY, SELL, or HOLD signals based on return thresholds."""
    signals = []
    for r in returns:
        if r > buy_threshold:
            signals.append("BUY")
        elif r < sell_threshold:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def trend_confirmation(signals):
    """Confirm trend if two consecutive signals match."""
    confirmed = []
    for i in range(1, len(signals)):
        if signals[i] == "BUY" and signals[i-1] == "BUY":
            confirmed.append("LONG CONFIRMED")
        elif signals[i] == "SELL" and signals[i-1] == "SELL":
            confirmed.append("SELL CONFIRMED")
        else:
            confirmed.append("NO CONFIRMATION")
    return confirmed


def backtest(prices, signals, starting_capital=10000):
    """Long-only backtest with drawdown and full performance stats."""
    position = None
    entry_price = 0
    total_profit = 0
    trades = 0
    wins = 0
    profits = []
    peak = 0
    max_drawdown = 0
    running = 0

    for i in range(len(signals)):
        signal = signals[i]
        price = prices[i + 1]

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
            print(f"  BUY  at ${entry_price}")

        elif signal == "SELL" and position == "LONG":
            profit = price - entry_price
            total_profit += profit
            trades += 1
            profits.append(round(profit, 2))
            if profit > 0:
                wins += 1
            print(f"  SELL at ${price:<8} | Profit: ${round(profit, 2)}")
            position = None
            running += profit
            if running > peak:
                peak = running
            if (peak - running) > max_drawdown:
                max_drawdown = peak - running

    # ── Stats ────────────────────────────────────────────
    win_rate = round((wins / trades) * 100, 2) if trades > 0 else 0
    avg_profit = round(sum(profits) / len(profits), 2) if profits else 0
    total_return = round((total_profit / starting_capital) * 100, 2)
    losses = trades - wins
    avg_win = round(sum(p for p in profits if p > 0) /
                    wins, 2) if wins > 0 else 0
    avg_loss = round(sum(p for p in profits if p < 0) /
                     losses, 2) if losses > 0 else 0
    rr_ratio = round(avg_win / abs(avg_loss), 2) if avg_loss != 0 else 0

    print("=" * 45)
    print(f"  Total Trades   : {trades}")
    print(f"  Win Rate       : {win_rate}%")
    print(f"  Avg Profit     : ${avg_profit}")
    print(f"  Avg Win        : ${avg_win}")
    print(f"  Avg Loss       : ${avg_loss}")
    print(f"  Risk/Reward    : {rr_ratio}")
    print(f"  Max Drawdown   : ${round(max_drawdown, 2)}")
    print(f"  Total Return   : {total_return}%")
    print(f"  Total Profit   : ${round(total_profit, 2)}")
    print("=" * 45)


def market_summary(prices, returns):
    """Print a dashboard summary of price and return statistics."""
    avg_return = round(sum(returns) / len(returns), 2)
    price_change = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)

    print("=" * 45)
    print("        QUANT TRADING DASHBOARD")
    print("=" * 45)
    print(f"  Start Price    : ${prices[0]}")
    print(f"  End Price      : ${prices[-1]}")
    print(f"  Total Change   : {price_change}%")
    print(f"  Best Return    : {max(returns)}%")
    print(f"  Worst Return   : {min(returns)}%")
    print(f"  Average Return : {avg_return}%")
    print("=" * 45)


# ── DATA ────────────────────────────────────────────────────
prices = [180, 182, 178, 185, 190, 188, 195,
          197, 201, 199, 203, 208, 205, 209, 211]

# ── CALCULATIONS ────────────────────────────────────────────
returns = calculate_returns(prices)
signals = generate_signals(returns)
confirmations = trend_confirmation(signals)

# ── DASHBOARD ───────────────────────────────────────────────
market_summary(prices, returns)
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmations}")
print("=" * 45)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n          Backtest Results")
print("=" * 45)
backtest(prices, signals)
