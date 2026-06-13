"""
Smart Spend Dashboard
---------------------
A fintech spending analytics dashboard built with Streamlit.

Run it locally with:
    streamlit run app.py
"""

from datetime import date, timedelta

import pandas as pd
import streamlit as st

# Our own modules from the src folder
from src.data_cleaning import validate_columns, clean_data
from src.analytics import (
    get_summary_metrics,
    spending_by_category_chart,
    spending_over_time_chart,
    top_merchants_chart,
    monthly_trend_chart,
    calculate_savings_plan,
)
from src.anomaly_detection import detect_suspicious_transactions, get_suspicious_only

# ---------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Smart Spend Dashboard",
    page_icon="💸",
    layout="wide",
)

st.title("💸 Smart Spend Dashboard")
st.caption("Upload your transactions and understand your spending in seconds.")

# ---------------------------------------------------------------
# Sidebar: CSV upload
# ---------------------------------------------------------------
st.sidebar.header("📂 Upload Transactions")
st.sidebar.write("Your CSV needs these columns: `date`, `merchant`, `amount`, `category`")

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.write("No file? Try the included **transactions_sample.csv**.")
use_sample = st.sidebar.button("Use sample data")

# ---------------------------------------------------------------
# Load the data (uploaded file or sample)
# ---------------------------------------------------------------
df_raw = None

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
elif use_sample or st.session_state.get("using_sample", False):
    st.session_state["using_sample"] = True  # remember across reruns
    df_raw = pd.read_csv("transactions_sample.csv")

if df_raw is None:
    # Friendly landing state before any data is loaded
    st.info("👈 Upload a CSV in the sidebar (or click **Use sample data**) to get started.")
    st.stop()

# ---------------------------------------------------------------
# Validate and clean
# ---------------------------------------------------------------
missing_cols = validate_columns(df_raw)
if missing_cols:
    st.error(
        f"❌ Your CSV is missing these required columns: **{', '.join(missing_cols)}**. "
        "Expected columns: date, merchant, amount, category."
    )
    st.stop()

df = clean_data(df_raw)

if df.empty:
    st.error("❌ No valid rows found after cleaning. Check your dates and amounts.")
    st.stop()

rows_dropped = len(df_raw) - len(df)
if rows_dropped > 0:
    st.warning(f"⚠️ {rows_dropped} row(s) with invalid dates or amounts were removed.")

# Run anomaly detection once, up front
df = detect_suspicious_transactions(df)

# ---------------------------------------------------------------
# Section 1: Key metrics
# ---------------------------------------------------------------
st.header("📊 Spending Summary")

metrics = get_summary_metrics(df)

# Two rows of three metric cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Spending", f"${metrics['total_spending']:,.2f}")
col2.metric("Average Transaction", f"${metrics['average_transaction']:,.2f}")
col3.metric("Largest Transaction", f"${metrics['largest_transaction']:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Most Common Merchant", metrics["most_common_merchant"])
col5.metric("Top Category", metrics["top_category"])
col6.metric("Transactions", f"{metrics['transaction_count']:,}")

# ---------------------------------------------------------------
# Section 2: Charts
# ---------------------------------------------------------------
st.header("📈 Visualizations")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.plotly_chart(spending_by_category_chart(df), use_container_width=True)
with chart_col2:
    st.plotly_chart(top_merchants_chart(df), use_container_width=True)

st.plotly_chart(spending_over_time_chart(df), use_container_width=True)
st.plotly_chart(monthly_trend_chart(df), use_container_width=True)

# ---------------------------------------------------------------
# Section 3: Suspicious transactions
# ---------------------------------------------------------------
st.header("🚨 Suspicious Transactions")

suspicious = get_suspicious_only(df)

if suspicious.empty:
    st.success("✅ No suspicious transactions found. Nice and clean!")
else:
    st.warning(f"Found **{len(suspicious)}** transaction(s) worth a second look:")
    st.dataframe(
        suspicious[["date", "merchant", "amount", "category", "suspicious_reason"]],
        use_container_width=True,
        hide_index=True,
    )

with st.expander("How does detection work?"):
    st.write(
        """
        Version 1 uses three simple rules:
        1. **Over $300** — unusually large purchases
        2. **More than 3x your average transaction** — way above your normal spending
        3. **Large charge (over $100) from a one-time merchant** — a big purchase
           somewhere you've never shopped before
        """
    )

# ---------------------------------------------------------------
# Section 4: Savings goal tracker
# ---------------------------------------------------------------
st.header("🎯 Savings Goal Tracker")

goal_col1, goal_col2, goal_col3 = st.columns(3)
with goal_col1:
    goal_amount = st.number_input("Savings goal ($)", min_value=0.0, value=5000.0, step=100.0)
with goal_col2:
    current_savings = st.number_input("Current savings ($)", min_value=0.0, value=1000.0, step=100.0)
with goal_col3:
    target_date = st.date_input("Target date", value=date.today() + timedelta(days=180))

plan = calculate_savings_plan(goal_amount, current_savings, target_date)

result_col1, result_col2, result_col3 = st.columns(3)
result_col1.metric("Remaining to Save", f"${plan['remaining']:,.2f}")
result_col2.metric("Weeks Until Target", f"{plan['weeks_left']:.1f}")
result_col3.metric("Needed per Week", f"${plan['per_week']:,.2f}")

# Visual progress toward the goal
if goal_amount > 0:
    progress = min(current_savings / goal_amount, 1.0)
    st.progress(progress, text=f"{progress:.0%} of goal reached")
    if progress >= 1.0:
        st.balloons()

# ---------------------------------------------------------------
# Section 5: Raw data (handy for debugging / curiosity)
# ---------------------------------------------------------------
with st.expander("🔍 View cleaned transaction data"):
    st.dataframe(df, use_container_width=True, hide_index=True)
