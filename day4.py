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
        elif r < 1:
            signals.append("SELL")
        else:
            signals.append("HOLD")

    return signals


prices = [180, 182, 178, 185]

returns = calculate_returns(prices)

signals = generate_signals(returns)

print("Returns:", [round(r, 2) for r in returns])
print("signals:", signals)
