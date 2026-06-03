# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================


def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        pct_change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(round(pct_change, 2))
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


def trend_confirmation(signals):
    confirmed = []
    for i in range(1, len(signals)):
        if signals[i] == "BUY" and signals[i-1] == "BUY":
            confirmed.append("LONG CONFIRMED")
        elif signals[i] == "SELL" and signals[i-1] == "SELL":
            confirmed.append("SHORT CONFIRMED")
        else:
            confirmed.append("NO CONFIRMATION")
    return confirmed


def backtest(prices, signals):
    position = None
    entry_price = 0
    total_profit = 0
    trade_count = 0
    winning_trades = 0
    losing_trades = 0

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
            trade_count += 1
            if profit > 0:
                winning_trades += 1
                print(
                    f"  SELL at ${price} | Profit: ${round(profit, 2)} WIN")
            else:
                losing_trades += 1
                print(
                    f"  SELL at ${price} | Profit: ${round(profit, 2)} LOSS")
            position = None

    win_rate = round((winning_trades / trade_count) *
                     100, 2) if trade_count > 0 else 0

    print("=" * 40)
    print("      BACKTEST SUMMARY")
    print("=" * 40)
    print(f"  Total Trades   : {trade_count}")
    print(f"  Winning Trades : {winning_trades}")
    print(f"  Losing Trades  : {losing_trades}")
    print(f"  Win Rate       : {win_rate}%")
    print(f"  Total Profit   : ${round(total_profit, 2)}")
    print("=" * 40)


def market_summary(prices, returns):
    print("=" * 40)
    print("      QUANT TRADING DASHBOARD")
    print("=" * 40)
    print(f"  Highest Price  : ${max(prices)}")
    print(f"  Lowest Price   : ${min(prices)}")
    print(f"  Average Price  : ${round(sum(prices) / len(prices), 2)}")
    print(f"  Best Return    : {max(returns)}%")
    print(f"  Worst Return   : {min(returns)}%")
    print(f"  Total Days     : {len(prices)}")
    print("=" * 40)


# ── DATA ────────────────────────────────────────────────────
prices = [180, 182, 178, 185, 190, 188, 195,
          197, 201, 199, 203, 208, 205, 209, 211]

# ── CALCULATIONS ────────────────────────────────────────────
returns = calculate_returns(prices)
signals = generate_signals(returns)
confirmed = trend_confirmation(signals)

# ── DASHBOARD ───────────────────────────────────────────────
market_summary(prices, returns)
print(f"  Returns      : {returns}")
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmed}")
print("=" * 40)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n      BACKTEST RESULTS")
print("=" * 40)
backtest(prices, signals)
