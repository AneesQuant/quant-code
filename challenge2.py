# Position Summary
ticker = "TSLA"
shares = 100
buy_price = 214.00
raw_price = "279.45"
is_long = True


# Type demonstration
print("===== Position Summary =====")
print("Ticker:",          ticker)
print(
    f"Type checks:  {type(ticker)} {type(buy_price)} {type(shares)} {type(is_long)}")


# Type conversing: string > float
current_price = float(raw_price)
print(f'Raw price:   "{raw_price}"  > {current_price}  (float)')
print("---")


# Calculations
cost_basis = shares * buy_price
market_value = shares * current_price
pnl = market_value - cost_basis
pct_return = (pnl / cost_basis) * 100


# Output
print(f"Shares:        {shares}")
print(f"Buy price:    ${buy_price}")
print(f"Current:      ${current_price}")
print(f"Cost basis:   ${cost_basis}")
print(f"Market value: ${market_value} ")
print(f"P&L:          ${pnl}")
print(f"Return:         {round(pct_return, 1)} %")
print("==============================")
