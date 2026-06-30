def calculate_average(prices):
    total = 0

    for price in prices:
        total += price
    average = total / len(prices)
    return (round(average, 3))


prices = [124, 1232, 2323, 24234, 32534, 32534]

print("Average:", calculate_average(prices))
