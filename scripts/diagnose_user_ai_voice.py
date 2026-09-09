import os
import sys

sys.path.insert(0, os.path.abspath('ml-model/src'))
from predict import predict, get_hf_pipeline, get_asv_model
from features import extract_features

pipe = get_hf_pipeline()
asv = get_asv_model()

test_files = [
    'backend/uploads/e45a533d-9ec4-4c8b-bcbd-5bdd38a3e39c.wav',
    'backend/uploads/17deab4c-10ca-4c70-a5d6-1bb0b1f26901.wav',
    'backend/uploads/7de8d740-d4cd-43d9-9808-43c720f8f253.wav',
    'backend/uploads/c77dbf8e-1364-4626-ae18-b6982c258c56.wav',
    'backend/uploads/2ad22164-5289-4085-8292-b9e4a6cefdb9.mp3',
    r'C:\Users\smsas\.gemini\antigravity-ide\brain\6c2c3191-ef68-424f-97a4-cf4a69e408e7\.user_uploaded\uploaded_media_1788990468961.img'
]

for p in test_files:
    if os.path.exists(p):
        try:
            res = predict(p)
            print(f"=== {os.path.basename(p)} ===")
            print(f"  Final Risk: {res['confidence']*100:.1f}%, Label: {res['label']}")
            print(f"  Neural Prob: {res['neural_deepfake_confidence']}, ASV Prob: {res['asvspoof_confidence']}, Acoustic: {res['acoustic_frequency_score']}")
            print(f"  Summary: {res['forensic_summary']}")
            print(f"  Metrics: {res['metrics']}\n")
        except Exception as e:
            print(f"Error {p}: {e}")
