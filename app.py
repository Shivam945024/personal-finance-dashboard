import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    initialize_database,
    add_transaction,
    get_transactions,
    delete_transaction,
    save_budget,
    get_budgets,
    delete_budget
)

from finance import (
    transactions_dataframe,
    calculate_summary,
    monthly_summary,
    category_summary,
    budget_analysis
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #777;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 15px;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">💰 Personal Finance Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Track income, expenses, savings and budgets</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Add Transaction",
        "Transactions",
        "Budget",
        "Reports"
    ]
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

transactions = get_transactions()

df = transactions_dataframe(transactions)

budgets = get_budgets()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("📊 Financial Overview")

    if df.empty:
        st.info(
            "No transactions available. "
            "Go to 'Add Transaction' to add your first transaction."
        )

    summary = calculate_summary(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💵 Total Income",
        f"₹{summary['income']:,.2f}"
    )

    col2.metric(
        "💸 Total Expense",
        f"₹{summary['expense']:,.2f}"
    )

    col3.metric(
        "💰 Savings",
        f"₹{summary['savings']:,.2f}"
    )

    col4.metric(
        "📈 Savings Rate",
        f"{summary['savings_rate']:.2f}%"
    )

    st.divider()

    # ----------------------------------------------
    # MONTHLY CHART
    # ----------------------------------------------

    monthly = monthly_summary(df)

    if not monthly.empty:

        st.subheader("📈 Income vs Expense")

        fig = px.bar(
            monthly,
            x="month",
            y=["Income", "Expense"],
            barmode="group",
            title="Monthly Income and Expenses"
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Amount (₹)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ----------------------------------------------
    # CATEGORY + SAVINGS
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    categories = category_summary(df)

    with col1:

        st.subheader("🍕 Expenses by Category")

        if not categories.empty:

            fig = px.pie(
                categories,
                names="category",
                values="amount",
                title="Expense Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No expense data available.")

    with col2:

        st.subheader("💰 Savings Trend")

        if not monthly.empty:

            fig = px.line(
                monthly,
                x="month",
                y="Savings",
                markers=True,
                title="Monthly Savings"
            )

            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Savings (₹)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No savings data available.")


# --------------------------------------------------
# ADD TRANSACTION
# --------------------------------------------------

elif page == "Add Transaction":

    st.header("➕ Add Transaction")

    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            transaction_date = st.date_input(
                "Date"
            )

            description = st.text_input(
                "Description",
                placeholder="e.g. Monthly Salary"
            )

            transaction_type = st.selectbox(
                "Transaction Type",
                [
                    "Income",
                    "Expense"
                ]
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=100.0
            )

        with col2:

            category = st.selectbox(
                "Category",
                [
                    "Salary",
                    "Freelancing",
                    "Business",
                    "Food",
                    "Rent",
                    "Transport",
                    "Shopping",
                    "Education",
                    "Entertainment",
                    "Bills",
                    "Healthcare",
                    "Investment",
                    "Travel",
                    "Other"
                ]
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Bank Transfer",
                    "Other"
                ]
            )

            notes = st.text_area(
                "Notes"
            )

        submitted = st.form_submit_button(
            "Add Transaction",
            type="primary"
        )

        if submitted:

            if not description.strip():

                st.error(
                    "Please enter a description."
                )

            elif amount <= 0:

                st.error(
                    "Amount must be greater than zero."
                )

            else:

                add_transaction(
                    str(transaction_date),
                    description,
                    category,
                    transaction_type,
                    amount,
                    payment_method,
                    notes
                )

                st.success(
                    "Transaction added successfully!"
                )

                st.rerun()


# --------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------

