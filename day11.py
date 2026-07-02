# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: William
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


def backtest(prices, signals):
    """Simple long-only backtest: buy on BUY signal, sell on SELL signal."""
    position = None
    entry_price = 0
    total_profit = 0
    trades = 0
    wins = 0

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
            if profit > 0:
                wins += 1
            print(f"  SELL at ${price:<8} | Profit: ${round(profit, 2)}")
            position = None

    # ── Win Rate Calculation ─────────────────────────────
    win_rate = round((wins / trades) * 100, 2) if trades > 0 else 0

    print("=" * 45)
    print(f"  Total Trades : {trades}")
    print(f"  Winning Trades : {wins}")
    print(f"  Losing Trades  : {trades - wins}")
    print(f"  Win Rate       : {win_rate}%")
    print(f"  Total Profit : ${round(total_profit, 2)}")
    print("=" * 45)


def market_summary(prices, returns):
    """Print a dashboard summary of price and return statistics."""
    avg_return = round(sum(returns) / len(returns), 2)
    price_change = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)

    print("=" * 45)
    print("        QUANT TRADING DASHBOARD")
    print("=" * 45)
    print(f"  Highest Price  : ${max(prices)}")
    print(f"  Lowest Price   : ${min(prices)}")
    print(f"  Average Price  : ${round(sum(prices) / len(prices), 2)}")
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
print(f"  Returns      : {returns}")
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmations}")
print("=" * 45)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n          Backtest Results")
print("=" * 45)
backtest(prices, signals)
