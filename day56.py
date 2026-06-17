# ============================================================
#   Quant Trading System — MACD + RSI Combined Strategy
#   Author: Anees
#   Description: MACD crossover filtered by RSI confirmation
# ============================================================


def calculate_ema(prices, span):
    """Exponential Moving Average — weights recent prices more."""
    ema = [prices[0]]
    k = 2 / (span + 1)
    for p in prices[1:]:
        ema.append(round((p - ema[-1]) * k + ema[-1], 4))
    return ema


def calculate_macd(prices, fast=5, slow=10, signal=3):
    """MACD Line = Fast EMA - Slow EMA | Signal = EMA of MACD."""
    macd_line = [round(
        f-s, 4) for f, s in zip(calculate_ema(prices, fast), calculate_ema(prices, slow))]
    signal_line = calculate_ema(macd_line, signal)
    histogram = [round(m-s, 4) for m, s in zip(macd_line, signal_line)]
    return macd_line, signal_line, histogram


def calculate_rsi(prices, period=7):
    """RSI — above 70 = overbought, below 30 = oversold."""
    rsi = [None] * period
    for i in range(period, len(prices)):
        w = prices[i-period:i]
        gains = [max(w[j]-w[j-1], 0) for j in range(1, len(w))]
        losses = [abs(min(w[j]-w[j-1], 0)) for j in range(1, len(w))]
        rs = (sum(gains)/len(gains)) / \
            (sum(losses)/len(losses)) if sum(losses) else 0
        rsi.append(round(100 - (100 / (1 + rs)), 2))
    return rsi


def generate_signals(macd_line, signal_line, rsi, ob=70, os_=30):
    """BUY = MACD crosses up + RSI not overbought. SELL = opposite."""
    signals = ["HOLD"]
    for i in range(1, len(macd_line)):
        prev = macd_line[i-1] - signal_line[i-1]
        curr = macd_line[i] - signal_line[i]
        r = rsi[i]
        if r is None:
            signals.append("HOLD")
        elif prev < 0 and curr > 0 and r < ob:
            signals.append("BUY")
        elif prev > 0 and curr < 0 and r > os_:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def trend_confirmation(signals):
    """Confirm trend if two consecutive signals match."""
    confirmed = []
    for i in range(1, len(signals)):
        if signals[i] == signals[i-1] == "BUY":
            confirmed.append("LONG CONFIRMED")
        elif signals[i] == signals[i-1] == "SELL":
            confirmed.append("SELL CONFIRMED")
        else:
            confirmed.append("NO CONFIRMATION")
    return confirmed


def backtest(prices, signals, capital=10000, risk_pct=0.02):
    """Backtest with position sizing, win rate, drawdown, and R/R ratio."""
    position = entry = total = trades = wins = running = peak = max_dd = 0
    profits = []

    for i in range(len(signals)):
        price = prices[i]
        shares = int((capital * risk_pct) / price)

        if signals[i] == "BUY" and not position:
            position, entry = 1, price
            print(f"  BUY  at ${entry} | Shares: {shares}")

        elif signals[i] == "SELL" and position:
            profit = (price - entry) * shares
            total += profit
            trades += 1
            profits.append(round(profit, 2))
            wins += profit > 0
            print(f"  SELL at ${price:<6} | Profit: ${round(profit, 2)}")
            position = 0
            running += profit
            if running > peak:
                peak = running
            if (peak - running) > max_dd:
                max_dd = peak - running

    losses = trades - wins
    avg_win = round(sum(p for p in profits if p > 0) /
                    wins,   2) if wins else 0
    avg_loss = round(sum(p for p in profits if p < 0) /
                     losses, 2) if losses else 0
    print("=" * 45)
    print(f"  Total Trades   : {trades}")
    print(f"  Win Rate       : {round(wins/trades*100, 2) if trades else 0}%")
    print(f"  Avg Win        : ${avg_win}")
    print(f"  Avg Loss       : ${avg_loss}")
    print(
        f"  Risk/Reward    : {round(avg_win/abs(avg_loss), 2) if avg_loss else 0}")
    print(f"  Max Drawdown   : ${round(max_dd, 2)}")
    print(f"  Total Profit   : ${round(total, 2)}")
    print("=" * 45)


def market_summary(prices, macd_line, rsi, signals):
    """Print MACD + RSI combined dashboard."""
    rsi_val = rsi[-1]
    rsi_status = "OVERBOUGHT" if rsi_val > 70 else "OVERSOLD" if rsi_val < 30 else "NEUTRAL"
    print("=" * 45)
    print("     MACD + RSI COMBINED DASHBOARD")
    print("=" * 45)
    print(f"  Start Price    : ${prices[0]}")
    print(f"  End Price      : ${prices[-1]}")
    print(
        f"  Total Change   : {round((prices[-1]-prices[0])/prices[0]*100, 2)}%")
    print(
        f"  MACD Trend     : {'BULLISH' if macd_line[-1] > 0 else 'BEARISH'}")
    print(f"  RSI Value      : {rsi_val} ({rsi_status})")
    print(f"  Last Signal    : {signals[-1]}")
    print("=" * 45)


# ── DATA ────────────────────────────────────────────────────
prices = [180, 182, 178, 185, 190, 188, 195, 197,
          201, 199, 203, 208, 205, 209, 211, 207,
          213, 210, 215, 218, 214, 220, 222, 219,
          225, 223, 228, 230, 226, 232]

# ── CALCULATIONS ────────────────────────────────────────────
macd_line, signal_line, histogram = calculate_macd(prices)
rsi = calculate_rsi(prices)
signals = generate_signals(macd_line, signal_line, rsi)
confirmations = trend_confirmation(signals)

# ── DASHBOARD ───────────────────────────────────────────────
market_summary(prices, macd_line, rsi, signals)
print(f"  RSI Values   : {rsi[-5:]}")
print(f"  MACD Line    : {macd_line[-5:]}")
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmations}")
print("=" * 45)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n          Backtest Results")
print("=" * 45)
backtest(prices, signals)