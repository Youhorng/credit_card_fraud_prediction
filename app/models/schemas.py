from pypdantic import BaseModel, Field # type: ignore
from typing import Dict, List, Any, Optional
from datetime import datetime 

# Schema for transaction data sent to the API for prediction
class TransactionRequest(BaseModel):
    transaction_amount: float = Field(..., description="Amount of the transaction")
    is_nighttime: int = Field(..., description="1 if the transaction is made at night, 0 otherwise")
    category: str = Field(..., description="Merchant category")
    transaction_location: str = Field(..., description="Location of the transaction")
    job: str = Field(..., description="Job of the cardholder")
    state: str = Field(..., description="State where the transaction occurred")
    transaction_number: str = Field(..., description="Unique identifier for the transaction")

    class Config:
        schema_extra = {
            "example": {
                "transaction_amount": 150.55,
                "is_nighttime": 1,
                "category": "shopping_pos",
                "transaction_location": "-95.7923, 36.1499",
                "job": "Naval architect",
                "state": "CA",
                "transaction_number": "tx_1001"
            }
        }

# Schema for the response from the API after prediction
class PredictionResponse(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    is_fraud: str = Field(..., description="Prediction result: 'Fraud' for fraud, 'Normal' for not fraud")
    fraud_probability: float = Field(..., description="Probability of the transaction being fraudulent")
    timestamp: datetime = Field(..., description="Timestamp of the prediction")

# Schema for the model performance metrics 
class ModelMetrics(BaseModel):
    f1_score: float
    precision: float
    recall: float
    average_precision: float

    class Config:
        schema_extra = {
            "example": {
                "f1_score": 0.85,
                "precision": 0.88,
                "recall": 0.82,
                "average_precision": 0.90
            }
        }
