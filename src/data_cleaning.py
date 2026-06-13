"""
data_cleaning.py
----------------
Functions for validating and cleaning the uploaded transaction data.

The dashboard expects a CSV with these columns:
    date, merchant, amount, category
"""

import pandas as pd

# The columns every uploaded CSV must contain
REQUIRED_COLUMNS = ["date", "merchant", "amount", "category"]


def validate_columns(df: pd.DataFrame) -> list:
    """
    Check that the DataFrame has all required columns.

    Returns a list of missing column names (empty list = all good).
    """
    # Normalize column names: lowercase + strip spaces so "Date " still works
    df.columns = df.columns.str.strip().str.lower()

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the transaction data.

    Steps:
    1. Normalize column names
    2. Convert 'date' to datetime (bad dates become NaT and are dropped)
    3. Convert 'amount' to numeric (bad values become NaN and are dropped)
    4. Fill missing merchant/category values with 'Unknown'
    5. Strip extra whitespace from text columns

    Returns the cleaned DataFrame.
    """
    # Work on a copy so we never modify the original upload
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # --- 1. Dates: convert to datetime, drop rows we can't parse ---
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # --- 2. Amounts: remove $ and commas, convert to number ---
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    # Spending should be positive; use absolute value just in case
    df["amount"] = df["amount"].abs()

    # --- 3. Text columns: fill missing values and tidy whitespace ---
    for col in ["merchant", "category"]:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
        # Empty strings also count as missing
        df[col] = df[col].replace("", "Unknown")

    # --- 4. Sort by date and reset the index ---
    df = df.sort_values("date").reset_index(drop=True)

    return df
