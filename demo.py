#!/usr/bin/env python3
"""
Demo script for PFRDA AI Validator with MongoDB integration
"""

import os
import sys
from datetime import datetime

def install_mongodb_docker():
    """
    Install MongoDB using Docker
    """
    print("🐳 Setting up MongoDB with Docker...")
    
    docker_commands = [
        "docker pull mongo:latest",
        "docker run -d --name pfrda-mongodb -p 27017:27017 -v pfrda-mongo-data:/data/db mongo:latest"
    ]
    
    for cmd in docker_commands:
        print(f"Running: {cmd}")
        os.system(cmd)
    
    print("✅ MongoDB is now running on localhost:27017")
    print("📁 Data will persist in Docker volume: pfrda-mongo-data")

def test_mongodb_connection():
    """
    Test MongoDB connection
    """
    try:
        from mongodb_service import MongoDBService
        
        print("🔍 Testing MongoDB connection...")
        mongo_service = MongoDBService()
        
        if mongo_service.client:
            print("✅ MongoDB connection successful!")
            
            # Test basic operations
            test_data = {
                "test": True,
                "timestamp": datetime.utcnow(),
                "message": "PFRDA AI Validator Test"
            }
            
            collection = mongo_service.db.test_collection
            result = collection.insert_one(test_data)
            print(f"✅ Test document inserted with ID: {result.inserted_id}")
            
            # Clean up test data
            collection.delete_one({"_id": result.inserted_id})
            print("✅ Test cleanup completed")
            
            mongo_service.close_connection()
            return True
        else:
            print("❌ Failed to connect to MongoDB")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB test failed: {e}")
        return False

def show_features():
    """
    Display available features
    """
    print("\n🎯 PFRDA AI Validator Features:")
    print("=" * 50)
    
    features = [
        "📄 Multi-sheet Excel/CSV file processing",
        "✅ Data validation against SRS specifications", 
        "🤖 AI-powered validation explanations (via Ollama/Mistral)",
        "📊 Intelligent data summarization",
        "🗄️ MongoDB storage for files and responses",
        "📈 Historical validation tracking",
        "🔍 Searchable AI response archive",
        "🌐 Web-based Streamlit interface"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n🚀 Getting Started:")
    print("=" * 50)
    print("1. Ensure Ollama is running: `ollama serve`")
    print("2. Start MongoDB (optional): `docker run -d -p 27017:27017 mongo`")
    print("3. Run the app: `streamlit run app.py`")
    print("4. Upload your SRS and data files")
    print("5. View AI-powered validation results!")

def main():
    """
    Main demo function
    """
    print("🏦 PFRDA AI Model Demo Setup")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "mongodb":
            install_mongodb_docker()
        elif command == "test":
            test_mongodb_connection()
        elif command == "features":
            show_features()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: mongodb, test, features")
    else:
        show_features()
        print("\n💡 Pro tip: Run `python demo.py mongodb` to set up MongoDB with Docker")

if __name__ == "__main__":
    main()
