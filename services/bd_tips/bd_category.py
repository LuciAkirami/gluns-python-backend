import pandas as pd
import numpy as np
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load transaction data
logging.info("Loading transaction data from 'datasets/bank_transactions.csv'")
df = pd.read_csv("datasets/bank_transactions.csv")

# Display column names
print("Available columns:", df.columns.tolist())

# Convert the date column to datetime and sort
logging.info("Converting 'TransactionDate' to datetime format and sorting by date")
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format="%d/%m/%y", errors='coerce')
df = df.sort_values(by='TransactionDate')

# Ensure 'TransactionAmount (INR)' is numeric
df['TransactionAmount (INR)'] = pd.to_numeric(df['TransactionAmount (INR)'], errors='coerce').fillna(0)

# Filter data for two specific customers (example IDs)
selected_customers = ['C5841053', 'C2142763']  # Replace with actual IDs from your dataset
df = df[df['CustomerID'].isin(selected_customers)]

# Simulate a description column with more specific categories
np.random.seed(0)  # For consistent results
descriptions = [
    "Salary", "Grocery shopping", "Restaurant bill", "Uber ride", "Online shopping",
    "Electricity bill", "Water utility", "Netflix subscription", "Other expenses"
]
df['TransactionDescription'] = np.random.choice(descriptions, size=len(df))

# Categorize transactions
def categorize_transaction(description):
    description = str(description).lower()
    if "salary" in description or "income" in description:
        return "Income"
    elif "grocery" in description or "restaurant" in description:
        return "Food"
    elif "uber" in description or "ride" in description or "transport" in description:
        return "Transport"
    elif "netflix" in description or "entertainment" in description:
        return "Entertainment"
    elif "shopping" in description or "store" in description:
        return "Shopping"
    elif "electricity" in description or "water" in description or "utility" in description:
        return "Utilities"
    else:
        return "Other"

# Apply categorization and show diagnostic information
logging.info("Categorizing transactions based on description keywords")
df['Category'] = df['TransactionDescription'].apply(categorize_transaction)

# Check the categorized data
print("\nCategorized data sample:\n", df[['CustomerID', 'TransactionDate', 'TransactionDescription', 'Category', 'TransactionAmount (INR)']].head(10))

# Check the distribution of categories
category_counts = df['Category'].value_counts()
print("\nCategory distribution for selected customers:\n", category_counts)

# Separate Income and Expense
logging.info("Separating income and expenses based on transaction amount")
df['Income'] = df.apply(lambda x: x['TransactionAmount (INR)'] if x['Category'] == 'Income' else 0, axis=1)
df['Expense'] = df.apply(lambda x: abs(x['TransactionAmount (INR)']) if x['Category'] != 'Income' else 0, axis=1)

# Group by CustomerID, month, and category to calculate monthly totals per category
logging.info("Grouping data by CustomerID, month, and category to calculate monthly totals")
df.set_index('TransactionDate', inplace=True)
monthly_category_totals = df.groupby(['CustomerID', pd.Grouper(freq='M'), 'Category']).agg({
    'Income': 'sum',
    'Expense': 'sum'
}).unstack(fill_value=0)  # Unstack to have categories as columns, fill missing values with 0

# Display resulting monthly category summary by customer
logging.info("Displaying monthly category summary by customer")
print(monthly_category_totals.head())

# Save the processed monthly category summary by customer
monthly_category_totals.to_csv("datasets/processed_monthly_category_totals_two_customers.csv")
logging.info("Processed monthly category totals for two customers saved to 'datasets/processed_monthly_category_totals_two_customers.csv'")
