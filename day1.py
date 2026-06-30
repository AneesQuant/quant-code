prices = [180, 182, 178, 185]

for i in range(1, len(prices)):
    change = prices[i] - prices[i-1]
    pct_change = (change / prices[i-1]) * 100

    print("Change:", change, "| %:", round(pct_change, 2))
