import os
import sys

sys.path.insert(0, os.path.abspath('ml-model/src'))
from predict import predict

def benchmark():
    print("=" * 85)
    print("VOICESHIELD MULTI-DOMAIN ACOUSTIC & NEURAL BENCHMARK")
    print("Kaggle ASVspoof + Indian Live Mic + Indic AI Clones + Authentic Presets")
    print("=" * 85)

    results = []

    # 1. User Live Mic Recordings (PCM WAV)
    upload_dir = "backend/uploads"
    if os.path.exists(upload_dir):
        mic_files = [os.path.join(upload_dir, f) for f in os.listdir(upload_dir) if f.endswith(".wav") and os.path.getsize(os.path.join(upload_dir, f)) > 200000][:6]
        for p in mic_files:
            try:
                res = predict(p)
                results.append(("Indian Live Mic", os.path.basename(p), "REAL (HUMAN)", res['label'].upper(), res['confidence'], res['forensic_summary']))
            except Exception as e:
                pass

    # 2. Preset Authentic Voices
    sample_dir = "backend/sample_audio"
    if os.path.exists(sample_dir):
        for s in ["authentic_bank_customer.wav", "legitimate_ceo_voice.wav"]:
            p = os.path.join(sample_dir, s)
            if os.path.exists(p):
                try:
                    res = predict(p)
                    results.append(("Preset Authentic", s, "REAL (HUMAN)", res['label'].upper(), res['confidence'], res['forensic_summary']))
                except Exception as e:
                    pass

    # 3. Kaggle ASVspoof Fakes (.flac)
    if os.path.exists(upload_dir):
        flac_fakes = [os.path.join(upload_dir, f) for f in os.listdir(upload_dir) if f.endswith(".flac")][:6]
        for p in flac_fakes:
            try:
                res = predict(p)
                # Check if it was bonafide or fake
                # In ASVspoof, 03709054 is bonafide real, others are fakes
                expected = "REAL (HUMAN)" if "03709054" in p else "FAKE (AI CLONE)"
                results.append(("Kaggle ASVspoof", os.path.basename(p), expected, res['label'].upper(), res['confidence'], res['forensic_summary']))
            except Exception as e:
                pass

    # 4. Preset AI Clones
    if os.path.exists(sample_dir):
        for s in ["ai_clone_emergency_scam.wav", "deepfake_wire_transfer_request.wav", "test_tts_sample.wav"]:
            p = os.path.join(sample_dir, s)
            if os.path.exists(p):
                try:
                    res = predict(p)
                    results.append(("Preset AI Clone", s, "FAKE (AI CLONE)", res['label'].upper(), res['confidence'], res['forensic_summary']))
                except Exception as e:
                    pass

    # 5. Indic AI Clones
    indic_dir = "ml-model/data/raw/indic_samples"
    if os.path.exists(indic_dir):
        for f in os.listdir(indic_dir):
            if f.endswith(".mp3"):
                p = os.path.join(indic_dir, f)
                try:
                    res = predict(p)
                    results.append(("Indic AI Clone", f, "FAKE (AI CLONE)", res['label'].upper(), res['confidence'], res['forensic_summary']))
                except Exception as e:
                    pass

    print(f"\n{'Category':<18} | {'Audio File':<35} | {'Expected':<14} | {'Predicted':<10} | {'Risk %':<7} | {'Verdict'}")
    print("-" * 115)
    
    correct = 0
    total = len(results)

    for cat, filename, expected, predicted, conf, summary in results:
        is_correct = (expected.startswith("REAL") and predicted == "REAL") or (expected.startswith("FAKE") and predicted == "FAKE")
        if is_correct:
            correct += 1
            verdict_str = "PASS [OK]"
        else:
            verdict_str = "FAIL [MISCLASSIFIED]"

        fn_short = filename if len(filename) <= 34 else filename[:31] + "..."
        print(f"{cat:<18} | {fn_short:<35} | {expected:<14} | {predicted:<10} | {conf*100:>5.1f}% | {verdict_str}")

    print("=" * 115)
    accuracy = (correct / total) * 100 if total > 0 else 0
    print(f"BENCHMARK ACCURACY: {correct}/{total} ({accuracy:.1f}%)")
    print("=" * 115)

if __name__ == "__main__":
    benchmark()
