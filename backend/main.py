import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from db.database import init_db
from routers import analyze, history, ledger

# Initialize SQLite database on startup
init_db()

app = FastAPI(
    title="Voice Clone Detector & Blockchain Ledger",
    description="Forensic AI Voice Clone / Deepfake Detection System with SHA-256 Blockchain Audit Trail",
    version="1.0.0"
)

# Enable CORS for Frontend React integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
sample_dir = os.path.join(os.path.dirname(__file__), "sample_audio")
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(sample_dir, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
app.mount("/sample_audio", StaticFiles(directory=sample_dir), name="sample_audio")

# Include Routers
app.include_router(analyze.router)
app.include_router(history.router)
app.include_router(ledger.router)

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "Voice Clone Detector Engine",
        "version": "1.0.0",
        "blockchain_ledger": "ACTIVE",
        "database": "CONNECTED"
    }

@app.get("/")
def root():
    return {
        "message": "Voice Clone Detector API is running.",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
