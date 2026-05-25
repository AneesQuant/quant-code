# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================

def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        pct_change = (change / prices[i-1]) * 100
        returns.append(round(pct_change, 2))
    return returns

<<<<<<< HEAD

=======
>>>>>>> 10706d0f65feaed2a86f470cda3dfea9e1804de8
def find_max(prices):
    highest = max(prices)
    return highest

<<<<<<< HEAD

=======
>>>>>>> 10706d0f65feaed2a86f470cda3dfea9e1804de8
def find_min(prices):
    lowest = min(prices)
    return lowest

<<<<<<< HEAD

=======
>>>>>>> 10706d0f65feaed2a86f470cda3dfea9e1804de8
def calculate_average(prices):
    total = 0
    for price in prices:
        total += price
    average = total / len(prices)
    return average

<<<<<<< HEAD

=======
>>>>>>> 10706d0f65feaed2a86f470cda3dfea9e1804de8
prices = [180, 182, 178, 185]
print("Highest Price:", find_max(prices))
print("Lowest Price:", find_min(prices))
print("Average:", calculate_average(prices))
<<<<<<< HEAD
print("Returns:", calculate_returns(prices))
=======
print("Returns:", calculate_returns(prices))
>>>>>>> 10706d0f65feaed2a86f470cda3dfea9e1804de8
