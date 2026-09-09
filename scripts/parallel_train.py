import os
import sys
import glob
import time
import numpy as np
import joblib
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml-model", "src")))
from features import extract_features  # type: ignore # pyrefly: ignore [missing-import]

EXTRACT_DIR = "ml-model/data/raw/asvspoof_extracted"
PROCESSED_DIR = "ml-model/data/processed"
MODELS_DIR = "ml-model/models"

def extract_single(item):
    path, label = item
    try:
        feat, _ = extract_features(path)
        return feat, label
    except Exception:
        return None, None

def run_parallel_training():
    start_time = time.time()
    real_paths = glob.glob(os.path.join(EXTRACT_DIR, "real", "*.flac"))
    fake_paths = glob.glob(os.path.join(EXTRACT_DIR, "fake", "*.flac"))
    tts_paths = glob.glob("ml-model/data/raw/tts_samples/*.mp3")

    print(f"Starting Multi-Core Parallel Feature Extraction across:")
    print(f"  - Real Human Voices: {len(real_paths)}")
    print(f"  - ASV Spoof / Replay Voices: {len(fake_paths)}")
    print(f"  - Commercial AI Text-to-Speech Voices: {len(tts_paths)}")

    tasks = [(p, 0) for p in real_paths] + [(p, 1) for p in fake_paths] + [(p, 1) for p in tts_paths]
    X, y = [], []

    workers = min(14, os.cpu_count() or 8)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(extract_single, t) for t in tasks]
        done_count = 0
        total = len(futures)
        for fut in as_completed(futures):
            feat, label = fut.result()
            if feat is not None:
                X.append(feat)
                y.append(label)
            done_count += 1
            if done_count % 300 == 0:
                print(f"  Processed {done_count}/{total} files ({int(done_count/total*100)}%)...")

    X = np.array(X)
    y = np.array(y)
    feat_time = time.time() - start_time
    print(f"Feature Extraction finished in {feat_time:.1f}s! Dataset: X={X.shape}, Real={np.sum(y==0)}, Fake={np.sum(y==1)}")

    # Split train/test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    np.save(os.path.join(PROCESSED_DIR, "X_train.npy"), X_train)
    np.save(os.path.join(PROCESSED_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(PROCESSED_DIR, "X_test.npy"), X_test)
    np.save(os.path.join(PROCESSED_DIR, "y_test.npy"), y_test)

    # Train Calibrated Classifier
    print("Training Calibrated Soft-Voting Classifier on ASVspoof data...")
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.metrics import accuracy_score, classification_report

    rf = RandomForestClassifier(n_estimators=200, max_depth=16, min_samples_split=4, random_state=42, class_weight="balanced", n_jobs=-1)
    gb = GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
    ensemble = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')

    clf = CalibratedClassifierCV(estimator=ensemble, method='sigmoid', cv=3)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print("=" * 60)
    print(f"TRAINING COMPLETE ON ASVSPOOF 2021 PA DATASET:")
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print("=" * 60)
    print(classification_report(y_test, preds, target_names=["Real Human Voice", "Spoof / Clone Audio"]))

    model_path = os.path.join(MODELS_DIR, "custom_classifier.pkl")
    joblib.dump(clf, model_path)
    print(f"Saved new trained model to: {model_path}")
    print(f"Total time taken: {time.time() - start_time:.1f}s")

if __name__ == "__main__":
    run_parallel_training()
