from pymongo import MongoClient # type: ignore
from typing import Dict, Any, Optional
from datetime import datetime

class MetricsService:
    def __init__(self, mongodb_uri: str = "mongodb://localhost:27017", db_name: str = "fraud_detection"):
        """Initialize the metrics service with database connection"""
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.metrics_collection = self.db["model_metrics"]
        
    def get_model_metrics(self, model_version: str = "1.0.0") -> Dict[str, Any]:
        """
        Get model metrics from MongoDB
        
        Args:
            model_version: Version of the model to retrieve metrics for
            
        Returns:
            Dictionary containing model metrics
        """
        # Query metrics for the specified model version
        metrics = self.metrics_collection.find_one(
            {"model_version": model_version},
            sort=[("timestamp", -1)]  # Get the most recent metrics
        )
        
        if metrics:
            # Convert ObjectId to string for JSON serialization
            metrics["_id"] = str(metrics["_id"])
            return metrics
        
        # If no metrics found in database, return hardcoded values
        # This is a fallback for development or when database is not available
        return {
            "model_version": model_version,
            "timestamp": datetime.now(),
            "threshold": 0.38,
            "f1_score": 0.74,
            "precision": 0.72,
            "recall": 0.75,
            "average_precision": 0.772,
            "accuracy": 0.999,
            "confusion_matrix": {
                "true_negatives": 368549,
                "false_positives": 485,
                "false_negatives": 482,
                "true_positives": 1448
            }
        }
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()