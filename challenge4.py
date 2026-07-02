def calculate_returns(prices):
    returns = []

    for i in range(1, len(prices)):
        pct_change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(pct_change)

    return returns


def generate_signal(returns):
    signals = []

    for r in returns:
        if r > 2:
            signals.append("BUY")
        elif r < -2:
            signals.append("SELL")
        else:
            signals.append("HOLD")

    return signals


def trend_confirmation(signals):
    confirmations = []

    for i in range(1, len(signals)):
        if signals[i] == "BUY" and signals[i-1] == "BUY":
            confirmations.append("LONG TREND CONFIRMED")
        elif signals[i] == "SELL" and signals[i-1] == "SELL":
            confirmations.append("SHORT TREND CONFIRMED")
        else:
            confirmations.append("NO CONFIRMATION")

    return confirmations


prices = [100, 103, 105, 104, 101, 104, 105.5, 106, 108, 107]


returns = calculate_returns(prices)

signals = generate_signal(returns)


confirmation = trend_confirmation(signals)

print("Returns:", [round(r, 2)for r in returns])

print("Signals:", signals)

print("Trend Confirmation", confirmation)
