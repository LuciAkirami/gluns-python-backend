import pandas as pd
import random
import os
from datetime import datetime, timedelta

# Load the original dataset
df = pd.read_csv("datasets/bank_transactions.csv")

# Array with the new user identifiers to replace CustomerID
new_user_ids = ["17ec6145-f058-49c2-8c71-042f2352f3bb", "b65e395c-6518-4e1d-9387-07a555b18ed3", "526eb4e0-7770-495c-bf4b-3d7a829d8c57"]

# Randomly replace CustomerIDs with new IDs
df['CustomerID'] = [random.choice(new_user_ids) for _ in range(len(df))]

# Randomly assign 'Income' or 'Expense' to each transaction
df['Transaction Type'] = df['TransactionAmount (INR)'].apply(lambda x: 'Income' if random.random() < 0.5 else 'Expense')

# Adjust amounts: make expenses negative
df['Amount'] = df.apply(lambda x: x['TransactionAmount (INR)'] if x['Transaction Type'] == 'Income' else -x['TransactionAmount (INR)'], axis=1)

# Generate random dates between 2016-01-01 and today for each transaction
start_date = datetime(2016, 1, 1)
end_date = datetime.now()
df['TransactionDate'] = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(len(df))]

# Calculate the cumulative balance per user, with sorting to ensure correct order
df = df.sort_values(by=['CustomerID', 'TransactionDate'])
df['Balance'] = df.groupby('CustomerID')['Amount'].cumsum()

# Round the 'Balance' column to two decimal places
df['Balance'] = df['Balance'].round(2)

# Verify the updated Balance column
print(df[['CustomerID', 'TransactionDate', 'TransactionAmount (INR)', 'Transaction Type', 'Amount', 'Balance']].head(10))

# Ensure output directory exists
output_dir = "datasets"
os.makedirs(output_dir, exist_ok=True)

# Save the modified dataset
output_path = os.path.join(output_dir, "dataset_bank_transactions.csv")
df.to_csv(output_path, index=False)
print(f"File generated: '{output_path}'")
