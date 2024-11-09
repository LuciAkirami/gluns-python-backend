import pandas as pd
import matplotlib.pyplot as plt

# Load the processed monthly category totals
monthly_category_totals = pd.read_csv("datasets/processed_monthly_category_totals.csv", header=[0, 1], index_col=0)

# Separate Income and Expense data for plotting
income_data = monthly_category_totals['Income']
expense_data = monthly_category_totals['Expense']

# Plot stacked bar chart for Income and Expense
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Plot Income categories
income_data.plot(kind='bar', stacked=True, ax=axes[0], colormap='viridis')
axes[0].set_title('Monthly Income by Category')
axes[0].set_ylabel('Amount (INR)')
axes[0].legend(title='Income Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Plot Expense categories
expense_data.plot(kind='bar', stacked=True, ax=axes[1], colormap='plasma')
axes[1].set_title('Monthly Expenses by Category')
axes[1].set_ylabel('Amount (INR)')
axes[1].legend(title='Expense Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Final formatting
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
