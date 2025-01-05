from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

#mock api key placeholder (change karlena bhai varna l lagne wala hai)
API_KEY = os.getenv("API_KEY", "mock_api_key_placeholder")

ROUTING_ENDPOINTS = {
    "fire": "https://api.exotel.com/route/fire",
    "medical": "https://api.exotel.com/route/medical",
    "police": "https://api.exotel.com/route/police"
}


# -------------------------------
# 📊 Health Check Endpoint
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "Server is running"}


# -------------------------------
# 📞 Exotel Webhook for Incoming Calls
# -------------------------------
@app.post("/exotel-webhook")
async def exotel_webhook(
    CallSid: str = Form(...),
    CallerID: str = Form(...),
    RecordingUrl: str = Form(...)
):
    """
    Handle incoming webhook requests from Exotel Passthru Applet.
    """
    print(f"Incoming Call: SID={CallSid}, CallerID={CallerID}, Recording={RecordingUrl}")
    
    try:
        # Forward audio to Hume AI for processing
        hume_response = requests.post(
            "https://api.hume.ai/v1/stream/phone",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "caller_id": CallerID,
                "audio_stream": RecordingUrl
            }
        )
        hume_response.raise_for_status()
        print("Audio forwarded to Hume AI successfully.")
    
    except requests.exceptions.RequestException as e:
        print("Error forwarding to Hume AI:", e)
        raise HTTPException(status_code=500, detail="Failed to forward to Hume AI")
    
    return {"status": "Audio sent to Hume AI"}


# -------------------------------
# 📝 Transcript Processing from Hume AI
# -------------------------------
class Transcript(BaseModel):
    transcript: str
    caller_id: str


@app.post("/transcript")
async def process_transcript(data: Transcript):
    """
    Process real-time transcripts from Hume AI and trigger call routing.
    """
    transcript = data.transcript.lower()
    caller_id = data.caller_id
    print("Transcript received:", transcript)

    if "connecting you to the fire department" in transcript:
        await trigger_routing("fire", caller_id)
    elif "connecting you to medical services" in transcript:
        await trigger_routing("medical", caller_id)
    elif "connecting you to the police department" in transcript:
        await trigger_routing("police", caller_id)
    else:
        print("No routing trigger detected.")
    
    return {"status": "Transcript processed"}


# -------------------------------
# 📡 Routing Function to Exotel
# -------------------------------
async def trigger_routing(department: str, caller_id: str):
    """
    Route the call to the specified department via Exotel API.
    """
    try:
        print(f"Routing call to: {department}")
        
        payload = {
            "From": caller_id,
            "To": ROUTING_ENDPOINTS[department],
            "CallerId": "your-caller-id",
            "Url": f"https://your-backend-url/ivr/{department}"
        }

        response = requests.post(
            "https://api.exotel.com/v1/Accounts/your-exotel-sid/Calls/connect.json",
            auth=(API_KEY, ""),
            data=payload
        )
        response.raise_for_status()
        print("Routing successful:", response.json())
        return {"status": "success", "message": f"Call routed to {department}"}
    
    except requests.exceptions.RequestException as e:
        print("Routing failed:", str(e))
        raise HTTPException(status_code=500, detail="Routing failed")
