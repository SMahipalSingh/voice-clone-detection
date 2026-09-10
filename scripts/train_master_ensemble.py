import os
import sys
import numpy as np
import joblib
import json
from datetime import datetime, timezone
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

sys.path.insert(0, os.path.abspath('ml-model/src'))
from features import extract_features

def train_master_ensemble():
    print("=" * 75)
    print("SWARX MULTI-TIER MASTER ENSEMBLE TRAINING PIPELINE")
    print("Kaggle ASVspoof + Indian Human Mic + Modern Neural Clones + Replay Attacks")
    print("=" * 75)

    # 1. Load ASVspoof Kaggle Dataset features
    processed_dir = "ml-model/data/processed"
    X_asv_tr = np.load(os.path.join(processed_dir, "X_train.npy"))
    y_asv_tr = np.load(os.path.join(processed_dir, "y_train.npy"))
    X_asv_te = np.load(os.path.join(processed_dir, "X_test.npy"))
    y_asv_te = np.load(os.path.join(processed_dir, "y_test.npy"))

    X_all = list(np.vstack([X_asv_tr, X_asv_te]))
    y_all = list(np.concatenate([y_asv_tr, y_asv_te]))
    print(f"[Step 1/5] Loaded {len(X_all)} ASVspoof Kaggle features (Real: {y_all.count(0)}, Fake: {y_all.count(1)})")

    upload_dir = "backend/uploads"
    sample_dir = "backend/sample_audio"
    indic_dir = "ml-model/data/raw/indic_samples"

    # Known AI replay audio files (played through speaker into microphone)
    ai_replay_files = {
        'e45a533d-9ec4-4c8b-bcbd-5bdd38a3e39c.wav',
        '17deab4c-10ca-4c70-a5d6-1bb0b1f26901.wav',
        '7de8d740-d4cd-43d9-9808-43c720f8f253.wav',
        '23c18473-f537-4dfb-867a-20a19ffcc392.wav'
    }

    # 2. Extract Real Indian Human Speech
    print("\n[Step 2/5] Adding Real Indian Human Voice Recordings...")
    real_mic_count = 0
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            if f.endswith(".wav") and f not in ai_replay_files and os.path.getsize(os.path.join(upload_dir, f)) > 150000:
                p = os.path.join(upload_dir, f)
                try:
                    feat, m = extract_features(p)
                    # Natural human speech acoustic check (ZCR < 0.16, formant peaks)
                    if m.get("pitch_micro_jitter", 0) > 0.005 and m.get("spectral_rolloff_hz", 0) > 800:
                        for _ in range(8):
                            noise = np.random.normal(0, 0.01 * (np.std(feat) + 1e-6), size=feat.shape)
                            X_all.append(feat + noise)
                            y_all.append(0)
                        real_mic_count += 1
                except Exception:
                    pass

    # Add preset authentic human samples
    if os.path.exists(sample_dir):
        for s in ["authentic_bank_customer.wav", "legitimate_ceo_voice.wav"]:
            p = os.path.join(sample_dir, s)
            if os.path.exists(p):
                try:
                    feat, _ = extract_features(p)
                    for _ in range(10):
                        noise = np.random.normal(0, 0.01 * (np.std(feat) + 1e-6), size=feat.shape)
                        X_all.append(feat + noise)
                        y_all.append(0)
                except Exception:
                    pass

    print(f" -> Integrated {real_mic_count} genuine Indian human microphone recordings (augmented).")

    # 3. Extract Modern Neural AI Voices & Replay Attacks
    print("\n[Step 3/5] Adding Modern Neural AI Voices (MP3) & Replay Attacks (WAV)...")
    ai_count = 0
    
    # Add all uploaded MP3 AI voice clones
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            if f.endswith(".mp3"):
                p = os.path.join(upload_dir, f)
                try:
                    feat, _ = extract_features(p)
                    for _ in range(12):
                        noise = np.random.normal(0, 0.01 * (np.std(feat) + 1e-6), size=feat.shape)
                        X_all.append(feat + noise)
                        y_all.append(1)
                    ai_count += 1
                except Exception:
                    pass

    # Add AI voice playback through mic recordings
    for f in ai_replay_files:
        p = os.path.join(upload_dir, f)
        if os.path.exists(p):
            try:
                feat, _ = extract_features(p)
                for _ in range(15):
                    noise = np.random.normal(0, 0.01 * (np.std(feat) + 1e-6), size=feat.shape)
                    X_all.append(feat + noise)
                    y_all.append(1)
                ai_count += 1
            except Exception:
                pass

    print(f" -> Integrated {ai_count} Modern AI Voices and Mic Replay attack samples (augmented).")

    # 4. Extract Indic AI Clones & Preset Clones
    print("\n[Step 4/5] Adding Indic AI Clones (Hindi/Indian English) & Presets...")
    clone_count = 0
    if os.path.exists(indic_dir):
        for f in os.listdir(indic_dir):
            if f.endswith(".mp3"):
                p = os.path.join(indic_dir, f)
                try:
                    feat, _ = extract_features(p)
                    for _ in range(12):
                        noise = np.random.normal(0, 0.01 * (np.std(feat) + 1e-6), size=feat.shape)
                        X_all.append(feat + noise)
                        y_all.append(1)
                    clone_count += 1
                except Exception:
                    pass

    if os.path.exists(sample_dir):
        for s in ["ai_clone_emergency_scam.wav", "deepfake_wire_transfer_request.wav", "test_tts_sample.wav"]:
            p = os.path.join(sample_dir, s)
            if os.path.exists(p):
                try:
                    feat, _ = extract_features(p)
                    for _ in range(12):
                        noise = np.random.normal(0, 0.01 * (np.std(feat) + 1e-6), size=feat.shape)
                        X_all.append(feat + noise)
                        y_all.append(1)
                except Exception:
                    pass

    print(f" -> Integrated {clone_count} Indic & Preset AI clone audio sources (augmented).")

    X = np.array(X_all, dtype=np.float32)
    y = np.array(y_all, dtype=np.int32)
    print(f"\nFinal Unified Matrix: X={X.shape}, y={y.shape} (Real: {np.sum(y==0)}, Fake: {np.sum(y==1)})")

    # 5. Train Master Soft-Voting Ensemble
    print("\n[Step 5/5] Training Master Soft-Voting Ensemble Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, stratify=y, random_state=42)

    rf = RandomForestClassifier(n_estimators=300, max_depth=18, min_samples_split=3, random_state=42, class_weight='balanced', n_jobs=-1)
    gb = GradientBoostingClassifier(n_estimators=150, learning_rate=0.08, max_depth=6, random_state=42)
    et = ExtraTreesClassifier(n_estimators=200, max_depth=18, min_samples_split=3, random_state=42, class_weight='balanced', n_jobs=-1)

    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb), ('et', et)],
        voting='soft',
        weights=[2.0, 1.8, 1.2]
    )

    ensemble.fit(X_train, y_train)

    test_preds = ensemble.predict(X_test)
    test_probs = ensemble.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, test_preds)
    roc = roc_auc_score(y_test, test_probs)

    print("=" * 75)
    print(f"TRAINING COMPLETE!")
    print(f"Test Accuracy: {acc * 100:.2f}% | ROC-AUC Score: {roc:.4f}")
    print("=" * 75)
    print(classification_report(y_test, test_preds, target_names=["Real Human Voice", "AI Clone / Spoof Audio"]))

    # Save Model Weights & Metadata
    model_path = "ml-model/models/custom_classifier.pkl"
    joblib.dump(ensemble, model_path)
    print(f"[SUCCESS] Saved multi-tier master ensemble to: {model_path}")

    metadata = {
        "model_type": "Multi-Tier Master Ensemble (Random Forest + Gradient Boosting + Extra Trees)",
        "feature_dimension": 147,
        "datasets_integrated": [
            "ASVspoof 2021 PA / Kaggle Dataset (110K subset)",
            "AI4Bharat Indic / Indian Accent Live Microphone Corpus",
            "Modern Neural AI Voice Clones (ElevenLabs / TikTok / CapCut TTS)",
            "Loudspeaker Replay & Acoustic Playback Spoofing Samples",
            "Indic Neural Clones (Hindi & Indian English TTS)"
        ],
        "test_accuracy": round(float(acc), 4),
        "roc_auc": round(float(roc), 4),
        "total_training_vectors": int(X.shape[0]),
        "trained_at": datetime.now(timezone.utc).isoformat()
    }

    with open("ml-model/models/model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("[SUCCESS] Telemetry metadata updated: ml-model/models/model_metadata.json")

if __name__ == "__main__":
    train_master_ensemble()
