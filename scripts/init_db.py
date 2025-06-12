import os 
import sys
from pymongo import MongoClient  # type: ignore
from dotenv import load_dotenv  # type: ignore
import traceback

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

def init_db():
    try:
        # Get MongoDB connection setting
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable not set")

        db_name = os.getenv("MONGODB_DB", "fraud_detection")

        # Connect to MongoDB database safely
        with MongoClient(mongodb_uri) as client:
            db = client[db_name]

            # Test connection 
            db.command('ping')
            print("MongoDB connection successful!")

            # Initialize model metrics collections 
            metrics_collection = db["metric_scores"]

            metrics_data = {
                "model_version": "1.0.0",
                "f1_score": 0.74,
                "precision": 0.72,
                "recall": 0.75,
                "average_precision": 0.78,
            }

            result = metrics_collection.insert_one(metrics_data)
            print(f"Inserted metrics data with ID: {result.inserted_id}")

            metrics_collection.create_index("model_version")
            print("Index on model_version created successfully.")

        print("Database initialized successfully.")
        return True

    except Exception:
        print("Error initializing database:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
