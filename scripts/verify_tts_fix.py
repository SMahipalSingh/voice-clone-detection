import sys
import os
sys.path.insert(0, os.path.abspath("ml-model/src"))
from predict import predict

print("=" * 70)
print("VERIFYING FORENSIC DETECTION FIX ACROSS TTS, REAL HUMAN & SPOOF VOICES")
print("=" * 70)

# 1. Commercial TTS Sample
print("\n[1] Testing Commercial AI Text-to-Speech (Google TTS / Neural Vocoder):")
res_tts = predict("ml-model/data/raw/tts_samples/tts_000.mp3")
print(f"  Confidence (Risk): {res_tts['confidence']*100:.1f}%")
print(f"  Classification:    {res_tts['label'].upper()} ({'CLONED/SYNTHETIC' if res_tts['is_cloned'] else 'SAFE'})")
print(f"  ASV+TTS ML Score:  {res_tts['asvspoof_confidence']*100:.1f}%")
print(f"  Neural Wav2Vec2:   {res_tts['neural_deepfake_confidence']*100:.1f}%")
print(f"  Acoustic Telemetry:{res_tts['acoustic_frequency_score']*100:.1f}%")
print(f"  Forensic Summary:  {res_tts['forensic_summary']}")

# 2. Real Human Microphone / Vocal Sample
print("\n[2] Testing Authentic Human Voice (ASVspoof Real Speaker):")
res_real = predict("ml-model/data/raw/asvspoof_extracted/real/PA_E_2541070.flac")
print(f"  Confidence (Risk): {res_real['confidence']*100:.1f}%")
print(f"  Classification:    {res_real['label'].upper()} ({'CLONED/SYNTHETIC' if res_real['is_cloned'] else 'SAFE'})")
print(f"  ASV+TTS ML Score:  {res_real['asvspoof_confidence']*100:.1f}%")
print(f"  Neural Wav2Vec2:   {res_real['neural_deepfake_confidence']*100:.1f}%")
print(f"  Acoustic Telemetry:{res_real['acoustic_frequency_score']*100:.1f}%")
print(f"  Forensic Summary:  {res_real['forensic_summary']}")

# 3. Spoofed Replay Audio Sample
print("\n[3] Testing Acoustic Physical Spoof (ASVspoof 2021 Attack):")
res_spoof = predict("ml-model/data/raw/asvspoof_extracted/fake/PA_E_2541068.flac")
print(f"  Confidence (Risk): {res_spoof['confidence']*100:.1f}%")
print(f"  Classification:    {res_spoof['label'].upper()} ({'CLONED/SYNTHETIC' if res_spoof['is_cloned'] else 'SAFE'})")
print(f"  ASV+TTS ML Score:  {res_spoof['asvspoof_confidence']*100:.1f}%")
print(f"  Neural Wav2Vec2:   {res_spoof['neural_deepfake_confidence']*100:.1f}%")
print(f"  Acoustic Telemetry:{res_spoof['acoustic_frequency_score']*100:.1f}%")
print(f"  Forensic Summary:  {res_spoof['forensic_summary']}")

print("\n" + "=" * 70)
