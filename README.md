# VoiceShield — AI Voice Clone Detector & Blockchain Audit Registry

> **Generalized AI Voice Deepfake Detection with 147 Forensic Spectral Features & SHA-256 Blockchain Audit Layer**

![System Status](https://img.shields.io/badge/ML%20Status-Calibrated%20Ensemble-00f2fe)
![Blockchain](https://img.shields.io/badge/Ledger-SHA--256%20Immutable-8b5cf6)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-10b981)
![React](https://img.shields.io/badge/Frontend-Vite%20%2B%20React-f59e0b)

---

## Key Highlights

- **Multi-Spectral Forensic Feature Extraction (147 dimensions)**: Catches both **Replay Attacks** (ASVspoof 2021 PA) and **Neural Voice Clones** (ElevenLabs, RVC, Tortoise, HiFi-GAN vocoders) by evaluating pitch micro-jitter, spectral flatness, and Nyquist damping.
- **Cryptographic SHA-256 Blockchain Audit Trail**: Automatically mints tamper-evident blocks linking raw audio fingerprints (`audio_sha256`), risk scores, and forensic verdicts into an immutable chain.
- **Scenario Context Engine**: Context-specific threat profiling for **Bank Wire Transfers**, **CEO / Executive Spoofing**, **Emergency Ransom Scams**, and **Law Enforcement Impersonation**.
- **Interactive Cyber-Forensic Dashboard**: Built-in 1-click benchmark evaluation samples, live microphone recording with real-time waveform visualizer, and a full Blockchain Ledger explorer with cryptographic chain auditing.

---

## Project Structure

```
voice-clone-detection/
├── backend/
│   ├── main.py                     # FastAPI Application Entry
│   ├── db/
│   │   └── database.py             # SQLite persistence layer
│   ├── routers/
│   │   ├── analyze.py              # /analyze-audio, /sample-audios
│   │   ├── history.py              # /history endpoints
│   │   └── ledger.py               # /ledger & /ledger/verify endpoints
│   ├── sample_audio/               # Built-in Real & Synthetic Test Audio Samples
│   └── services/
│       ├── ledger_service.py       # SHA-256 Blockchain ledger engine
│       └── risk_scoring.py         # Scenario context scoring engine
│
├── ml-model/
│   ├── data/                       # Raw & Processed Training Sets
│   ├── models/
│   │   ├── custom_classifier.pkl   # Calibrated Random Forest + Gradient Boosting Ensemble
│   │   └── model_metadata.json     # Performance metrics & training telemetry
│   └── src/
│       ├── features.py             # 147-dim MFCC, Flatness, Jitter, Rolloff extractor
│       ├── build_dataset.py        # Adaptive loader & stratified dataset builder
│       ├── generate_samples.py     # Acoustic voice & vocoder simulator
│       ├── train.py                # Ensemble training pipeline
│       └── predict.py              # Production inference engine
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Live header with node status & pitch guide
│   │   │   ├── AudioUploader.jsx   # Drag-drop, live mic, & preset test matrix
│   │   │   ├── RiskGauge.jsx       # Glowing radial risk meter
│   │   │   ├── AlertBanner.jsx     # Security alert & action guidance
│   │   │   ├── AcousticMetrics.jsx # Forensic feature telemetry cards
│   │   │   ├── LedgerView.jsx      # Blockchain Explorer & Cryptographic Audit
│   │   │   ├── HistoryTable.jsx    # SQLite Persistent Scan Logs
│   │   │   └── PitchModal.jsx      # Technical presentation helper
│   │   ├── services/api.js         # API integration client
│   │   ├── App.jsx                 # Main state coordinator
│   │   └── index.css               # Cyber-forensic design system
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── PROJECT_CONTEXT.md          # In-depth architectural & pitch guide
└── scripts/
    └── download_kaggle.py          # Automated Kaggle dataset downloader
```

---

## Quickstart & Execution Guide

### 1. Start the Backend Server (Port 8000)

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Run FastAPI Backend
uvicorn backend.main:app --reload --port 8000
```
Backend will be available at: `http://localhost:8000` (Swagger docs at `/docs`)

---

### 2. Start the Frontend Dashboard (Port 5173)

```bash
cd frontend
npm run dev
```
Open your browser at: `http://localhost:5173`

---

## Kaggle Dataset Integration

To train or benchmark on the official Kaggle dataset (**Balanced ASVspoof 2021 PA** `abdallamohamed312/ready-to-input-for-training`):

1. Place your `kaggle.json` API token into `~/.kaggle/kaggle.json`.
2. Run the automated download script:
   ```bash
   python scripts/download_kaggle.py
   ```
3. Re-train the model:
   ```bash
   python ml-model/src/train.py
   ```

---

## Testing & Validation Checklist

- [x] **Real Voice Classification**: Test with `legitimate_ceo_voice.wav` -> Evaluates to **SAFE** (Risk < 25%).
- [x] **AI Clone Classification**: Test with `ai_clone_emergency_scam.wav` -> Evaluates to **SUSPICIOUS / CLONE DETECTED** (Risk > 90%).
- [x] **Live Microphone Recording**: Record voice in real-time with dynamic audio visualizer and run instant scan.
- [x] **Blockchain Audit**: Click **"Run Cryptographic Audit"** in the Ledger View to verify all SHA-256 hashes across the chain.
- [x] **SQLite History**: Scans persist in `backend/db/history.db` and display in the History Table.
