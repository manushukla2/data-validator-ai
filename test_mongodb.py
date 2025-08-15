# Test MongoDB Connection and Create Sample Data

import pandas as pd
from mongodb_service import MongoDBService
from datetime import datetime
import io

def test_mongodb_integration():
    print("🧪 Testing MongoDB Integration...")
    
    # Initialize MongoDB service
    mongo_service = MongoDBService()
    
    if not mongo_service.client:
        print("❌ MongoDB connection failed")
        return False
    
    print("✅ MongoDB connected successfully!")
    
    # Create sample data
    sample_data = {
        'Employee_ID': ['EMP001', 'EMP002', 'EMP003'],
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Pension_Contribution': [5000, 7500, 6200],
        'Salary': [50000, 75000, 62000],
        'Department': ['IT', 'Finance', 'HR']
    }
    
    df = pd.DataFrame(sample_data)
    print(f"📊 Created sample dataframe with {len(df)} rows")
    
    # Test file storage
    file_content = df.to_csv(index=False).encode('utf-8')
    file_id = mongo_service.store_uploaded_file(
        file_content=file_content,
        filename="sample_pension_data.csv",
        file_type="test_data",
        sheet_data={"Sheet1": df}
    )
    
    if file_id:
        print(f"✅ File stored with ID: {file_id}")
    else:
        print("❌ File storage failed")
        return False
    
    # Test validation results storage
    validation_summary = {
        "total_rows": len(df),
        "valid_rows": len(df) - 1,
        "invalid_rows": 1,
        "validation_score": 0.67
    }
    
    failed_rules = [
        {"column": "Pension_Contribution", "error": "Value below minimum threshold"}
    ]
    
    validation_id = mongo_service.store_validation_results(
        file_id=file_id,
        sheet_name="Sheet1",
        validation_summary=validation_summary,
        failed_rules=failed_rules
    )
    
    if validation_id:
        print(f"✅ Validation results stored with ID: {validation_id}")
    else:
        print("❌ Validation storage failed")
        return False
    
    # Test AI response storage
    sample_prompt = "Explain the pension contribution validation errors"
    sample_response = "The pension contribution failed validation because the minimum required contribution is ₹6000, but Employee EMP001 has only contributed ₹5000."
    
    ai_response_id = mongo_service.store_ai_response(
        file_id=file_id,
        sheet_name="Sheet1",
        response_type="validation_explanation",
        prompt=sample_prompt,
        ai_response=sample_response,
        model_used="mistral"
    )
    
    if ai_response_id:
        print(f"✅ AI response stored with ID: {ai_response_id}")
    else:
        print("❌ AI response storage failed")
        return False
    
    # Test data retrieval
    print("\n📋 Testing data retrieval...")
    
    file_history = mongo_service.get_file_history(limit=5)
    print(f"📁 Found {len(file_history)} files in history")
    
    validation_history = mongo_service.get_validation_history(limit=5)
    print(f"✅ Found {len(validation_history)} validation records")
    
    ai_history = mongo_service.get_ai_responses_history(limit=5)
    print(f"🤖 Found {len(ai_history)} AI responses")
    
    print("\n🎉 All MongoDB tests passed successfully!")
    print("💡 You can now upload files in the Streamlit interface and they will be stored in MongoDB")
    
    mongo_service.close_connection()
    return True

if __name__ == "__main__":
    test_mongodb_integration()
