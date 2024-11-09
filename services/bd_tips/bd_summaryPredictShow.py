import pandas as pd
import matplotlib.pyplot as plt

# Load historical transaction data
historical_data = pd.read_csv("datasets/dataset_bank_transactions.csv")
historical_data['TransactionDate'] = pd.to_datetime(historical_data['TransactionDate'], format='%d/%m/%y')

# Group by CustomerID and month to get the cumulative balance for each month
historical_data['Month'] = historical_data['TransactionDate'].dt.to_period('M')
monthly_historical_balance = historical_data.groupby(['CustomerID', 'Month']).agg({
    'Amount': 'sum'
}).rename(columns={'Amount': 'Actual Balance'}).reset_index()
monthly_historical_balance['ds'] = monthly_historical_balance['Month'].dt.to_timestamp()

# Load forecast data
forecast_data = pd.read_csv("datasets/cash_flow_forecast.csv")
forecast_data['ds'] = pd.to_datetime(forecast_data['ds'])  # Ensure 'ds' is in datetime format

# Loop over each customer to create a plot
for customer_id, customer_forecast in forecast_data.groupby('CustomerID'):
    # Filter historical data for the current customer
    customer_historical = monthly_historical_balance[monthly_historical_balance['CustomerID'] == customer_id]

    # Create a plot
    plt.figure(figsize=(10, 6))

    # Plot historical balance as a solid line with markers
    plt.plot(customer_historical['ds'], customer_historical['Actual Balance'], 'o-', color='blue',
             label='Actual Balance')

    # Plot forecasted balance as a dashed line
    plt.plot(customer_forecast['ds'], customer_forecast['yhat'], 'b--', label='Forecast')

    # Add confidence interval shading for the forecast
    plt.fill_between(customer_forecast['ds'],
                     customer_forecast['yhat_lower'],
                     customer_forecast['yhat_upper'],
                     color='blue', alpha=0.1, label='Confidence Interval')

    # Configure plot appearance
    plt.title(f"Monthly Cash Flow Forecast for Customer {customer_id}")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.legend()
    plt.grid()

    # Show the plot
    plt.show()
