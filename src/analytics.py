"""
analytics.py
------------
Functions that calculate spending metrics and build Plotly charts.
"""

import pandas as pd
import plotly.express as px


def get_summary_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate the key financial metrics shown at the top of the dashboard.

    Returns a dictionary so app.py can display each value easily.
    """
    return {
        "total_spending": df["amount"].sum(),
        "average_transaction": df["amount"].mean(),
        "largest_transaction": df["amount"].max(),
        "most_common_merchant": df["merchant"].mode()[0],
        "top_category": df.groupby("category")["amount"].sum().idxmax(),
        "transaction_count": len(df),
    }


def spending_by_category_chart(df: pd.DataFrame):
    """Pie chart: how spending is split across categories."""
    category_totals = df.groupby("category")["amount"].sum().reset_index()

    fig = px.pie(
        category_totals,
        names="category",
        values="amount",
        title="Spending by Category",
        hole=0.4,  # donut style looks a bit more modern
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def spending_over_time_chart(df: pd.DataFrame):
    """Line chart: total spending per day."""
    daily_totals = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()
    daily_totals.columns = ["date", "amount"]

    fig = px.line(
        daily_totals,
        x="date",
        y="amount",
        title="Spending Over Time",
        markers=True,
        labels={"date": "Date", "amount": "Amount ($)"},
    )
    return fig


def top_merchants_chart(df: pd.DataFrame, top_n: int = 10):
    """Horizontal bar chart: the merchants you spend the most at."""
    merchant_totals = (
        df.groupby("merchant")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        merchant_totals,
        x="amount",
        y="merchant",
        orientation="h",
        title=f"Top {top_n} Merchants by Spending",
        labels={"amount": "Total Spent ($)", "merchant": "Merchant"},
    )
    # Show the biggest spender at the top
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def monthly_trend_chart(df: pd.DataFrame):
    """Bar chart: total spending per month."""
    monthly = df.copy()
    # Convert each date to a 'YYYY-MM' label, e.g. 2026-01
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    monthly_totals = monthly.groupby("month")["amount"].sum().reset_index()

    fig = px.bar(
        monthly_totals,
        x="month",
        y="amount",
        title="Monthly Spending Trend",
        labels={"month": "Month", "amount": "Total Spent ($)"},
    )
    return fig


def calculate_savings_plan(goal: float, current: float, target_date) -> dict:
    """
    Work out how much the user needs to save per week to hit their goal.

    Parameters:
        goal        - total savings goal in dollars
        current     - amount already saved
        target_date - the date they want to reach the goal by

    Returns a dictionary with the remaining amount, weeks left,
    and required savings per week.
    """
    remaining = max(goal - current, 0)

    # Days between today and the target date
    days_left = (pd.Timestamp(target_date) - pd.Timestamp.today()).days
    weeks_left = max(days_left / 7, 0)

    if remaining == 0:
        per_week = 0  # goal already reached!
    elif weeks_left < 1:
        per_week = remaining  # less than a week left: need it all now
    else:
        per_week = remaining / weeks_left

    return {
        "remaining": remaining,
        "weeks_left": weeks_left,
        "per_week": per_week,
    }
