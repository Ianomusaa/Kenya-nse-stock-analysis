# Kenya NSE Stock Analysis

A Python project analysing historical stock price data from five companies listed on the Nairobi Securities Exchange (NSE).

The project combines data collection, cleaning, financial calculations, technical indicators and visualisation into one automated workflow.

## Companies Analysed

| Ticker | Company |
|---|---|
| SCOM | Safaricom |
| EQTY | Equity Group |
| KCB | KCB Group |
| EABL | East African Breweries |
| COOP | Co-operative Bank |

**Data period:** January 2023 – June 2026

## What the Project Does

- Combines and cleans historical NSE datasets.
- Checks data quality, missing values and duplicate records.
- Calculates daily returns, annual returns and cumulative returns.
- Measures annualised volatility and maximum drawdown.
- Calculates moving averages, RSI, MACD and Bollinger Bands.
- Generates charts to compare stock performance and price trends.

## Tools

Python · Pandas · NumPy · Matplotlib · Seaborn

## Project Structure

```text
├── charts/       # Generated visualisations
├── data/
│   ├── raw/      # Original datasets
│   └── processed/# Cleaned and analysed data
├── reports/
├── src/          # Analysis scripts
├── main.py       # Runs the complete workflow
└── requirements.txt
```

## Run the Project

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Place the source CSV datasets in `data/raw/` before running the project.

## Data Sources

Historical NSE datasets from Mendeley Data:

- [2023–2024 dataset](https://doi.org/10.17632/ss5pfw8xnk.3)
- [2025 dataset](https://doi.org/10.17632/2b63rx67xt.2)
- [2026 dataset](https://doi.org/10.17632/hvmhnp7f9r.1)

Original data contributed by Barack Wanjawa, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Limitations

The dataset ends on 30 June 2026. Adjusted prices are unavailable, so returns do not include dividends. Three EABL volume observations are missing. The analysis is historical and descriptive, not a price prediction.

## About

Built as a hands-on Python project to explore financial data processing and stock market analysis using Kenyan market data.