
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FILE = PROJECT_ROOT / "data" / "processed" / "nse_five_stocks.csv"

df = pd.read_csv(FILE, parse_dates=["Date"])

print("\nNSE DATA QUALITY REPORT")
print("=" * 55)

# 1. Overall information
print("\nOVERALL DATA")
print("Total records:", len(df))
print("Companies:", df["Code"].nunique())
print("Date range:", df["Date"].min(), "to", df["Date"].max())
# Check missing values in important columns
print("\nMISSING VALUES IN KEY COLUMNS")

key_columns = [
    "Date",
    "Code",
    "Day Price",
    "Volume",
    "Adjusted Price"
]

for column in key_columns:
    print(f"{column}: {df[column].isna().sum()}")
    # Check invalid dates
print("\nINVALID DATE RECORDS:", df["Date"].isna().sum())

# 2. Records per company and year
print("\nRECORDS PER COMPANY")
print(df.groupby("Code").size())

print("\nRECORDS PER COMPANY PER YEAR")
print(
    df.groupby(
        ["Code", df["Date"].dt.year]
    ).size().unstack(fill_value=0)
)

# 3. Check duplicate records
duplicates = df.duplicated(
    subset=["Date", "Code"],
    keep=False
)

print("\nDUPLICATE DATE/CODE RECORDS:", duplicates.sum())

# 4. Check price quality
price_column = "Day Price"

print("\nPRICE QUALITY")

for code, group in df.groupby("Code"):

    prices = group[price_column]

    print(f"\n{code}")
    print("Missing prices:", prices.isna().sum())
    print("Zero prices:", (prices == 0).sum())
    print("Negative prices:", (prices < 0).sum())
    print("Minimum price:", prices.min())
    print("Maximum price:", prices.max())

# 5. Check missing volume
print("\nMISSING VOLUME VALUES")
print(df.groupby("Code")["Volume"].apply(
    lambda x: x.isna().sum()
))

# 6. Check adjusted price availability
print("\nADJUSTED PRICE AVAILABILITY")
print(df.groupby("Code")["Adjusted Price"].apply(
    lambda x: x.notna().sum()
))

# 7. Check date coverage
print("\nDATE COVERAGE PER COMPANY")

for code, group in df.groupby("Code"):
    dates = group["Date"].dropna().sort_values()

    print(
        f"{code}: {dates.min().date()} "
        f"to {dates.max().date()} "
        f"({dates.nunique()} unique dates)"
    )

print("\nQUALITY AUDIT COMPLETE")
