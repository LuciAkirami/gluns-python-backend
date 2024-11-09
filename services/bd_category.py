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

# Simulate a description column with random categories
np.random.seed(0)  # For consistent results
categories = ["Salary", "Grocery", "Restaurant", "Uber", "Shopping", "Electricity", "Water", "Netflix", "Other"]
df['TransactionDescription'] = np.random.choice(categories, size=len(df))

# Categorize transactions
def categorize_transaction(description):
    description = str(description).lower()
    if "salary" in description or "income" in description:
        return "Income"
    elif "food" in description or "restaurant" in description or "grocery" in description:
        return "Food"
    elif "transport" in description or "uber" in description or "taxi" in description:
        return "Transport"
    elif "entertainment" in description or "movie" in description or "netflix" in description:
        return "Entertainment"
    elif "shopping" in description or "store" in description:
        return "Shopping"
    elif "utility" in description or "electricity" in description or "water" in description:
        return "Utilities"
    else:
        return "Other"

# Apply categorization
logging.info("Categorizing transactions based on description keywords")
df['Category'] = df['TransactionDescription'].apply(categorize_transaction)

# Separate Income and Expense
logging.info("Separating income and expenses based on transaction amount")
df['Income'] = df.apply(lambda x: x['TransactionAmount (INR)'] if x['Category'] == 'Income' else 0, axis=1)
df['Expense'] = df.apply(lambda x: abs(x['TransactionAmount (INR)']) if x['Category'] != 'Income' else 0, axis=1)

# Group by month and category to calculate monthly totals per category
logging.info("Grouping data by month and category to calculate monthly totals")
df.set_index('TransactionDate', inplace=True)
monthly_category_totals = df.groupby([pd.Grouper(freq='ME'), 'Category']).agg({
    'Income': 'sum',
    'Expense': 'sum'
}).unstack(fill_value=0)

# Display resulting monthly category summary
logging.info("Displaying monthly category summary")
print(monthly_category_totals.head())

# Save the processed monthly category summary
monthly_category_totals.to_csv("datasets/processed_monthly_category_totals.csv")
logging.info("Processed monthly category totals saved to 'datasets/processed_monthly_category_totals.csv'")
