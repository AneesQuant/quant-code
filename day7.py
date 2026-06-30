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

    for i in range(len(signals)):
        signal = signals[i]
        price = prices[i + 1]

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
            print("BUY at $", entry_price)

        elif signal == "SELL" and position == "LONG":
            profit = price - entry_price
            total_profit += profit
            print("SELL at $", price, "| Profit: $", round(profit, 2))
            position = None

    print("=" * 40)
    print("Total Profit: $", round(total_profit, 2))
    print("=" * 40)


def market_summary(prices, returns):
    print("=" * 40)
    print("      QUANT TRADING DASHBOARD")
    print("=" * 40)
    print("Highest Price:  $", max(prices))
    print("Lowest Price:   $", min(prices))
    print("Average Price:  $", round(sum(prices) / len(prices), 2))
    print("Best Return:    ", max(returns), "%")
    print("Worst Return:   ", min(returns), "%")
    print("=" * 40)


# DATA
prices = [180, 182, 178, 185, 190, 188, 195,
          197, 201, 199, 203, 208, 205, 209, 211]

# CALCULATIONS
returns = calculate_returns(prices)
signals = generate_signals(returns)
confirmed = trend_confirmation(signals)

# PRINT DASHBOARD
market_summary(prices, returns)
print("Returns:      ", returns)
print("Signals:      ", signals)
print("Confirmation: ", confirmed)
print("=" * 40)

# BACKTEST
print("      BACKTEST RESULTS")
backtest(prices, signals)
