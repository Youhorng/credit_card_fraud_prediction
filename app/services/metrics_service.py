import os
from typing import Dict, Any, Optional
from pymongo import MongoClient  # type: ignore
from dotenv import load_dotenv  # type: ignore
import traceback

# Load environment variables
load_dotenv()

class MetricsService:
    """
    Service for retrieving model metrics from MongoDB database
    """

    def __init__(self):
        """
        Initialize the MetricsService with MongoDB connection
        """
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("MONGODB_DB", "fraud_detection")

        self.client = None
        self.db = None

        self.connect()

    def connect(self):
        """
        Establish a connection to MongoDB
        """
        try:
            if not self.mongodb_uri:
                raise ValueError("MONGODB_URI environment variable not found")

            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.db_name]
            self.db.command('ping')
            print("MongoDB connection successful!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            traceback.print_exc()
            raise

    def get_model_metrics(self, model_version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            if self.db is None:
                raise Exception("Database connection not established")

            metrics_collection = self.db["metric_scores"]
            query = {"model_version": model_version} if model_version else {}
            metrics = metrics_collection.find_one(query)

            if metrics:
                metrics["_id"] = str(metrics["_id"])
                print(f"Retrieved metrics for model version {model_version}")
                return metrics

            return None

        except Exception as e:
            print(f"Error retrieving model metrics: {str(e)}")
            traceback.print_exc()
            return None


    def close(self):
        """
        Close the MongoDB connection
        """
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            print("MongoDB connection closed")

# Example usage:
metric = MetricsService()
result = metric.get_model_metrics("1.0.0")
print(result)  
metric.close()