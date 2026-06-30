# ============================================================
#   Quant Trading System — Basic Signal & Backtest Engine
#   Author: Anees
#   Description: Price returns, signal generation, backtesting
# ============================================================


def calculate_returns(prices):
    """Calculate percentage returns between each price."""
    returns = []
    for i in range(1, len(prices)):
        pct_change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100
        returns.append(round(pct_change, 2))
    return returns


def calculate_volatility(returns):
    """Calculate volatility as standard deviation of returns."""
    avg = sum(returns) / len(returns)
    variance = sum((r - avg) ** 2 for r in returns) / (len(returns) - 1)
    return round(variance ** 0.5, 4)


def momentum_score(prices, window=5):
    """Calculate momentum: latest price vs price N days ago."""
    score = round(((prices[-1] - prices[-window]) / prices[-window]) * 100, 2)
    return score, "BULLISH" if score > 0 else "BEARISH"


def moving_average(prices, window=5):
    """Calculate simple moving average over a given window."""
    return round(sum(prices[-window:]) / window, 2)


def calculate_rsi(prices, period=14):
    """RSI: above 70 overbought, below 30 oversold."""
    gains = [max(prices[i]-prices[i-1], 0) for i in range(1, len(prices))]
    losses = [abs(min(prices[i]-prices[i-1], 0))
              for i in range(1, len(prices))]
    ag, al = sum(gains[-period:]) / period, sum(losses[-period:]) / period
    if al == 0:
        return 100, "OVERBOUGHT"
    rsi = round(100 - (100 / (1 + ag / al)), 2)
    return rsi, "OVERBOUGHT" if rsi > 70 else "OVERSOLD" if rsi < 30 else "NEUTRAL"


def generate_signals(returns, buy_threshold=1.0, sell_threshold=-1.0):
    """Generate BUY, SELL, or HOLD signals based on return thresholds."""
    signals = []
    for r in returns:
        if r > buy_threshold:
            signals.append("BUY")
        elif r < sell_threshold:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def trend_confirmation(signals):
    """Confirm trend if two consecutive signals match."""
    confirmed = []
    for i in range(1, len(signals)):
        if signals[i] == "BUY" and signals[i-1] == "BUY":
            confirmed.append("LONG CONFIRMED")
        elif signals[i] == "SELL" and signals[i-1] == "SELL":
            confirmed.append("SELL CONFIRMED")
        else:
            confirmed.append("NO CONFIRMATION")
    return confirmed


def backtest(prices, signals, capital=10000, risk_pct=0.02):
    """Backtest with position sizing and performance stats."""
    position, entry_price, total_profit = None, 0, 0
    trades, wins, profits = 0, 0, []
    peak, max_drawdown, running = 0, 0, 0

    for i in range(len(signals)):
        signal = signals[i]
        price = prices[i + 1]
        shares = int((capital * risk_pct) / price)

        if signal == "BUY" and position is None:
            position, entry_price = "LONG", price
            print(f"  BUY  at ${entry_price} | Shares: {shares}")

        elif signal == "SELL" and position == "LONG":
            profit = (price - entry_price) * shares
            total_profit += profit
            trades += 1
            profits.append(round(profit, 2))
            if profit > 0:
                wins += 1
            print(f"  SELL at ${price:<6} | Profit: ${round(profit, 2)}")
            position = None
            running += profit
            if running > peak:
                peak = running
            if (peak - running) > max_drawdown:
                max_drawdown = peak - running

    win_rate = round((wins / trades) * 100, 2) if trades > 0 else 0
    losses = trades - wins
    avg_win = round(sum(p for p in profits if p > 0) /
                    wins, 2) if wins > 0 else 0
    avg_loss = round(sum(p for p in profits if p < 0) /
                     losses, 2) if losses > 0 else 0

    print("=" * 45)
    print(f"  Total Trades   : {trades}")
    print(f"  Win Rate       : {win_rate}%")
    print(f"  Avg Win        : ${avg_win}")
    print(f"  Avg Loss       : ${avg_loss}")
    print(
        f"  Risk/Reward    : {round(avg_win/abs(avg_loss), 2) if avg_loss != 0 else 0}")
    print(f"  Max Drawdown   : ${round(max_drawdown, 2)}")
    print(f"  Total Profit   : ${round(total_profit, 2)}")
    print("=" * 45)


def market_summary(prices, returns):
    """Print dashboard with volatility, momentum, MA and RSI."""
    score, trend = momentum_score(prices)
    rsi, label = calculate_rsi(prices)
    print("=" * 45)
    print("        QUANT TRADING DASHBOARD")
    print("=" * 45)
    print(f"  Start Price    : ${prices[0]}")
    print(f"  End Price      : ${prices[-1]}")
    print(
        f"  Total Change   : {round(((prices[-1]-prices[0])/prices[0])*100, 2)}%")
    print(f"  Volatility     : {calculate_volatility(returns)}%")
    print(f"  Momentum       : {score}% ({trend})")
    print(f"  5-Day MA       : ${moving_average(prices)}")
    print(f"  RSI            : {rsi} ({label})")
    print("=" * 45)


# ── DATA ────────────────────────────────────────────────────
prices = [180, 182, 178, 185, 190, 188, 195,
          197, 201, 199, 203, 208, 205, 209, 211]

# ── CALCULATIONS ────────────────────────────────────────────
returns = calculate_returns(prices)
signals = generate_signals(returns)
confirmations = trend_confirmation(signals)

# ── DASHBOARD ───────────────────────────────────────────────
market_summary(prices, returns)
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmations}")
print("=" * 45)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n          Backtest Results")
print("=" * 45)
backtest(prices, signals)