elif page == "Transactions":

    st.header("📋 Transactions")

    if df.empty:

        st.info(
            "No transactions found."
        )

    else:

        # Search

        search = st.text_input(
            "🔎 Search transactions"
        )

        filtered_df = df.copy()

        if search:

            search = search.lower()

            filtered_df = filtered_df[
                filtered_df.astype(str)
                .apply(
                    lambda row:
                    row.str.lower().str.contains(search).any(),
                    axis=1
                )
            ]

        # Type filter

        transaction_filter = st.selectbox(
            "Transaction Type",
            [
                "All",
                "Income",
                "Expense"
            ]
        )

        if transaction_filter != "All":

            filtered_df = filtered_df[
                filtered_df["transaction_type"]
                == transaction_filter
            ]

        st.dataframe(
            filtered_df[
                [
                    "id",
                    "transaction_date",
                    "description",
                    "category",
                    "transaction_type",
                    "amount",
                    "payment_method"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("🗑️ Delete Transaction")

        transaction_ids = filtered_df["id"].tolist()

        if transaction_ids:

            selected_id = st.selectbox(
                "Select transaction ID",
                transaction_ids
            )

            if st.button(
                "Delete Selected Transaction",
                type="secondary"
            ):

                delete_transaction(
                    selected_id
                )

                st.success(
                    "Transaction deleted."
                )

                st.rerun()


# --------------------------------------------------
# BUDGET
# --------------------------------------------------

elif page == "Budget":

    st.header("🎯 Budget Management")

    st.subheader("Set Category Budget")

    with st.form("budget_form"):

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Rent",
                "Transport",
                "Shopping",
                "Education",
                "Entertainment",
                "Bills",
                "Healthcare",
                "Travel",
                "Other"
            ]
        )

        amount = st.number_input(
            "Monthly Budget (₹)",
            min_value=0.0,
            step=500.0
        )

        submit_budget = st.form_submit_button(
            "Save Budget",
            type="primary"
        )

        if submit_budget:

            if amount <= 0:

                st.error(
                    "Budget must be greater than zero."
                )

            else:

                save_budget(
                    category,
                    amount
                )

                st.success(
                    f"Budget saved for {category}."
                )

                st.rerun()

    st.divider()

    st.subheader("📊 Budget Analysis")

    analysis = budget_analysis(
        df,
        budgets
    )

    if not analysis.empty:

        st.dataframe(
            analysis,
            use_container_width=True,
            hide_index=True
        )

        for _, row in analysis.iterrows():

            usage = row["usage_percent"]

            st.write(
                f"**{row['category']}** — "
                f"₹{row['spent']:,.2f} / "
                f"₹{row['budget']:,.2f}"
            )

            st.progress(
                min(int(usage), 100)
            )

            if usage > 100:

                st.error(
                    f"⚠️ {row['category']} budget exceeded!"
                )

            elif usage >= 80:

                st.warning(
                    f"⚠️ {row['category']} is at "
                    f"{usage:.1f}% of budget."
                )

    else:

        st.info(
            "No budgets configured."
        )


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif page == "Reports":

    st.header("📑 Financial Reports")

    if df.empty:

        st.info(
            "No transaction data available."
        )

    else:

        # ------------------------------------------
        # DATE FILTER
        # ------------------------------------------

        min_date = df["transaction_date"].min().date()
        max_date = df["transaction_date"].max().date()

        start_date, end_date = st.date_input(
            "Select date range",
            value=(min_date, max_date)
        )

        report_df = df[
            (
                df["transaction_date"].dt.date
                >= start_date
            )
            &
            (
                df["transaction_date"].dt.date
                <= end_date
            )
        ]

        summary = calculate_summary(
            report_df
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Income",
            f"₹{summary['income']:,.2f}"
        )

        col2.metric(
            "Expenses",
            f"₹{summary['expense']:,.2f}"
        )

        col3.metric(
            "Savings",
            f"₹{summary['savings']:,.2f}"
        )

        st.divider()

        # ------------------------------------------
        # CATEGORY REPORT
        # ------------------------------------------

        categories = category_summary(
            report_df
        )

        if not categories.empty:

            st.subheader(
                "Expense Category Report"
            )

            fig = px.bar(
                categories,
                x="category",
                y="amount",
                title="Expenses by Category"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ------------------------------------------
        # DOWNLOAD CSV
        # ------------------------------------------

        csv = report_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Report as CSV",
            data=csv,
            file_name="finance_report.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader(
            "Transaction Details"
        )

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True
        )
