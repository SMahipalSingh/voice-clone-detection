# VoiceShield: AI Voice Clone & Deepfake Detection Platform
### Complete System Architecture, Design Specification & DFD (Level 0 – 1)

---

## 1. Executive Project Overview

**VoiceShield** is an enterprise-grade cyber-forensic platform designed to detect **AI-synthesized voice clones, commercial Text-to-Speech (TTS), and physical replay attacks** in real-time, while establishing an immutable, tamper-evident **SHA-256 Blockchain Audit Ledger** for every forensic scan.

### The Core Problem Solved:
* **Generative Voice Clones (ElevenLabs, RVC, VALL-E):** Highly realistic vocal duplication used in CEO fraud, banking authorization bypass, and social engineering.
* **Commercial Neural TTS (Google Cloud, Amazon Polly, OpenAI):** Clean synthetic speech designed to fool human listeners and standard classifiers.
* **Acoustic Spoofing & Replay (ASVspoof Attacks):** Recorded human audio played back through loudspeakers to spoof biometric voiceprint systems.
* **Chain-of-Custody & Auditability:** Need for cryptographically verifiable, non-repudiable proof that an audio file was scanned, timestamped, and unaltered.

---

## 2. Technology Stack & Frameworks

| Layer / Subsystem | Technologies & Libraries | Purpose & Key Responsibilities |
| :--- | :--- | :--- |
| **Frontend UI / UX** | **React 18, Vite, Vanilla CSS, Lucide Icons** | Ultra-responsive glassmorphic cyber-dashboard, native Web Audio API visualizers, dynamic SVG threat gauge. |
| **Audio Ingestion** | **Native Browser `MediaRecorder` API, Web Audio API** | Real-time studio microphone capture at native sample rates (48 kHz mono PCM) and lossless audio file uploads. |
| **Backend REST API** | **FastAPI, Uvicorn, Pydantic, Python 3.10+** | High-performance asynchronous REST microservice, multi-part form data processing, and endpoint routing. |
| **Acoustic Feature Extraction** | **Librosa, SoundFile, PyDub, NumPy, SciPy** | 147-dimensional forensic feature extraction, fast autocorrelation $F_0$ pitch tracking, spectral dynamics. |
| **Machine Learning & AI** | **Scikit-Learn, PyTorch, Hugging Face Transformers, Joblib** | Calibrated Soft-Voting Ensemble (Random Forest + Gradient Boosting) + Pretrained Wav2Vec2 deep neural embeddings. |
| **Security & Cryptography** | **Python `hashlib` (SHA-256), JSON serialization** | Proof-of-Integrity blockchain engine, block hashing, Merkle-linked payload signatures. |
| **Datasets & Training** | **ASVspoof 2021 PA Dataset, Google TTS Engine (`gTTS`)** | 2,217+ balanced multi-accent audio files (1,000 Real + 1,000 ASV Spoof + 217 Commercial TTS). |

---

## 3. High-Level System Architecture

```mermaid
flowchart TB
    subgraph ClientLayer ["1. Client & Presentation Layer (React 18 + Vite)"]
        UI_Upload["Audio File Uploader (.wav, .mp3, .flac)"]
        UI_Mic["Live Studio Microphone Recorder (Web Audio API)"]
        UI_Gauge["Dynamic Threat Gauge & Radial Risk Meter"]
        UI_Metrics["Acoustic Telemetry Grid (Jitter, Rolloff, Flatness)"]
        UI_Ledger["Blockchain Explorer & Integrity Verifier"]
        UI_History["Forensic History Table & Deletion Service"]
    end

    subgraph APILayer ["2. API & Gateway Layer (FastAPI Backend)"]
        API_Analyze["POST /analyze-audio (Multipart Form-Data)"]
        API_Ledger["GET /ledger & GET /ledger/verify"]
        API_History["GET /history & DELETE /history"]
        API_Health["GET /health"]
    end

    subgraph MLEngine ["3. Cyber-Forensic ML & Acoustic Engine"]
        FE["Feature Extractor (147-D Vector)"]
        PitchTracker["Vectorized Autocorrelation Pitch Tracker (F0 & Jitter)"]
        SpectralEngine["Spectral Damping & Flatness Analyzer"]
        
        subgraph Models ["Ensemble Models"]
            RF_GB["Calibrated Soft-Voting Classifier (RF + GB on ASVspoof + TTS)"]
            Wav2Vec["Deep Learning Transformer (Wav2Vec2 Embeddings)"]
        end
        
        Fusion["Continuous Multi-Factor Decision Fusion Engine"]
    end

    subgraph SecurityLayer ["4. Cryptographic Blockchain & Audit Trail"]
        AudioHasher["SHA-256 Audio Payload Fingerprinter"]
        BlockEngine["Chained Block Generator (H_i = SHA-256(i + PrevHash + Payload))"]
        LedgerStore["ledger.json (Immutable Distributed State)"]
        HistoryStore["history.json (Persistent Scan Records)"]
    end

    UI_Upload --> API_Analyze
    UI_Mic --> API_Analyze
    UI_Ledger --> API_Ledger
    UI_History --> API_History

    API_Analyze --> FE
    FE --> PitchTracker & SpectralEngine
    PitchTracker & SpectralEngine --> RF_GB & Wav2Vec
    RF_GB & Wav2Vec --> Fusion

    Fusion --> AudioHasher
    AudioHasher --> BlockEngine
    BlockEngine --> LedgerStore & HistoryStore

    Fusion --> API_Analyze
    BlockEngine --> API_Analyze
    API_Analyze --> UI_Gauge & UI_Metrics & UI_Ledger
```

