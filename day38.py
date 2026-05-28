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
    confirmations = []
    for i in range(1, len(signals)):
        if signals[i] == "BUY" and signals[i-1] == "BUY":
            confirmations.append("LONG CONFIRMED")
        elif signals[i] == "SELL" and signals[i-1] == "SELL":
            confirmations.append("SHORT CONFIRMED")
        else:
            confirmations.append("NO CONFIRMATION")
    return confirmations


def backtest_with_risk(prices, signals):
    capital = 100000
    risk_per_trade = 0.02
    position = None
    entry_price = 0

    for i in range(len(signals)):
        signal = signals[i]
        price = prices[i + 1]
        risk_amount = capital * risk_per_trade

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
            print(f"  BUY  at ${entry_price}")

        elif signal == "SELL" and position == "LONG":
            profit_per_unit = price - entry_price
            position_size = risk_amount / entry_price
            profit = profit_per_unit * position_size
            capital += profit
            print(
                f"  SELL at ${price} | Profit: ${round(profit, 2)} | Capital: ${round(capital, 2)}")
            position = None

    print("=" * 45)
    print(f"  Final Capital : ${round(capital, 2)}")
    print("=" * 45)


def market_summary(prices, returns):
    print("=" * 45)
    print("         TRADING DASHBOARD")
    print("=" * 45)
    print(f"  Highest Price : ${max(prices)}")
    print(f"  Lowest Price  : ${min(prices)}")
    print(f"  Average Price : ${round(sum(prices) / len(prices), 2)}")
    print(f"  Best Return   : {max(returns)}%")
    print(f"  Worst Return  : {min(returns)}%")
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
print(f"  Returns       : {returns}")
print(f"  Signals       : {signals}")
print(f"  Confirmations : {confirmations}")
print("=" * 45)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n         BACKTEST RESULTS")
print("=" * 45)
backtest_with_risk(prices, signals)
