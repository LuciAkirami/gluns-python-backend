from pydantic import BaseModel
from typing import Union

class TransactionData:
    def __init__(self, customer_id: str, month: str, monthly_expense: float, monthly_income: float):
        self.customer_id = customer_id
        self.month = month
        self.monthly_expense = monthly_expense
        self.monthly_income = monthly_income

    def __repr__(self):
        return f"TransactionData(customer_id={self.customer_id}, month={self.month}, monthly_expense={self.monthly_expense}, monthly_income={self.monthly_income})"

# DTO para la respuesta en la API
class TransactionDataResponse(BaseModel):
    customer_id: str
    month: str
    monthly_expense: float
    monthly_income: float

    @classmethod
    def from_transaction_data(cls, transaction: TransactionData):
        return cls(
            customer_id=transaction.customer_id,
            month=transaction.month,
            monthly_expense=transaction.monthly_expense,
            monthly_income=transaction.monthly_income
        )
