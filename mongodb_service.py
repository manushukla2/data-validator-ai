try:
    import pymongo
    import gridfs
    from pymongo.errors import ServerSelectionTimeoutError
    from bson import ObjectId
    MONGODB_AVAILABLE = True
    print("✅ MongoDB packages loaded successfully")
except ImportError as e:
    print(f"MongoDB packages not available: {e}")
    MONGODB_AVAILABLE = False
    ObjectId = None
    
from datetime import datetime
import io
import pandas as pd

class MongoDBService:
    def __init__(self, connection_string="mongodb://localhost:27017/", database_name="pfrda_ai_validator"):
        """
        Initialize MongoDB connection
        """
        if not MONGODB_AVAILABLE:
            print("⚠️ MongoDB packages not available. Database features disabled.")
            self.client = None
            return
            
        try:
            self.client = pymongo.MongoClient(connection_string)
            self.db = self.client[database_name]
            self.fs = gridfs.GridFS(self.db)
            
            # Collections
            self.files_collection = self.db.uploaded_files
            self.validations_collection = self.db.validation_results
            self.ai_responses_collection = self.db.ai_responses
            
            # Test connection
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB database: {database_name}")
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            self.client = None
    
    def store_uploaded_file(self, file_content, filename, file_type, sheet_data=None):
        """
        Store uploaded file in GridFS and metadata in collection
        """
        if not self.client:
            return None
            
        try:
            # Store file in GridFS
            file_id = self.fs.put(
                file_content, 
                filename=filename,
                upload_date=datetime.utcnow(),
                content_type=file_type
            )
            
            # Store metadata
            file_doc = {
                "_id": file_id,
                "filename": filename,
                "file_type": file_type,
                "upload_date": datetime.utcnow(),
                "file_size": len(file_content),
                "sheets": list(sheet_data.keys()) if sheet_data else [],
                "sheet_info": {
                    sheet: {
                        "rows": len(df),
                        "columns": len(df.columns),
                        "column_names": df.columns.tolist()
                    } for sheet, df in sheet_data.items()
                } if sheet_data else {}
            }
            
            self.files_collection.insert_one(file_doc)
            print(f"✅ Stored file: {filename} with ID: {file_id}")
            return str(file_id)
            
        except Exception as e:
            print(f"❌ Error storing file: {e}")
            return None
    
    def store_validation_results(self, file_id, sheet_name, validation_summary, failed_rules):
        """
        Store validation results
        """
        if not self.client:
            return None
            
        try:
            validation_doc = {
                "file_id": file_id,
                "sheet_name": sheet_name,
                "validation_date": datetime.utcnow(),
                "validation_summary": validation_summary,
                "failed_rules": failed_rules,
                "total_failures": len(failed_rules) if failed_rules else 0,
                "status": "failed" if failed_rules else "passed"
            }
            
            result = self.validations_collection.insert_one(validation_doc)
            print(f"✅ Stored validation results for sheet: {sheet_name}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"❌ Error storing validation results: {e}")
            return None
    
    def store_ai_response(self, file_id, sheet_name, response_type, prompt, ai_response, model_used="mistral"):
        """
        Store AI-generated responses
        """
        if not self.client:
            return None
            
        try:
            ai_doc = {
                "file_id": file_id,
                "sheet_name": sheet_name,
                "response_type": response_type,  # "validation_explanation" or "data_summary"
                "prompt": prompt,
                "ai_response": ai_response,
                "model_used": model_used,
                "generated_date": datetime.utcnow(),
                "response_length": len(ai_response) if ai_response else 0
            }
            
            result = self.ai_responses_collection.insert_one(ai_doc)
            print(f"✅ Stored AI response for sheet: {sheet_name}, type: {response_type}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"❌ Error storing AI response: {e}")
            return None
    
    def get_file_history(self, limit=10):
        """
        Get recent file upload history
        """
        if not self.client:
            return []
            
        try:
            files = list(self.files_collection.find().sort("upload_date", -1).limit(limit))
            return files
        except Exception as e:
            print(f"❌ Error getting file history: {e}")
            return []
    
    def get_validation_history(self, file_id=None, limit=10):
        """
        Get validation history
        """
        if not self.client:
            return []
            
        try:
            query = {"file_id": file_id} if file_id else {}
            validations = list(self.validations_collection.find(query).sort("validation_date", -1).limit(limit))
            return validations
        except Exception as e:
            print(f"❌ Error getting validation history: {e}")
            return []
    
    def get_ai_responses_history(self, file_id=None, limit=10):
        """
        Get AI responses history
        """
        if not self.client:
            return []
            
        try:
            query = {"file_id": file_id} if file_id else {}
            responses = list(self.ai_responses_collection.find(query).sort("generated_date", -1).limit(limit))
            return responses
        except Exception as e:
            print(f"❌ Error getting AI responses history: {e}")
            return []
    
    def get_file_content(self, file_id):
        """
        Retrieve file content from GridFS
        """
        if not self.client or not MONGODB_AVAILABLE:
            return None
            
        try:
            if MONGODB_AVAILABLE:
                file_obj = self.fs.get(ObjectId(file_id))
                return file_obj.read()
        except Exception as e:
            print(f"❌ Error retrieving file content: {e}")
            return None
    
    def close_connection(self):
        """
        Close MongoDB connection
        """
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")
