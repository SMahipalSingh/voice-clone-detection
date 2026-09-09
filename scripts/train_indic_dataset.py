import os
import sys
import numpy as np
import soundfile as sf
import joblib
import json
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score

sys.path.insert(0, os.path.abspath('ml-model/src'))
from features import extract_features

def build_indic_training_pipeline(num_samples_per_class=100):
    """
    Automated training pipeline for Indic / Multi-accent voice clone detection.
    Integrates genuine Indic human speech with synthetic Indic neural TTS clones.
    """
    print("=" * 60)
    print("AI4Bharat & Indic Voice Clone Detection Training Pipeline")
    print("=" * 60)

    os.makedirs("ml-model/data/processed", exist_ok=True)
    os.makedirs("ml-model/models", exist_ok=True)
    indic_raw_dir = "ml-model/data/raw/indic_samples"
    os.makedirs(indic_raw_dir, exist_ok=True)

    # 1. Gather Real Indian Voice Samples (from live uploads + datasets)
    print("\n[Step 1/4] Collecting Real Indian Voice Samples...")
    real_paths = []
    
    # Collect existing user live microphone recordings
    upload_dir = "backend/uploads"
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            if f.endswith(".wav") and os.path.getsize(os.path.join(upload_dir, f)) > 100000:
                real_paths.append(os.path.join(upload_dir, f))

    # Add preset authentic samples
    sample_dir = "backend/sample_audio"
    if os.path.exists(sample_dir):
        for s in ["authentic_bank_customer.wav", "legitimate_ceo_voice.wav"]:
            p = os.path.join(sample_dir, s)
            if os.path.exists(p):
                real_paths.append(p)

    print(f" -> Found {len(real_paths)} genuine speaker samples.")

    # 2. Generate Corresponding Synthetic Indic TTS / Clones
    print("\n[Step 2/4] Synthesizing Indic AI Clones (gTTS / Vocoder Simulation)...")
    fake_paths = []
    from gtts import gTTS

    indic_prompts = [
        ("hindi_urgent_transfer", "नमस्ते, यह बैंक से अत्यंत महत्वपूर्ण सत्यापन कॉल है।", "hi"),
        ("hindi_security_alert", "कृपया अपने खाते की सुरक्षा के लिए पासवर्ड तुरंत अपडेट करें।", "hi"),
        ("indian_en_ceo_fraud", "Hello, this is urgent wire transfer authorization for the vendor account.", "en"),
        ("indian_en_finance_call", "Please expedite payment for the Bangalore corporate office immediately.", "en"),
        ("hindi_police_scam", "यह पुलिस मुख्यालय से कॉल है, तुरंत अपने विवरण सत्यापित करें।", "hi"),
        ("hindi_emergency_loan", "आपकी पूर्व-स्वीकृत व्यक्तिगत ऋण राशि तुरंत जारी की जा रही है।", "hi"),
        ("indian_en_otp_request", "Your banking security token will expire in two minutes. Please confirm.", "en"),
        ("hindi_kyc_update", "आपके बैंक खाते का ईकेवाईसी अधूरा है, इसे अभी पूरा करें।", "hi")
    ]

    for name, text, lang in indic_prompts:
        out_path = os.path.join(indic_raw_dir, f"indic_ai_clone_{name}.mp3")
        if not os.path.exists(out_path):
            try:
                tld = 'co.in' if lang == 'en' else 'com'
                tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
                tts.save(out_path)
            except Exception as e:
                print(f"TTS generation error for {name}: {e}")
        if os.path.exists(out_path):
            fake_paths.append(out_path)

    # Add preset clone samples
    if os.path.exists(sample_dir):
        for s in ["ai_clone_emergency_scam.wav", "deepfake_wire_transfer_request.wav", "test_tts_sample.wav"]:
            p = os.path.join(sample_dir, s)
            if os.path.exists(p):
                fake_paths.append(p)

    print(f" -> Prepared {len(fake_paths)} synthetic AI clone samples.")

    # 3. Feature Extraction
    print("\n[Step 3/4] Extracting 147 Multi-Spectral Acoustic Features...")
    X_list = []
    y_list = []

    for path in real_paths:
        try:
            feats, _ = extract_features(path)
            X_list.append(feats)
            y_list.append(0) # 0 = Real Human
        except Exception as e:
            print(f"Error extracting {path}: {e}")

    for path in fake_paths:
        try:
            feats, _ = extract_features(path)
            X_list.append(feats)
            y_list.append(1) # 1 = AI Clone
        except Exception as e:
            print(f"Error extracting {path}: {e}")

    # Data augmentation for robust generalization
    augmented_X = []
    augmented_y = []
    for x, y_val in zip(X_list, y_list):
        augmented_X.append(x)
        augmented_y.append(y_val)
        # Add slight acoustic noise variation for generalization
        for _ in range(3):
            noise = np.random.normal(0, 0.015 * np.std(x), size=x.shape)
            augmented_X.append(x + noise)
            augmented_y.append(y_val)

    X = np.array(augmented_X)
    y = np.array(augmented_y)
    print(f" -> Total Training Vectors: {X.shape[0]} (Dimensions: {X.shape[1]})")

    # 4. Train Calibrated Ensemble Classifier
    print("\n[Step 4/4] Training Ensemble Classifier (Random Forest + Gradient Boosting)...")
    rf = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42, class_weight='balanced')
    gb = GradientBoostingClassifier(n_estimators=80, learning_rate=0.08, max_depth=4, random_state=42)

    ensemble = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')
    ensemble.fit(X, y)

    # 5-fold cross validation score
    cv_scores = cross_val_score(ensemble, X, y, cv=min(5, len(y)//2), scoring='accuracy')
    mean_acc = float(np.mean(cv_scores))
    print(f" -> Cross-Validation Accuracy: {mean_acc*100:.2f}%")

    # Save Model & Metadata
    model_save_path = "ml-model/models/custom_classifier.pkl"
    joblib.dump(ensemble, model_save_path)

    metadata = {
        "model_type": "Soft-Voting Ensemble (Random Forest + Gradient Boosting)",
        "feature_dimension": 147,
        "indic_domain_adapted": True,
        "languages_supported": ["Indian English", "Hindi", "Indic Multi-Accent", "Global English"],
        "cross_val_accuracy": round(mean_acc, 4),
        "total_training_samples": int(X.shape[0]),
        "trained_at": datetime.utcnow().isoformat()
    }

    with open("ml-model/models/model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n[SUCCESS] Model weights saved to: {model_save_path}")
    print(f"[SUCCESS] Telemetry metadata updated: ml-model/models/model_metadata.json")
    print("=" * 60)

if __name__ == "__main__":
    build_indic_training_pipeline()
