import pandas as pd
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Load transaction history from the CSV file
logging.info("Loading transaction data from 'datasets/bank_transactions.csv'")
df = pd.read_csv("datasets/bank_transactions.csv")

# 2. Convert the date column to datetime format and sort the data
logging.info("Converting 'TransactionDate' to datetime format and sorting by date")
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format="%d/%m/%y", errors='coerce')
df = df.sort_values(by='TransactionDate')

# 3. Ensure amounts are in numeric format
logging.info("Ensuring 'TransactionAmount (INR)' and 'CustAccountBalance' are numeric")
df['TransactionAmount (INR)'] = pd.to_numeric(df['TransactionAmount (INR)'], errors='coerce').fillna(0)
df['CustAccountBalance'] = pd.to_numeric(df['CustAccountBalance'], errors='coerce').fillna(0)

# 4. Create columns for income and expenses
# Assuming a positive 'TransactionAmount (INR)' value is income and a negative value is an expense
logging.info("Creating 'Income' and 'Expense' columns based on transaction amounts")
df['Income'] = df['TransactionAmount (INR)'].apply(lambda x: x if x > 0 else 0)
df['Expense'] = df['TransactionAmount (INR)'].apply(lambda x: abs(x) if x < 0 else 0)

# 5. Group data by month to calculate monthly cash flow
logging.info("Grouping data by month to calculate monthly cash flow")
df.set_index('TransactionDate', inplace=True)  # Set 'TransactionDate' as index
monthly_df = df.resample('ME').agg({
    'Income': 'sum',
    'Expense': 'sum',
    'CustAccountBalance': 'last'  # End balance for the month
}).rename(columns={'CustAccountBalance': 'End Balance'})

# 6. Calculate the monthly net cash flow
monthly_df['Net Cash Flow'] = monthly_df['Income'] - monthly_df['Expense']

# 7. Handle missing values in the end balance (if applicable)
logging.info("Handling missing values in the 'End Balance' column")
monthly_df['End Balance'] = monthly_df['End Balance'].ffill()

# 8. Display the resulting data
logging.info("Displaying prepared monthly cash flow data")
print(monthly_df.head())

# Optionally, save the cleaned and processed file for future analysis
monthly_df.to_csv("datasets/processed_monthly_cash_flow.csv")
logging.info("Processed monthly cash flow data saved to 'datasets/processed_monthly_cash_flow.csv'")
