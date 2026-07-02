def calculate_returns(prices):
    returns = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        pct_change = (change / prices[i-1]) * 100
        returns.append(round(pct_change, 2))

    return returns


def find_max(prices):
    highest = max(prices)
    return highest


def find_min(prices):
    lowest = min(prices)
    return lowest


def calculate_average(prices):
    total = 0

    for price in prices:
        total += price
    average = total / len(prices)
    return average


prices = [180, 182, 178, 185]

print("Highest Price:", find_max(prices))

print("Lowest Price:", find_min(prices))

print("Average:", calculate_average(prices))

print("Returns:", calculate_returns(prices))
