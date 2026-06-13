"""
anomaly_detection.py
--------------------
Simple rule-based detection of suspicious transactions.

Version 1 rules (no machine learning, just clear logic):
1. Amount over $300
2. Amount more than 3x the average transaction
3. A large transaction (over $100) from a merchant that appears only once
"""

import pandas as pd

# Thresholds used by the rules — easy to tweak in one place
LARGE_AMOUNT_THRESHOLD = 300       # Rule 1
AVERAGE_MULTIPLIER = 3             # Rule 2
ONE_TIME_MERCHANT_THRESHOLD = 100  # Rule 3


def detect_suspicious_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the three rules above and add two new columns:

    - suspicious_flag   : True/False
    - suspicious_reason : text explaining WHY it was flagged

    Returns the DataFrame with these columns added.
    """
    df = df.copy()

    avg_amount = df["amount"].mean()

    # Count how many times each merchant appears in the data
    merchant_counts = df["merchant"].value_counts()

    flags = []    # True/False for each row
    reasons = []  # explanation text for each row

    for _, row in df.iterrows():
        row_reasons = []

        # Rule 1: very large transaction
        if row["amount"] > LARGE_AMOUNT_THRESHOLD:
            row_reasons.append(f"Over ${LARGE_AMOUNT_THRESHOLD}")

        # Rule 2: much bigger than this user's typical transaction
        if row["amount"] > AVERAGE_MULTIPLIER * avg_amount:
            row_reasons.append(
                f"More than {AVERAGE_MULTIPLIER}x the average transaction "
                f"(${avg_amount:.2f})"
            )

        # Rule 3: large charge from a merchant seen only once
        is_one_time = merchant_counts[row["merchant"]] == 1
        if is_one_time and row["amount"] > ONE_TIME_MERCHANT_THRESHOLD:
            row_reasons.append("Large charge from a one-time merchant")

        flags.append(len(row_reasons) > 0)
        reasons.append("; ".join(row_reasons))

    df["suspicious_flag"] = flags
    df["suspicious_reason"] = reasons

    return df


def get_suspicious_only(df: pd.DataFrame) -> pd.DataFrame:
    """Return just the rows that were flagged, for the alert table."""
    return df[df["suspicious_flag"]].copy()
