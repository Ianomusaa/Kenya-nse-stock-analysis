
from pathlib import Path
import pandas as pd
import numpy as np

# File locations
# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "nse_five_stocks.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "nse_stock_metrics.csv"

# Load cleaned data
df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])

# Sort chronologically within each company
df = df.sort_values(["Code", "Date"]).copy()

# Ensure prices are numeric
df["Day Price"] = pd.to_numeric(
    df["Day Price"], errors="coerce"
)

# Calculate metrics separately for each company
results = []

for code, group in df.groupby("Code"):

    group = group.copy()
    group = group.sort_values("Date")

    prices = group["Day Price"]

    # Daily percentage returns
    group["Daily Return"] = prices.pct_change()

    # Cumulative price return
    group["Cumulative Return"] = (
        prices / prices.iloc[0]
    ) - 1

    # Moving averages
    group["MA20"] = prices.rolling(window=20).mean()
    group["MA50"] = prices.rolling(window=50).mean()

    # Running peak and drawdown
    running_peak = prices.cummax()

    group["Drawdown"] = (
        prices / running_peak
    ) - 1

    results.append(group)

# Combine all companies
metrics = pd.concat(results, ignore_index=True)

# Save detailed metrics
metrics.to_csv(OUTPUT_FILE, index=False)


# Annual performance summary
metrics["Year"] = metrics["Date"].dt.year

# Last available price for each company in each year
year_end_prices = (
    metrics.groupby(["Code", "Year"])["Day Price"].last()
)

# Calculate returns against the previous year-end price
annual_returns = year_end_prices.groupby(
    level="Code"
).pct_change()

# Calculate 2023 observed-period return separately
first_year_prices = (
    metrics.groupby(["Code", "Year"])["Day Price"].first()
)

for code in metrics["Code"].unique():

    first_price = first_year_prices.loc[(code, 2023)]
    last_price = year_end_prices.loc[(code, 2023)]

    annual_returns.loc[(code, 2023)] = (
        last_price / first_price
    ) - 1

# Display annual returns
annual_returns_table = (
    annual_returns.unstack().mul(100).round(2)
)

print("\nANNUAL AND YEAR-TO-DATE RETURNS (%)")
print(annual_returns_table)

# Annualised volatility
volatility = (
    metrics.groupby("Code")["Daily Return"].std()
    * np.sqrt(252)
)

# Maximum drawdown
max_drawdown = (
    metrics.groupby("Code")["Drawdown"].min()
)

print("\nANNUALISED VOLATILITY (%)")
print((volatility * 100).round(2))

print("\nMAXIMUM DRAWDOWN (%)")
print((max_drawdown * 100).round(2))

print("\nSAVED TO:", OUTPUT_FILE)
print("\nMETRICS CALCULATION COMPLETE")
