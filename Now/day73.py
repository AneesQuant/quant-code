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
            confirmations.append("SELL CONFIRMED")
        else:
            confirmations.append("NO CONFIRMATION")
    return confirmations


def backtest(prices, signals):
    position = None
    entry_price = 0
    total_profit = 0

    for i in range(len(signals)):
        signal = signals[i]
        price = prices[i+1]
        shares = 15343

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
            print("BUY at $", entry_price)

        elif signal == "SELL" and position == "LONG":
            net_profit = (price - entry_price) * shares
            total_profit += net_profit
            print("SELL at $", price, "| Profit $", net_profit)
            position = None

    print("=" * 40)
    print("Total Profit: $", total_profit)
    print("=" * 40)


def market_summary(prices, returns):
    print("=" * 40)
    print("            TRADING DASHBOARD")
    print("=" * 40)
    print("Highest Price:    $", max(prices))
    print("Lowest Price:     $", min(prices))
    print("Average Price:    $", round(sum(prices) / len(prices), 2))
    print("Best Return:      ", max(returns), "%")
    print("Worst Return:     ", min(returns), "%")
    print("=" * 40)


# ── DATA ────────────────────────────────────────────────────
prices = [180, 182, 178, 185, 190, 188, 195,
          197, 201, 199, 203, 208, 205, 209, 211]

# ── CALCULATIONS ────────────────────────────────────────────
returns = calculate_returns(prices)
signals = generate_signals(returns)
confirmations = trend_confirmation(signals)

# ── DASHBOARD ───────────────────────────────────────────────
market_summary(prices, returns)
print("Returns         ", returns)
print("Signals         ", signals)
print("Confirmations   ", confirmations)
print("=" * 40)

# ── BACKTEST ─────────────────────────────────────────────────
print("         BACKTEST RESULTS")
backtest(prices, signals)