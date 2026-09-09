import os
import sys

sys.path.insert(0, os.path.abspath('ml-model/src'))
from predict import get_hf_pipeline, get_asv_model
from features import extract_features

pipe = get_hf_pipeline()
asv = get_asv_model()

def test(path):
    try:
        import librosa
        feats, m = extract_features(path)
        y, _ = librosa.load(path, sr=16000)
        hf = pipe({"raw": y, "sampling_rate": 16000}) if pipe else None
        asv_p = asv.predict_proba(feats.reshape(1, -1))[0][1] if asv else 0
        print(f"{os.path.basename(path)}:")
        print(f"  HF Pipeline: {hf}")
        print(f"  ASV fake prob: {asv_p:.4f}")
        print(f"  Jitter: {m['pitch_micro_jitter']:.4f}, Rolloff: {m['spectral_rolloff_hz']:.1f}, Flatness: {m['spectral_flatness']:.5f}\n")
    except Exception as e:
        print(f"Error {path}: {e}")

print("=== KAGGLE FAKES (.flac) ===")
flacs = [os.path.join('backend/uploads', f) for f in os.listdir('backend/uploads') if f.endswith('.flac')][:4]
for f in flacs:
    test(f)

print("=== USER LIVE MIC RECORDINGS (.wav) ===")
wavs = [os.path.join('backend/uploads', f) for f in os.listdir('backend/uploads') if f.endswith('.wav') and os.path.getsize(os.path.join('backend/uploads', f)) > 200000][:4]
for f in wavs:
    test(f)

print("=== PRESET AUTHENTIC ===")
for s in ['authentic_bank_customer.wav', 'legitimate_ceo_voice.wav']:
    p = os.path.join('backend/sample_audio', s)
    if os.path.exists(p):
        test(p)

print("=== PRESET AI CLONES ===")
for s in ['ai_clone_emergency_scam.wav', 'deepfake_wire_transfer_request.wav']:
    p = os.path.join('backend/sample_audio', s)
    if os.path.exists(p):
        test(p)
