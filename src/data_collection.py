
from pathlib import Path
import pandas as pd

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Five target NSE companies
TARGET_STOCKS = {
    "SCOM": "Safaricom",
    "EQTY": "Equity Group",
    "KCB": "KCB Group",
    "EABL": "East African Breweries",
    "COOP": "Co-operative Bank",
}

# Find CSV files
csv_files = sorted(RAW_FOLDER.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in data/raw")

# Load and combine all datasets
dataframes = []

for file in csv_files:
    print(f"Reading: {file.name}")

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    dataframes.append(df)

all_data = pd.concat(dataframes, ignore_index=True)

print("\nTOTAL RAW RECORDS:", len(all_data))

# Standardise stock codes
all_data["Code"] = (
    all_data["Code"].astype(str).str.strip().str.upper()
)

# Convert dates
all_data["Date"] = pd.to_datetime(
    all_data["Date"],
    format="%d-%b-%y",
    errors="coerce"
)

# Select our five companies
all_data = all_data[
    all_data["Code"].isin(TARGET_STOCKS.keys())
].copy()

# Add company names from our mapping
all_data["Company"] = all_data["Code"].map(TARGET_STOCKS)

# Convert numeric columns
numeric_columns = [
    "Day Low",
    "Day High",
    "Day Price",
    "Previous",
    "Volume",
    "Adjusted Price",
]

for column in numeric_columns:
    all_data[column] = pd.to_numeric(
        all_data[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .replace("-", pd.NA),
        errors="coerce"
    )

# Remove records without valid dates
all_data = all_data.dropna(subset=["Date"])

# Remove duplicate date and stock combinations
all_data = all_data.drop_duplicates(
    subset=["Date", "Code"],
    keep="first"
)

# Sort records
all_data = all_data.sort_values(
    ["Code", "Date"]
).reset_index(drop=True)

# Save cleaned data
output_file = OUTPUT_FOLDER / "nse_five_stocks.csv"

all_data.to_csv(output_file, index=False)

# Summary
print("\nDATA COLLECTION COMPLETE")
print("=" * 50)

print("TOTAL CLEANED RECORDS:", len(all_data))
print("START DATE:", all_data["Date"].min())
print("END DATE:", all_data["Date"].max())

print("\nRECORDS PER STOCK:")
print(all_data.groupby("Code").size())

print("\nMISSING DAY PRICE VALUES:")
print(all_data.groupby("Code")["Day Price"].apply(
    lambda x: x.isna().sum()
))

print("\nSAVED TO:", output_file)
