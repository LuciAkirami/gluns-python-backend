import pandas as pd
from fastapi import HTTPException
from typing import List, Optional
from numpy import random

from services.bd_tips.modelDTO.TransactionData import TransactionDataResponse, TransactionData

class SummaryService:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_transaction_data(self, random_choice: bool = False) -> List[TransactionDataResponse]:
        try:
            # Read
            data = pd.read_csv(self.filepath)

            # Random user id if enabled random_choice
            if random_choice:
                unique_user_ids = data['CustomerID'].unique()
                user_id = random.choice(unique_user_ids)
            else:
                # Default user
                user_id = data['CustomerID'].iloc[0]

            # Filter transactions by user_id if specified
            if user_id:
                data = data[data['CustomerID'] == user_id]

            # Map object
            transactions = [
                TransactionDataResponse(
                    customer_id=row['CustomerID'],
                    month=row['Month'],
                    monthly_expense=row['Monthly Expense'],
                    monthly_income=row['Monthly Income']
                )
                for _, row in data.iterrows()
            ]
            return transactions
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error loading transaction data")
