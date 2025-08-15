import requests
import pandas as pd
from mongodb_service import MongoDBService

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"  # or "llama2" depending on what you pulled via ollama

# Initialize MongoDB service
mongo_service = MongoDBService()

def explain_validation_results(sheet_name, failed_rules, file_id=None):
    failures = "\n".join([f"- {r['column']}: {r['error']}" for r in failed_rules])
    prompt = f"""
You are a data validation assistant. Explain why the following fields failed validation in sheet '{sheet_name}' and what the user can do to fix them:

{failures}

Respond clearly and helpfully.
"""
    
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False})
        ai_response = response.json().get("response", "No explanation returned.")
        
        # Store AI response in MongoDB
        if file_id and mongo_service.client:
            mongo_service.store_ai_response(
                file_id=file_id,
                sheet_name=sheet_name,
                response_type="validation_explanation",
                prompt=prompt,
                ai_response=ai_response,
                model_used=MODEL
            )
        
        return ai_response
        
    except Exception as e:
        error_msg = f"Error getting AI explanation: {e}"
        print(error_msg)
        return error_msg

def summarize_data_sheet(df: pd.DataFrame, sheet_name: str, file_id=None):
    cols = df.columns.tolist()
    summary = f"This sheet '{sheet_name}' contains {len(df)} rows and {len(cols)} columns.\n\nColumns include: {', '.join(cols)}."
    sample_data = df.head(3).to_dict(orient="records")

    prompt = f"""
Given the sheet '{sheet_name}' with sample data:
{sample_data}

Explain what this data appears to represent and briefly describe each column.
"""
    
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False})
        ai_response = response.json().get("response", "No summary returned.")
        
        # Store AI response in MongoDB
        if file_id and mongo_service.client:
            mongo_service.store_ai_response(
                file_id=file_id,
                sheet_name=sheet_name,
                response_type="data_summary",
                prompt=prompt,
                ai_response=ai_response,
                model_used=MODEL
            )
        
        return ai_response
        
    except Exception as e:
        error_msg = f"Error getting AI summary: {e}"
        print(error_msg)
        return error_msg
