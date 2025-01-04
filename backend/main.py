from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI()


# Mock the API_KEY if not available
API_KEY = os.getenv("API_KEY", "mock_api_key_placeholder")

ROUTING_ENDPOINTS = {
    "fire": "https://api.exotel.com/route/fire",
    "medical": "https://api.exotel.com/route/medical",
    "police": "https://api.exotel.com/route/police"
}

# Data Model for Transcript
class Transcript(BaseModel):
    transcript: str

# Health Check
@app.get("/health")
def health_check():
    return {"status": "Server is running"}

# Transcript Analysis
@app.post("/transcript")
async def process_transcript(data: Transcript):
    transcript = data.transcript.lower()
    print("Transcript received:", transcript)

    if "connecting you to the fire department" in transcript:
        await trigger_routing("fire")
    elif "connecting you to medical services" in transcript:
        await trigger_routing("medical")
    elif "connecting you to the police department" in transcript:
        await trigger_routing("police")
    else:
        print("No routing trigger detected.")
    
    return {"status": "Transcript processed"}

# Routing Function
async def trigger_routing(department: str):
    try:
        print(f"Routing call to: {department}")
        
        # Mocking the response
        mock_response = {
            "status": "success",
            "message": f"Call routed to {department}"
        }

        # Simulate success
        print("Routing successful:", mock_response)
        return mock_response
    
    except Exception as e:
        print("Routing failed:", str(e))
        raise HTTPException(status_code=500, detail="Routing failed")


