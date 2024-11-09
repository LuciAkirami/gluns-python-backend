import pandas as pd


df = pd.read_csv("datasets/dataset_bank_transactions.csv")

# Count the number of transactions per user
transaction_counts = df['CustomerID'].value_counts().reset_index()
transaction_counts.columns = ['CustomerID', 'TransactionCount']

# Select the top users with the most transactions
top_3_users = transaction_counts.head(10)


transaction_counts.to_csv("datasets/top_users_by_transaction_count.csv", index=False)
print("Save file to: 'top_3_users_by_transaction_count.csv'")
