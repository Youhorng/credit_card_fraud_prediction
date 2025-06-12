import joblib  # type: ignore
import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

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

        # Model Information
        self.threshold = 0.5 # Default threshold for fraud detection
        self.model_version = "1.0.0"  # Version of the model
        self.model_name = "XGBoost Fraud Detection Model"  # Name of the model

    # Method to predict fraud based on transaction data
    def predict(self, data: pd.DataFrame) -> Tuple[bool, str, float]:
        """
        Predict if a transaction is fraudulent
        """
        try:
            # Make a copy of the data to avoid modifying the input
            data_copy = data.copy()
            
            # Explicit type conversions
            data_copy["transaction_amount"] = data_copy["transaction_amount"].astype(float)
            data_copy["is_nighttime"] = data_copy["is_nighttime"].astype(str)
            data_copy["category"] = data_copy["category"].astype(str)
            data_copy["transaction_location"] = data_copy["transaction_location"].astype(str)
            data_copy["job"] = data_copy["job"].astype(str)
            data_copy["state"] = data_copy["state"].astype(str)
            
            # Preprocess the data 
            processed_data = self.preprocessor.transform(data_copy)
            
            # Predict fraud in the transaction
            fraud_probability = self.model.predict_proba(processed_data)[:, 1]
            is_fraud = fraud_probability[0] >= self.threshold
            label = "Fraud" if is_fraud else "Normal"
            
            # Return results
            return bool(is_fraud), label, float(fraud_probability[0])
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            # Include data shapes in error
            error_msg = f"Prediction error: {str(e)}, Data shape: {data.shape}, Columns: {list(data.columns)}"
            raise Exception(error_msg)
    

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the fraud detection model
        
        Returns:
            Dictionary containing model information
        """
        return {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "threshold": self.threshold
        }
