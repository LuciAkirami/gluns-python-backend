import pandas as pd

# Load the dataset with income and expense data
df = pd.read_csv("datasets/dataset_bank_transactions.csv")

# Ensure 'TransactionDate' is in datetime format (auto-detect format)
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

# Add a 'Month' column for grouping by month
df['Month'] = df['TransactionDate'].dt.to_period('M')

# Group by CustomerID, Month, and Transaction Type to calculate monthly totals for Income and Expense separately
monthly_summary = df.groupby(['CustomerID', 'Month', 'Transaction Type']).agg({
    'Amount': 'sum'
}).reset_index()

# Pivot the data so that Income and Expense are separate columns
monthly_summary = monthly_summary.pivot_table(
    index=['CustomerID', 'Month'],
    columns='Transaction Type',
    values='Amount',
    fill_value=0
).reset_index()

# Rename columns for clarity
monthly_summary.columns.name = None  # Remove pivot table index name
monthly_summary = monthly_summary.rename(columns={'Income': 'Monthly Income', 'Expense': 'Monthly Expense'})

# Save the monthly summary to a new CSV file
monthly_summary.to_csv("datasets/summary_monthly_user.csv", index=False)
print("Monthly summary file generated: summary_monthly_user.csv")