---

## 4. Data Flow Diagrams (DFD)

### 4.1. DFD Level 0 — Context Diagram

```mermaid
flowchart LR
    User["Security Analyst / User"]
    Mic["Microphone / Audio Source"]
    System(("0.0 <br/> VoiceShield <br/> AI Voice Clone & <br/> Deepfake Detection System"))
    
    User -->|"Upload Audio File (.wav, .mp3, .flac)"| System
    Mic -->|"Stream Live Voice Recording (Blob)"| System
    User -->|"Query / Verify Ledger Integrity"| System
    User -->|"Clear / View Scan History"| System

    System -->|"Forensic Risk Score (0-100%) & Threat Tier"| User
    System -->|"Acoustic Frequency Telemetry (Jitter, Rolloff, Flatness)"| User
    System -->|"SHA-256 Cryptographic Block Certificate"| User
    System -->|"Audit Ledger Status (VALID / COMPROMISED)"| User
```

---

### 4.2. DFD Level 1 — Detailed Functional Decomposition

```mermaid
flowchart TB
    User(["Security Analyst / User"])
    
    subgraph Process1 ["1.0 Audio Ingestion & Decoding"]
        P1["Receive Audio Stream / File <br/> Resample to 16 kHz Mono PCM <br/> Trim Leading/Trailing Silence"]
    end
    
    subgraph Process2 ["2.0 Acoustic Feature Extraction"]
        P2["Compute 147 Forensic Features: <br/> • 60 MFCCs + Deltas + Delta-Deltas <br/> • Vectorized Autocorrelation F0 Tracking <br/> • Pitch Micro-Jitter Index <br/> • Spectral Flatness & 7-Band Contrast <br/> • High-Frequency Rolloff & Centroid"]
    end

    subgraph Process3 ["3.0 Multi-Factor Decision Fusion"]
        P3["Execute Calibrated Classifier (RF + GB) <br/> Run Wav2Vec2 Neural Deepfake Transformer <br/> Synthesize Multi-Factor Risk Score (0.05 - 0.96)"]
    end

    subgraph Process4 ["4.0 Blockchain Ledger Generation"]
        P4["Calculate SHA-256 of Raw Audio Payload <br/> Construct Block Header (Index, Timestamp, PrevHash) <br/> Compute Cryptographic Block Hash <br/> Append to Immutable Ledger"]
    end

    subgraph Process5 ["5.0 Audit & History Persistence"]
        P5["Record Scan Entry in history.json <br/> Update Blockchain Ledger State in ledger.json"]
    end

    subgraph Process6 ["6.0 Telemetry & UI Dashboard Visualization"]
        P6["Render Radial Threat Gauge (0-100%) <br/> Display Acoustic Telemetry Grid <br/> Render Block Audit Badge & Recommendations"]
    end

    DS1[("Data Store 1: <br/> Trained ML Model <br/> (custom_classifier.pkl)")]
    DS2[("Data Store 2: <br/> Immutable Ledger <br/> (backend/db/ledger.json)")]
    DS3[("Data Store 3: <br/> Forensic History <br/> (backend/db/history.json)")]

    User -->|"1. Raw Audio (File/Mic)"| P1
    P1 -->|"2. Clean 16kHz PCM Array (y, sr)"| P2
    P2 -->|"3. 147-D Vector + Metric Dict"| P3
    DS1 -->|"Trained Weights / Estimators"| P3
    P3 -->|"4. Verdict, Risk %, Acoustic Indices"| P4
    P4 -->|"5. Minted Block & Cryptographic Hash"| P5
    P5 -->|"Save Block"| DS2
    P5 -->|"Save Scan Record"| DS3
    P4 & P3 -->|"6. Complete Forensic Payload"| P6
    P6 -->|"7. Interactive Visual Telemetry"| User
```

