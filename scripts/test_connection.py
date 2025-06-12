import os
from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv # type: ignore
import ssl

load_dotenv()

def test_connection():
    # Get connection string from environment variable
    mongodb_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    
    if not mongodb_uri:
        print("Error: MONGO_URI environment variable not found")
        return
    
    try:
        print(f"Attempting connection to MongoDB with URI: {mongodb_uri}")
        
        # Create client with explicit SSL context
        client = MongoClient(mongodb_uri)
        
        db = client[db_name]
        
        # Test connection with a ping command
        db.command('ping')
        print("MongoDB connection successful!")
        
        # List collections (if any)
        collections = db.list_collection_names()
        if collections:
            print(f"Collections in database: {', '.join(collections)}")
        else:
            print("Database exists but has no collections")
        
        client.close()
        
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()