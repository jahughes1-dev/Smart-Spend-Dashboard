# 💸 Smart Spend Dashboard

A fintech spending analytics dashboard built with Python and Streamlit. Upload a CSV of your transactions and instantly see where your money goes, spot suspicious charges, and plan toward a savings goal.

## Description

Smart Spend Dashboard turns a plain transaction CSV into an interactive financial dashboard. It cleans and validates your data, summarizes your spending habits with key metrics and Plotly charts, flags unusual transactions using simple rule-based detection, and includes a savings goal calculator that tells you exactly how much to set aside each week.

## Features

- **CSV upload** with validation and friendly error messages for missing columns
- **Automatic data cleaning** — parses dates, fixes amounts (handles `$` and commas), fills missing values
- **Spending summary** — total spend, average and largest transaction, top merchant and category, transaction count
- **Interactive Plotly charts** — spending by category, spending over time, top 10 merchants, monthly trend
- **Suspicious transaction detection** — rule-based flags with plain-English explanations
- **Savings goal tracker** — enter a goal, current savings, and target date to get a weekly savings plan
- **Sample dataset included** — try the app with one click, no data needed

## Tech Stack

- Python
- Streamlit (web app framework)
- Pandas (data cleaning & analysis)
- Plotly (interactive charts)

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/smart-spend-dashboard.git
cd smart-spend-dashboard

# 2. (Recommended) Create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`. Click **Use sample data** in the sidebar to explore without uploading anything.

## Sample CSV Format

Your CSV must contain these four columns:

```csv
date,merchant,amount,category
2026-03-01,Starbucks,6.45,Food & Drink
2026-03-02,Whole Foods,87.32,Groceries
2026-03-13,Best Buy,489.99,Electronics
```

A ready-to-use file, `transactions_sample.csv`, is included in this repo.

## How Suspicious Detection Works

A transaction is flagged when it matches any of these rules:

| Rule | Why it matters |
|------|----------------|
| Amount over $300 | Unusually large purchase |
| More than 3x your average transaction | Way above your normal spending pattern |
| Large charge (>$100) from a one-time merchant | Big purchase somewhere you've never shopped |

Each flagged transaction includes a `suspicious_reason` explaining exactly which rules it triggered.

## Screenshots

*Screenshots coming soon — run the app locally and add yours to the `screenshots/` folder.*

| Dashboard | Suspicious Transactions |
|-----------|------------------------|
| ![Dashboard](screenshots/dashboard.png) | ![Alerts](screenshots/alerts.png) |

## Project Structure

```
smart-spend-dashboard/
├── app.py                   # Main Streamlit app
├── transactions_sample.csv  # Sample data to try the app
├── requirements.txt         # Python dependencies
├── README.md
├── screenshots/             # App screenshots
└── src/
    ├── data_cleaning.py     # Validation & cleaning logic
    ├── analytics.py         # Metrics, charts, savings math
    └── anomaly_detection.py # Rule-based fraud flags
```

## Future Improvements

- SQLite storage so transactions persist between sessions
- Budget limits per category with alerts
- Recurring subscription detection
- Export flagged transactions to CSV/PDF
- Smarter anomaly detection (statistical or ML-based)
- Support for bank export formats (Chase, Amex, etc.)

## Resume Bullet

> Built a fintech spending analytics dashboard using Python, Pandas, Streamlit, and Plotly to analyze transaction data, visualize spending patterns, flag unusual activity, and track savings goals.
