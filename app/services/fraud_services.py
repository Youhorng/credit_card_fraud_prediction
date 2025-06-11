import joblib  # type: ignore
import os
import pandas as pd
import numpy as np
from typing import Tuple

# Class for handling fraud prediction services
class FraudDetectionService:
    # Initialize the fraud detection service with a direct model loading 
    def __init__(self):
        # Base paths 
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Model and Preprocessor paths
        model_path = os.path.join(base_dir, "models", "xgb_model.pkl")
        preprocessor_path = os.path.join(base_dir, "models", "preprocessor_pipeline.pkl")

        # Load Model and Preprocessor directly
        print(f"Loading model from '{model_path}'")
        self.model = joblib.load(model_path)

        print(f"Loading preprocessor from '{preprocessor_path}'")
        self.preprocessor = joblib.load(preprocessor_path)

    # Method to predict fraud based on transaction data
    def predict(self, data: pd.DataFrame) -> Tuple[bool, str, float]:
        """
        Predict if a transaction is fraudulent
        
        Args:
            data: Transaction data as DataFrame
            
        Returns:
            Tuple of (is_fraud: bool, label: str, fraud_probability: float)
        """
        # Drop transaction_id from dataframe
        if 'transaction_id' in data.columns:
            data = data.drop(columns=['transaction_id'])

        # Preprocess the data 
        processed_data = self.preprocessor.transform(data)     

        # Predict fraud in the transaction
        is_fraud = self.model.predict(processed_data)
        label = ["Fraud" if fraud == 1 else "Normal" for fraud in is_fraud]

        # Get the probability of fraud
        fraud_probability = self.model.predict_proba(processed_data)[:, 1]

        # Return the prediction result
        return bool(is_fraud[0]), label[0], float(fraud_probability[0])
