import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

FILE = "expenses.csv"

# Load existing expense records
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(
        columns=["Date", "Category", "Description", "Amount"]
    )

st.title("Personal Expense Tracker")
st.write("Track your daily expenses and manage your monthly budget.")

# Monthly budget
st.header("1. Set Monthly Budget")

budget = st.number_input(
    "Monthly Budget (₹)",
    min_value=0.0,
    value=10000.0,
    step=500.0
)

# Add a new expense
st.header("2. Add New Expense")

with st.form("expense_form"):
    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    category = st.selectbox(
        "Expense Category",
        ["Food", "Travel", "Education", "Shopping", "Bills", "Other"]
    )

    description = st.text_input("Expense Description")

    amount = st.number_input(
        "Expense Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0:
            st.error("Please enter an amount greater than zero.")
        else:
            new_expense = pd.DataFrame([{
                "Date": str(expense_date),
                "Category": category,
                "Description": description,
                "Amount": amount
            }])

            df = pd.concat(
                [df, new_expense],
                ignore_index=True
            )

            df.to_csv(FILE, index=False)

            st.success("Expense added successfully!")
            st.rerun()

# Expense dashboard
st.header("3. Expense Dashboard")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

    available_months = sorted(
        df["Date"].dt.strftime("%Y-%m").unique(),
        reverse=True
    )

    selected_month = st.selectbox(
        "Select Month",
        available_months
    )

    monthly_df = df[
        df["Date"].dt.strftime("%Y-%m") == selected_month
    ]

    total_expenses = monthly_df["Amount"].sum()
    remaining_budget = budget - total_expenses

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}"
    )

    col2.metric(
        "Monthly Budget",
        f"₹{budget:,.2f}"
    )

    col3.metric(
        "Remaining Budget",
        f"₹{remaining_budget:,.2f}"
    )

    if remaining_budget < 0:
        st.warning("You have exceeded your monthly budget!")
    else:
        st.success("You are within your monthly budget.")

    st.subheader("Category-wise Expense Analysis")

    category_totals = monthly_df.groupby(
        "Category"
    )["Amount"].sum()

    st.bar_chart(category_totals)

    st.subheader("Expense History")

    st.dataframe(
        monthly_df.sort_values("Date", ascending=False),
        use_container_width=True
    )

    st.download_button(
        label="Download Expense Report (CSV)",
        data=monthly_df.to_csv(index=False).encode("utf-8"),
        file_name="expense_report.csv",
        mime="text/csv"
    )

else:
    st.info("No expenses recorded yet. Add your first expense above.")

st.caption("Personal Expense Tracker | Python, Pandas and Streamlit")