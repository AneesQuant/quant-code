# Calculating Returns

def calculate_returns(prices):
    returns = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        pct_change = (change / prices[i-1]) * 100
        returns.append(round(pct_change, 2))

    return returns

# Calculating average


def calculate_average(prices):
    total = 0

    for price in prices:
        total += price
    average = total / len(prices)

    return average

# Calculate Highest Price


def calculate_highest(prices):
    Highest = max(prices)
    return Highest

# Calculate Lowest Price


def calculate_lowest(prices):
    Lowest = min(prices)
    return Lowest


prices = [123, 543, 654, 765, 234, 245]

print("Returns:", calculate_returns(prices))

print("Highest price:", calculate_highest(prices))

print("Lowest:", calculate_lowest(prices))

print("Average:", (round(calculate_average(prices), 2)))
