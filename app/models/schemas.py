from pydantic import BaseModel, Field # type: ignore
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

    model_config = {  # Updated to use model_config instead of Config class
        "json_schema_extra": {  # Changed from schema_extra to json_schema_extra
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
    }

# Schema for the response from the API after prediction
class PredictionResponse(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    is_fraud: bool = Field(..., description="Prediction result: '1' for fraud, '0' for not fraud")
    label: str = Field(..., description="Label indicating if the transaction is fraudulent or not")
    fraud_probability: float = Field(..., description="Probability of the transaction being fraudulent")
    timestamp: datetime = Field(..., description="Timestamp of the prediction")

class ModelInfoResponse(BaseModel):
    """Schema for model information response"""
    model_name: str = Field(..., description="Name of the model")
    model_version: str = Field(..., description="Version of the model")
    threshold: float = Field(..., description="Classification threshold for fraud detection")
    
    model_config = {  # Updated configuration
        "protected_namespaces": (),  # Disable protected namespace warnings
        "json_schema_extra": {
            "example": {
                "model_name": "XGBoost Fraud Detection Model",
                "model_version": "1.0.0",
                "threshold": 0.5
            }
        }
    }

# Schema for the model performance metrics 
class ModelMetricsResponse(BaseModel):
    f1_score: float
    precision: float
    recall: float
    average_precision: float

    model_config = {  # Updated to use model_config
        "json_schema_extra": {  # Changed from schema_extra
            "example": {
                "f1_score": 0.85,
                "precision": 0.88,
                "recall": 0.82,
                "average_precision": 0.90
            }
        }
    }