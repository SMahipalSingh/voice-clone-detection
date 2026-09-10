import os
import sys
import uuid
import shutil
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

# Include ML model src in import path
ML_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ml-model", "src"))
if ML_SRC not in sys.path:
    sys.path.insert(0, ML_SRC)

from predict import predict
from services.risk_scoring import compute_risk
from services.ledger_service import add_block, hash_audio_file
from db.database import save_history

router = APIRouter(tags=["Analysis"])

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
SAMPLE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_audio"))
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SAMPLE_DIR, exist_ok=True)

@router.post("/analyze-audio")
async def analyze_audio(
    audio: UploadFile = File(...),
    scenario: str = Form(default="General Call")
):
    """
    Forensic voice clone detection endpoint.
    Performs spectral extraction, calibrated ML inference, risk calculation,
    database logging, and blockchain audit block emission.
    """
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file uploaded.")

    # Generate unique filename
    ext = os.path.splitext(audio.filename)[1] or ".wav"
    temp_filename = f"{uuid.uuid4()}{ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        file_size_kb = round(os.path.getsize(temp_path) / 1024, 2)
        audio_sha256 = hash_audio_file(temp_path)

        # 1. Run ML Model Prediction & Spectral Extraction
        prediction = predict(temp_path)

        # 2. Context-Aware Risk Calculation
        risk = compute_risk(prediction["confidence"], scenario, prediction["metrics"])
        timestamp = datetime.now(timezone.utc).isoformat()

        # 3. Create Immutable Blockchain Audit Block
        block = add_block(
            risk_score=risk["risk_score"],
            verdict=risk["verdict"],
            timestamp=timestamp,
            filename=audio.filename,
            audio_sha256=audio_sha256,
            scenario=scenario
        )

        # 4. Save to SQLite Forensic History
        duration_sec = prediction["metrics"].get("duration_seconds", 0.0)
        save_history(
            filename=audio.filename,
            file_size_kb=file_size_kb,
            duration_sec=duration_sec,
            risk_score=risk["risk_score"],
            verdict=risk["verdict"],
            threat_tier=risk["threat_tier"],
            scenario=scenario,
            block_hash=block["hash"],
            audio_sha256=audio_sha256,
            timestamp=timestamp
        )

        return {
            "status": "success",
            "filename": audio.filename,
            "file_size_kb": file_size_kb,
            "duration_seconds": duration_sec,
            "confidence": prediction.get("confidence", 0.0),
            "raw_model_confidence": prediction.get("raw_model_confidence", prediction.get("confidence", 0.0)),
            "neural_deepfake_confidence": prediction.get("neural_deepfake_confidence", 0.0),
            "asvspoof_confidence": prediction.get("asvspoof_confidence", 0.0),
            "vocoder_anomaly_score": prediction.get("vocoder_anomaly_score", 0.0),
            "label": prediction.get("label", "real"),
            "is_cloned": prediction.get("is_cloned", False),
            "risk_score": risk.get("risk_score", 0),
            "verdict": risk.get("verdict", "safe"),
            "threat_tier": risk.get("threat_tier", "AUTHENTIC — LOW RISK"),
            "color_theme": risk.get("color_theme", "success"),
            "recommendation": risk.get("recommendation", ""),
            "forensic_summary": prediction.get("forensic_summary", ""),
            "metrics": prediction.get("metrics", {}),
            "scenario": scenario,
            "timestamp": timestamp,
            "blockchain": {
                "block_index": block["index"],
                "block_hash": block["hash"],
                "prev_hash": block["prev_hash"],
                "audio_sha256": audio_sha256,
                "signature_status": block["signature_status"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/sample-audios")
def list_sample_audios():
    """
    Returns pre-loaded audio files for 1-click instant UI testing.
    """
    samples = [
        {
            "id": "legitimate_ceo_voice.wav",
            "name": "Authentic Executive Voice",
            "type": "real",
            "description": "Legitimate executive phone conversation with organic pitch micro-jitter and vocal tract acoustics.",
            "expected_verdict": "SAFE"
        },
        {
            "id": "authentic_bank_customer.wav",
            "name": "Authentic Bank Customer",
            "type": "real",
            "description": "Genuine banking customer audio with natural acoustic breath dynamics and human prosody.",
            "expected_verdict": "SAFE"
        },
        {
            "id": "ai_clone_emergency_scam.wav",
            "name": "AI Cloned Voice — Emergency Scam",
            "type": "fake",
            "description": "Neural TTS cloned voice exhibit with rigid harmonic alignment and vocoder high-frequency cutoff.",
            "expected_verdict": "SUSPICIOUS / HIGH RISK"
        },
        {
            "id": "deepfake_wire_transfer_request.wav",
            "name": "Deepfake Wire Transfer Call",
            "type": "fake",
            "description": "Voice-converted deepfake impersonating a corporate executive demanding urgent wire transfer.",
            "expected_verdict": "SUSPICIOUS / HIGH RISK"
        }
    ]
    return {"samples": samples}


@router.get("/sample-audios/{sample_id}/audio")
def stream_sample_audio(sample_id: str):
    """Streams the preset sample audio for in-browser playback."""
    file_path = os.path.join(SAMPLE_DIR, sample_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample audio file not found")
    return FileResponse(file_path, media_type="audio/wav")
