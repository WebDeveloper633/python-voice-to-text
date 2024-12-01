import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL (adjust if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY_VOICE"))
model_name = "whisper-large-v3-turbo"

# Function to convert audio file to text using Groq's API
def audio_to_text(file, filename):
    translation = client.audio.transcriptions.create(
        file=(filename, file.read()),  # Use the actual file name and binary data
        model=model_name,
        response_format="verbose_json",
    )
    return translation.text

# FastAPI endpoint to receive audio and return transcription
@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Use the original file name for the transcription
        transcription_text = audio_to_text(file.file, file.filename)
        return JSONResponse(content={"transcription": transcription_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Run the app with: uvicorn filename:app --reload
