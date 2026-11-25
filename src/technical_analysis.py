
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "nse_stock_metrics.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "nse_technical_indicators.csv"

df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])

df = df.sort_values(["Code", "Date"]).copy()

results = []

for code, group in df.groupby("Code"):

    group = group.copy()
    prices = group["Day Price"]

    # RSI (14 periods)
    delta = prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1/14,
        min_periods=14,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1/14,
        min_periods=14,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    group["RSI"] = 100 - (100 / (1 + rs))

        # Handle zero-loss and no-movement periods
    group.loc[
        (avg_loss == 0) & (avg_gain > 0),
        "RSI"
    ] = 100

    group.loc[
        (avg_loss == 0) & (avg_gain == 0),
        "RSI"
    ] = 50

    # MACD
    ema12 = prices.ewm(
        span=12, adjust=False, min_periods=12
    ).mean()

    ema26 = prices.ewm(
        span=26, adjust=False, min_periods=26
    ).mean()

    group["MACD"] = ema12 - ema26

    group["MACD Signal"] = group["MACD"].ewm(
        span=9, adjust=False, min_periods=9
    ).mean()

    group["MACD Histogram"] = (
        group["MACD"] - group["MACD Signal"]
    )

    # Bollinger Bands
    middle_band = prices.rolling(window=20).mean()

    standard_deviation = prices.rolling(
        window=20
    ).std(ddof=0)

    group["BB Middle"] = middle_band
    group["BB Upper"] = middle_band + (
        2 * standard_deviation
    )
    group["BB Lower"] = middle_band - (
        2 * standard_deviation
    )

    # Descriptive technical conditions
    group["Trend"] = np.where(
        group["MA20"] > group["MA50"],
        "Bullish",
        "Bearish"
    )

    group["RSI Condition"] = np.select(
        [
            group["RSI"] < 30,
            group["RSI"] > 70
        ],
        [
            "Oversold",
            "Overbought"
        ],
        default="Neutral"
    )

    group["MACD Condition"] = np.where(
        group["MACD"] > group["MACD Signal"],
        "Bullish",
        "Bearish"
    )

    results.append(group)

# Combine all companies
technical = pd.concat(results, ignore_index=True)

# Save technical indicators
technical.to_csv(OUTPUT_FILE, index=False)

# Display latest available observation for each company
print("\nNSE TECHNICAL ANALYSIS")
print("=" * 60)

latest = (
    technical.sort_values("Date")
    .groupby("Code")
    .tail(1)
    .sort_values("Code")
)

columns = [
    "Code",
    "Date",
    "Day Price",
    "MA20",
    "MA50",
    "RSI",
    "MACD",
    "MACD Signal",
    "Trend",
    "RSI Condition",
    "MACD Condition"
]

print("\nLATEST TECHNICAL INDICATORS")
print(latest[columns].to_string(index=False))

print("\nSAVED TO:", OUTPUT_FILE)
print("\nTECHNICAL ANALYSIS COMPLETE")
