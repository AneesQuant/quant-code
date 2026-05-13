# ============================================================
#   Quant Trading System — MACD Strategy
#   Author: Anees
#   Description: EMA, MACD Line, Signal Line, Histogram, Backtest
#   Day 22 — Builds on Day 20 (MA) + Day 21 (RSI)
# ============================================================


def calculate_ema(prices, span):
    """Calculate Exponential Moving Average (EMA) for a given span."""
    ema = []
    multiplier = 2 / (span + 1)
    ema.append(prices[0])                          # seed with first price
    for i in range(1, len(prices)):
        value = (prices[i] - ema[-1]) * multiplier + ema[-1]
        ema.append(round(value, 4))
    return ema


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD Line, Signal Line, and Histogram."""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = [round(f - s, 4) for f, s in zip(ema_fast, ema_slow)]
    signal_line = calculate_ema(macd_line, signal)
    histogram = [round(m - s, 4) for m, s in zip(macd_line, signal_line)]
    return macd_line, signal_line, histogram


def generate_signals(macd_line, signal_line):
    """Generate BUY/SELL/HOLD signals based on MACD crossovers."""
    signals = ["HOLD"]                             # no signal on first candle
    for i in range(1, len(macd_line)):
        prev_diff = macd_line[i-1] - signal_line[i-1]
        curr_diff = macd_line[i] - signal_line[i]

        if prev_diff < 0 and curr_diff > 0:        # MACD crosses above Signal
            signals.append("BUY")
        elif prev_diff > 0 and curr_diff < 0:      # MACD crosses below Signal
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


def momentum_score(macd_line, histogram):
    """Score momentum from latest MACD and Histogram values."""
    score = macd_line[-1]
    trend = "BULLISH" if score > 0 else "BEARISH"
    strength = "STRENGTHENING" if histogram[-1] > histogram[-2] else "WEAKENING"
    return round(score, 4), trend, strength


def backtest(prices, signals, capital=10000, risk_pct=0.02):
    """Backtest MACD signals with position sizing and performance stats."""
    position = None
    entry_price = 0
    total_profit = 0
    trades = 0
    wins = 0
    profits = []
    peak = 0
    max_drawdown = 0
    running = 0

    for i in range(len(signals)):
        signal = signals[i]
        price = prices[i]
        shares = int((capital * risk_pct) / price)

        if signal == "BUY" and position is None:
            position = "LONG"
            entry_price = price
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
                    wins,   2) if wins > 0 else 0
    avg_loss = round(sum(p for p in profits if p < 0) /
                     losses, 2) if losses > 0 else 0
    rr_ratio = round(avg_win / abs(avg_loss), 2) if avg_loss != 0 else 0

    print("=" * 45)
    print(f"  Total Trades   : {trades}")
    print(f"  Win Rate       : {win_rate}%")
    print(f"  Avg Win        : ${avg_win}")
    print(f"  Avg Loss       : ${avg_loss}")
    print(f"  Risk/Reward    : {rr_ratio}")
    print(f"  Max Drawdown   : ${round(max_drawdown, 2)}")
    print(f"  Total Profit   : ${round(total_profit, 2)}")
    print("=" * 45)


def macd_dashboard(prices, macd_line, signal_line, histogram, signals):
    """Print MACD dashboard summary."""
    score, trend, strength = momentum_score(macd_line, histogram)
    price_change = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)

    print("=" * 45)
    print("        MACD STRATEGY DASHBOARD")
    print("=" * 45)
    print(f"  Start Price    : ${prices[0]}")
    print(f"  End Price      : ${prices[-1]}")
    print(f"  Total Change   : {price_change}%")
    print(f"  MACD Score     : {score}")
    print(f"  Trend          : {trend}")
    print(f"  Momentum       : {strength}")
    print(f"  Last Signal    : {signals[-1]}")
    print("=" * 45)


# ── DATA ────────────────────────────────────────────────────
prices = [
    180, 182, 178, 185, 190, 188, 195, 197,
    201, 199, 203, 208, 205, 209, 211, 207,
    213, 210, 215, 218, 214, 220, 222, 219,
    225, 223, 228, 230, 226, 232
]

# ── CALCULATIONS ────────────────────────────────────────────
macd_line, signal_line, histogram = calculate_macd(
    prices, fast=5, slow=10, signal=3)
signals = generate_signals(macd_line, signal_line)
confirmations = trend_confirmation(signals)

# ── DASHBOARD ───────────────────────────────────────────────
macd_dashboard(prices, macd_line, signal_line, histogram, signals)
print(f"  MACD Line    : {macd_line[-5:]}")
print(f"  Signal Line  : {signal_line[-5:]}")
print(f"  Histogram    : {histogram[-5:]}")
print(f"  Signals      : {signals}")
print(f"  Confirmation : {confirmations}")
print("=" * 45)

# ── BACKTEST ─────────────────────────────────────────────────
print("\n          Backtest Results")
print("=" * 45)
backtest(prices, signals)
