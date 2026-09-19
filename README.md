# 💰 Personal Finance Dashboard

A full-stack-style personal finance analytics dashboard built with **Python, Streamlit, SQLite, Pandas and Plotly**.

The application allows users to record income and expenses, monitor savings, create budgets, analyze spending categories and download financial reports.

## 🚀 Features

* 💵 Income tracking
* 💸 Expense tracking
* 💰 Automatic savings calculation
* 📈 Savings-rate calculation
* 📊 Monthly income vs expense charts
* 🥧 Expense category visualization
* 🎯 Monthly category budgets
* ⚠️ Budget usage alerts
* 🔎 Transaction search
* 🗑️ Transaction deletion
* 📅 Date-range financial reports
* 📥 CSV report download
* 🗄️ SQLite database
* 📱 Streamlit web interface

## 🛠️ Technologies

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Application logic         |
| Streamlit  | Web dashboard             |
| SQLite     | Database                  |
| Pandas     | Data analysis             |
| Plotly     | Interactive visualization |
| Git        | Version control           |
| GitHub     | Project hosting           |

## 📁 Project Structure

```text
personal-finance-dashboard/
│
├── app.py
├── database.py
├── finance.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── finance.db
│
└── .streamlit/
    └── config.toml
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/personal-finance-dashboard.git
```

### 2. Enter the project

```bash
cd personal-finance-dashboard
```

### 3. Create virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## 🗄️ Database

The application uses SQLite.

The database is automatically created at:

```text
data/finance.db
```

### Transactions table

The transactions table contains:

* id
* transaction_date
* description
* category
* transaction_type
* amount
* payment_method
* notes
* created_at

### Budgets table

The budgets table contains:

* id
* category
* amount

## 📊 Dashboard

The dashboard provides:

### Financial Summary

* Total Income
* Total Expenses
* Total Savings
* Savings Rate

### Visualizations

* Monthly Income vs Expense
* Expense Distribution by Category
* Monthly Savings Trend

## 🎯 Budget Management

Users can configure category-based monthly budgets.

Example:

```text
Food       ₹5,000
Transport  ₹3,000
Shopping   ₹4,000
Bills      ₹5,000
```

The application calculates budget utilization and displays warnings when spending approaches or exceeds the configured budget.

## 📑 Reports

Users can select a date range and generate:

* Total income
* Total expenses
* Total savings
* Category-wise expenses
* Transaction details

Reports can be downloaded as CSV files.

## 🔐 Privacy

Financial data is stored locally in SQLite.

The SQLite database is excluded from Git using `.gitignore` so personal financial information is not accidentally uploaded to GitHub.

## 🔮 Future Improvements

Possible future versions could include:

* User authentication
* Multiple user accounts
* Recurring transactions
* Investment portfolio tracking
* EMI calculator
* Financial goal tracking
* PDF report generation
* Excel export
* Email reports
* Expense prediction using machine learning
* Automatic transaction categorization
* Bank API integration
* Cloud database
* Mobile-friendly PWA
* AI-powered financial insights

## 👨‍💻 Author

**Shivam Singh**

B.Tech CSE Student

### Areas of Interest

* Python
* Full Stack Development
* Artificial Intelligence
* Machine Learning
* Computer Vision
* Data Analytics

## ⭐ Project Purpose

This project was developed as a portfolio project to demonstrate practical skills in:

```text
Python
↓
SQLite
↓
Pandas
↓
Data Analysis
↓
Plotly
↓
Streamlit
↓
Web Dashboard
```

If you find this project useful, consider giving the repository a ⭐.
# personal-finance-dashboard
personal finance dashboard
