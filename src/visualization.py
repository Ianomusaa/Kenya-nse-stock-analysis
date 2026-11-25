
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "nse_technical_indicators.csv"
CHART_DIR = PROJECT_ROOT / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
df = df.sort_values(["Code", "Date"]).copy()

# Chart appearance
sns.set_theme(style="whitegrid")

STOCKS = ["COOP", "EABL", "EQTY", "KCB", "SCOM"]


# 1. Historical stock prices
def plot_stock_prices():

    plt.figure(figsize=(13, 7))

    for code in STOCKS:

        stock = df[df["Code"] == code]

        plt.plot(
            stock["Date"],
            stock["Day Price"],
            label=code
        )

    plt.title("NSE Stock Price History (2023–June 2026)")
    plt.xlabel("Date")
    plt.ylabel("Share Price (KES)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(CHART_DIR / "stock_price_history.png", dpi=300)
    plt.close()


# 2. Cumulative returns
def plot_cumulative_returns():

    plt.figure(figsize=(13, 7))

    for code in STOCKS:

        stock = df[df["Code"] == code]

        plt.plot(
            stock["Date"],
            stock["Cumulative Return"] * 100,
            label=code
        )

    plt.axhline(0, linestyle="--", linewidth=1)

    plt.title("Cumulative Price Returns Comparison")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(CHART_DIR / "cumulative_returns.png", dpi=300)
    plt.close()


# 3. Annual returns
def plot_annual_returns():

    yearly_prices = (
        df.groupby(["Code", df["Date"].dt.year])["Day Price"]
        .agg(["first", "last"])
    )

    annual_returns = (
        yearly_prices.groupby(level="Code")["last"].pct_change()
    )

    first_prices = (
        df.groupby(["Code", df["Date"].dt.year])["Day Price"].first()
    )

    for code in STOCKS:

        annual_returns.loc[(code, 2023)] = (
            yearly_prices.loc[(code, 2023), "last"] /
            first_prices.loc[(code, 2023)]
        ) - 1

    annual_returns = annual_returns.unstack() * 100
    annual_returns = annual_returns.rename(
    columns={2026: "2026 YTD (to June 30)"}
)

    annual_returns.plot(
        kind="bar",
        figsize=(13, 7)
    )

    plt.title("Annual and Year-to-Date Price Returns")
    plt.xlabel("Company")
    plt.ylabel("Return (%)")
    plt.xticks(rotation=0)
    plt.legend(title="Year")
    plt.tight_layout()

    plt.savefig(CHART_DIR / "annual_returns.png", dpi=300)
    plt.close()


# 4. Moving averages
def plot_moving_averages():

    for code in STOCKS:

        stock = df[df["Code"] == code].copy()

        plt.figure(figsize=(13, 7))

        plt.plot(
            stock["Date"],
            stock["Day Price"],
            label="Share Price",
            alpha=0.6
        )

        plt.plot(
            stock["Date"],
            stock["MA20"],
            label="20-Day Moving Average"
        )

        plt.plot(
            stock["Date"],
            stock["MA50"],
            label="50-Day Moving Average"
        )

        plt.title(f"{code} - Share Price and Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Share Price (KES)")
        plt.legend()
        plt.tight_layout()

        plt.savefig(
            CHART_DIR / f"{code.lower()}_moving_averages.png",
            dpi=300
        )

        plt.close()


# 5. RSI comparison
def plot_rsi():

    plt.figure(figsize=(13, 7))

    for code in STOCKS:

        stock = df[df["Code"] == code]

        plt.plot(
            stock["Date"],
            stock["RSI"],
            label=code
        )

    plt.axhline(70, color="red", linestyle="--", label="Overbought (70)")
    plt.axhline(30, color="green", linestyle="--", label="Oversold (30)")

    plt.title("Relative Strength Index (RSI)")
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()

    plt.savefig(CHART_DIR / "rsi_comparison.png", dpi=300)
    plt.close()


# Run all visualisations
if __name__ == "__main__":

    plot_stock_prices()
    plot_cumulative_returns()
    plot_annual_returns()
    plot_moving_averages()
    plot_rsi()

    print("\nVISUALISATIONS COMPLETE")
    print("=" * 50)

    for chart in sorted(CHART_DIR.glob("*.png")):
        print(chart)
