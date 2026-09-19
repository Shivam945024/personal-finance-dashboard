import pandas as pd


def transactions_dataframe(transactions):
    if not transactions:
        return pd.DataFrame(
            columns=[
                "id",
                "transaction_date",
                "description",
                "category",
                "transaction_type",
                "amount",
                "payment_method",
                "notes"
            ]
        )

    df = pd.DataFrame(transactions)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    return df


def calculate_summary(df):
    if df.empty:
        return {
            "income": 0,
            "expense": 0,
            "savings": 0,
            "savings_rate": 0
        }

    income = df.loc[
        df["transaction_type"] == "Income",
        "amount"
    ].sum()

    expense = df.loc[
        df["transaction_type"] == "Expense",
        "amount"
    ].sum()

    savings = income - expense

    savings_rate = (
        (savings / income) * 100
        if income > 0
        else 0
    )

    return {
        "income": income,
        "expense": expense,
        "savings": savings,
        "savings_rate": savings_rate
    }


def monthly_summary(df):
    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    data["month"] = data["transaction_date"].dt.to_period(
        "M"
    ).astype(str)

    income = (
        data[data["transaction_type"] == "Income"]
        .groupby("month")["amount"]
        .sum()
    )

    expense = (
        data[data["transaction_type"] == "Expense"]
        .groupby("month")["amount"]
        .sum()
    )

    result = pd.DataFrame({
        "Income": income,
        "Expense": expense
    }).fillna(0)

    result["Savings"] = (
        result["Income"] - result["Expense"]
    )

    result = result.reset_index()

    return result


def category_summary(df):
    if df.empty:
        return pd.DataFrame()

    expenses = df[
        df["transaction_type"] == "Expense"
    ]

    if expenses.empty:
        return pd.DataFrame()

    result = (
        expenses
        .groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    return result


def budget_analysis(df, budgets):
    category_expenses = category_summary(df)

    if category_expenses.empty:
        category_expenses = pd.DataFrame(
            columns=["category", "amount"]
        )

    budget_df = pd.DataFrame(budgets)

    if budget_df.empty:
        return pd.DataFrame(
            columns=[
                "category",
                "budget",
                "spent",
                "remaining",
                "usage_percent"
            ]
        )

    result = budget_df.merge(
        category_expenses,
        on="category",
        how="left"
    )

    result["amount"] = result["amount"].fillna(0)

    result.rename(
        columns={
            "amount_x": "budget",
            "amount_y": "spent"
        },
        inplace=True
    )

    if "budget" not in result:
        result["budget"] = result["amount"]

    if "spent" not in result:
        result["spent"] = 0

    result["remaining"] = (
        result["budget"] - result["spent"]
    )

    result["usage_percent"] = (
        result["spent"] / result["budget"] * 100
    ).round(2)

    return result[
        [
            "category",
            "budget",
            "spent",
            "remaining",
            "usage_percent"
        ]
    ]
