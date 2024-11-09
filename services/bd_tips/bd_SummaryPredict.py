import pandas as pd
from prophet import Prophet

# Load the dataset with income and expense data
df = pd.read_csv("datasets/dataset_bank_transactions.csv")

# Ensure 'TransactionDate' is in datetime format
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format='%d/%m/%y')

# Group by user and month to calculate monthly balance
df['Month'] = df['TransactionDate'].dt.to_period('M')
monthly_balances = df.groupby(['CustomerID', 'Month']).agg({
    'Amount': 'sum'
}).rename(columns={'Amount': 'Net Amount'}).reset_index()

# Calculate cumulative monthly balance for each user
monthly_balances['Balance'] = monthly_balances.groupby('CustomerID')['Net Amount'].cumsum()

# Prepare data for Prophet
monthly_balances['ds'] = monthly_balances['Month'].dt.to_timestamp()  # Convert 'Month' to timestamp for Prophet
monthly_balances = monthly_balances.rename(columns={'Balance': 'y'})

# Create a Prophet model for each user and forecast 6 months ahead
forecast_dfs = []
for user_id, user_data in monthly_balances.groupby('CustomerID'):
    model = Prophet(interval_width=0.95)  # Set interval width to ensure yhat_upper and yhat_lower are calculated
    model.fit(user_data[['ds', 'y']])  # Train the model with monthly balance time series

    # Generate a forecast for the next 6 months
    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)

    # Print forecast sample to check if yhat_upper and yhat_lower are present
    print(f"\nSample forecast for user {user_id}:\n", forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower']].head())

    # Add CustomerID to the forecast
    forecast['CustomerID'] = user_id
    forecast = forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower', 'CustomerID']]
    forecast_dfs.append(forecast)

# Concatenate all forecasts
forecast_df = pd.concat(forecast_dfs)

# Save the forecast result to a CSV file
forecast_df.to_csv("datasets/cash_flow_forecast.csv", index=False)
print("Forecast file generated: 'cash_flow_forecast.csv'")
