# MongoDB Setup Instructions

## Option 1: Local MongoDB Installation

### Windows:
1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Install MongoDB with default settings
3. MongoDB will run on `mongodb://localhost:27017/` by default

### Using MongoDB with Docker (Recommended):
```bash
# Pull and run MongoDB container
docker run -d --name mongodb -p 27017:27017 mongo:latest

# To stop MongoDB
docker stop mongodb

# To start MongoDB again
docker start mongodb
```

## Option 2: MongoDB Atlas (Cloud)

1. Go to https://www.mongodb.com/atlas
2. Create a free account
3. Create a new cluster
4. Get your connection string
5. Update the `connection_string` in `mongodb_service.py`:

```python
mongo_service = MongoDBService(
    connection_string="mongodb+srv://username:password@cluster.mongodb.net/",
    database_name="pfrda_ai_validator"
)
```

## Database Structure

The application creates the following collections:

### 1. uploaded_files
- Stores file metadata and content using GridFS
- Tracks file upload date, size, and sheet information

### 2. validation_results
- Stores validation results for each sheet
- Links to uploaded files via file_id

### 3. ai_responses
- Stores all AI-generated responses
- Includes prompts, responses, and metadata

## Features

✅ **File Storage**: All uploaded files are stored in MongoDB GridFS
✅ **Validation History**: Track all validation results over time  
✅ **AI Response Archive**: Keep all AI explanations and summaries
✅ **Search & Retrieval**: Easy access to historical data
✅ **Data Analytics**: Analyze validation patterns and AI performance

## Usage Notes

- If MongoDB is not available, the application will still work but won't store data
- File storage uses GridFS for efficient handling of large files
- All timestamps are stored in UTC
- Database connection is tested on startup

## Troubleshooting

1. **Connection Issues**: Check if MongoDB is running on port 27017
2. **Permission Errors**: Ensure MongoDB has proper read/write permissions
3. **Memory Issues**: Large files might require adjusted MongoDB memory settings