---

## 5. Detailed System Design & Core Modules

### 5.1. Audio Feature Extraction Pipeline ([`features.py`](file:///c:/Users/smsas/voice-clone-detection/ml-model/src/features.py))
1. **MFCCs + 1st/2nd Order Derivatives (60 dims):** Tracks formant transitions and spectral envelope trajectories over time.
2. **Vectorized Autocorrelation Pitch Tracker (15ms execution):** Computes fundamental frequencies ($F_0$) over $[65\text{ Hz}, 500\text{ Hz}]$ and calculates cycle-to-cycle **Pitch Micro-Jitter**:
   $$\text{Jitter} = \frac{\frac{1}{N-1}\sum_{t=1}^{N-1} |F_0(t+1) - F_0(t)|}{\bar{F}_0}$$
3. **Spectral Flatness ($2\text{ dims}$):** Quantifies harmonic sharpness vs. vocoder noise smoothing.
4. **7-Band Spectral Contrast ($14\text{ dims}$):** Measures peak-to-valley energy across 7 octave sub-bands.
5. **Spectral Rolloff ($2\text{ dims}$):** Identifies low-pass cutoff frequencies ($2.8\text{ kHz}-3.2\text{ kHz}$).
6. **Zero-Crossing Rate & RMS Energy ($4\text{ dims}$):** Evaluates voiced-to-unvoiced transitions and organic breath decays.

---

### 5.2. Multi-Factor AI Inference Engine ([`predict.py`](file:///c:/Users/smsas/voice-clone-detection/ml-model/src/predict.py))
* **ASVspoof + Commercial TTS Trained Ensemble:** Calibrated Random Forest + Gradient Boosting soft-voting classifier.
* **Pretrained Wav2Vec2 Deep Transformer:** Evaluates acoustic neural embeddings.
* **Physical Frequency Telemetry:** Verifies human biological micro-tremor and wideband harmonic resonance.

---

### 5.3. Cryptographic Blockchain Audit Ledger ([`ledger_service.py`](file:///c:/Users/smsas/voice-clone-detection/backend/services/ledger_service.py))
Every audio scan is minted into an immutable chained ledger:
$$H_i = \text{SHA256}(\text{Index} + \text{PrevHash} + \text{Timestamp} + \text{AudioSHA256} + \text{RiskScore})$$

---

## 6. Acoustic Forensic Metric Reference

| Acoustic Metric | Biological Human Voice | Commercial TTS / AI Clone | Forensic Significance |
| :--- | :--- | :--- | :--- |
| **Pitch Micro-Jitter** | $0.015 - 0.045$ (organic tremor) | $< 0.008$ (rigid spline) | Involuntary muscle vibrations cannot be fully replicated by vocoders. |
| **Spectral Rolloff** | $> 3.5\text{ kHz} - 8.0\text{ kHz}$ | $< 2.8\text{ kHz} - 3.2\text{ kHz}$ | Low-pass Nyquist cutoff applied by TTS pipelines to suppress aliasing noise. |
| **Spectral Flatness** | Low to Moderate ($0.0001 - 0.001$) | Elevated / Uniform ($> 0.01$) | Neural vocoders create unnaturally smooth harmonic spectra across high bands. |
| **Spectral Contrast** | $15\text{ dB} - 45\text{ dB}$ (dynamic peaks) | $10\text{ dB} - 22\text{ dB}$ (compressed) | Human vocal cords produce sharp formant peaks; synthetic speech compresses this range. |

---

## 7. Execution & Running the Platform

1. **Backend Server (FastAPI):**
   ```bash
   .\venv\Scripts\uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
2. **Frontend Dashboard (Vite + React):**
   ```bash
   cd frontend
   npm run dev
   ```
3. **Open in Browser:** Access the live dashboard at **`http://localhost:5173/`**.
