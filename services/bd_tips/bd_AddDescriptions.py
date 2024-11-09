import pandas as pd
import random

# Cargar el dataset original y renombrar 'CustomerID' a 'UserID'
df = pd.read_csv("datasets/bank_transactions_with_main_categories.csv")
df.rename(columns={'CustomerID': 'UserID', 'TransactionAmount (INR)': 'Transaction Amount'}, inplace=True)

# Simular 'Transaction Details' basándose en la categoría
transaction_details = {
    "Income": ["Salary Payment", "Freelance Payment", "Sales Income", "Pension Payment"],
    "Food": ["Grocery Store Purchase", "Restaurant Dinner", "Fast Food Purchase", "Cafe Visit"],
    "Housing": ["Monthly Rent", "Mortgage Payment"],
    "Utilities": ["Electricity Bill", "Water Bill", "Internet Bill", "Phone Bill"],
    "Entertainment": ["Movie Tickets", "Concert Tickets", "Streaming Subscription", "Gaming Purchase"],
    "Shopping": ["Clothing Purchase", "Electronics Purchase", "Online Shopping", "Accessory Purchase"],
    "Other": ["Miscellaneous Expense", "Gift Purchase", "Donation", "Charity"],
}

df['Transaction Details'] = df['Category'].apply(lambda x: random.choice(transaction_details.get(x, ["General Expense"])))

# Asignar aleatoriamente 'Withdrawal Amount' y 'Deposit Amount' según 'Income' o 'Expense'
df['Withdrawal Amount'] = df.apply(lambda x: x['Transaction Amount'] if x['Category'] != 'Income' else 0, axis=1)
df['Deposit Amount'] = df.apply(lambda x: x['Transaction Amount'] if x['Category'] == 'Income' else 0, axis=1)

# Calcular el 'Balance After' suponiendo un saldo inicial y acumulando los movimientos
df = df.sort_values(['UserID', 'TransactionDate'])
initial_balance = 3000  # Saldo inicial para cada usuario, puedes modificarlo según sea necesario

def calculate_balance(row, previous_balance):
    if row['Deposit Amount'] > 0:
        return previous_balance + row['Deposit Amount']
    else:
        return previous_balance - row['Withdrawal Amount']

# Asignar saldo inicial y calcular el saldo tras cada transacción
df['Balance After'] = initial_balance
user_balances = {}

for idx, row in df.iterrows():
    user_id = row['UserID']
    if user_id in user_balances:
        balance = calculate_balance(row, user_balances[user_id])
    else:
        balance = calculate_balance(row, initial_balance)
    df.at[idx, 'Balance After'] = balance
    user_balances[user_id] = balance

# Simular columnas adicionales
payment_methods = ["Card", "Transfer", "Cash", "Mobile Payment"]
locations = ["Mumbai, India", "Delhi, India", "Pune, India", "Chennai, India", "Bangalore, India"]
industries = ["Technology", "Commerce", "Healthcare", "Education", "Design"]
income_ranges = ["1,500-2,000 USD", "2,000-3,000 USD", "3,000-5,000 USD", "4,000-6,000 USD", "5,000-7,000 USD"]

df['Payment Method'] = [random.choice(payment_methods) for _ in range(len(df))]
df['Transaction Location'] = [random.choice(locations) for _ in range(len(df))]
df['Transaction Type'] = df['Category'].apply(lambda x: "Income" if x == "Income" else "Expense")
df['Industry'] = [random.choice(industries) for _ in range(len(df))]
df['Income Range'] = [random.choice(income_ranges) for _ in range(len(df))]

# Seleccionar y reordenar las columnas como en el ejemplo final
df = df[['UserID', 'TransactionDate', 'Transaction Details', 'Withdrawal Amount', 'Deposit Amount', 'Balance After',
         'Payment Method', 'Transaction Location', 'Category', 'Transaction Type', 'Industry', 'Income Range']]

# Guardar el nuevo dataset en un archivo CSV
df.to_csv("datasets/enriched_bank_transactions.csv", index=False)
print("Archivo generado: 'enriched_bank_transactions.csv'")
