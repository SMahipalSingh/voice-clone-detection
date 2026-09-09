import os
import sys
import zipfile
import glob
import numpy as np
import joblib
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml-model", "src")))
from features import extract_features

ZIP_PATH = "ml-model/data/raw/ready-to-input-for-training.zip"
EXTRACT_DIR = "ml-model/data/raw/asvspoof_extracted"
PROCESSED_DIR = "ml-model/data/processed"
MODELS_DIR = "ml-model/models"

def extract_balanced_subset(sample_limit_per_class=1000):
    """
    Extracts a balanced subset of real and fake FLAC audio samples
    from the 110,468-file ASVspoof Kaggle zip archive.
    """
    os.makedirs(os.path.join(EXTRACT_DIR, "real"), exist_ok=True)
    os.makedirs(os.path.join(EXTRACT_DIR, "fake"), exist_ok=True)

    print(f"Opening ASVspoof zip archive: {ZIP_PATH}...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        all_files = z.namelist()
        real_files = [f for f in all_files if "/real/" in f.lower() and f.endswith(".flac")]
        fake_files = [f for f in all_files if "/fake/" in f.lower() and f.endswith(".flac")]

        print(f"Total in archive: Real = {len(real_files)}, Fake = {len(fake_files)}")
        
        selected_real = real_files[:sample_limit_per_class]
        selected_fake = fake_files[:sample_limit_per_class]

        print(f"Extracting balanced subset ({len(selected_real)} Real, {len(selected_fake)} Fake)...")
        for f in selected_real:
            target_path = os.path.join(EXTRACT_DIR, "real", os.path.basename(f))
            if not os.path.exists(target_path):
                with z.open(f) as src, open(target_path, "wb") as dst:
                    dst.write(src.read())

        for f in selected_fake:
            target_path = os.path.join(EXTRACT_DIR, "fake", os.path.basename(f))
            if not os.path.exists(target_path):
                with z.open(f) as src, open(target_path, "wb") as dst:
                    dst.write(src.read())

    print("Extraction complete!")

def process_file(args):
    path, label = args
    try:
        feat, _ = extract_features(path)
        return feat, label
    except Exception as e:
        return None, None

def build_features_and_train():
    extract_balanced_subset(sample_limit_per_class=1000)

    real_paths = glob.glob(os.path.join(EXTRACT_DIR, "real", "*.flac"))
    fake_paths = glob.glob(os.path.join(EXTRACT_DIR, "fake", "*.flac"))

    print(f"Extracting 147 forensic acoustic features from {len(real_paths) + len(fake_paths)} real ASVspoof samples...")

    tasks = [(p, 0) for p in real_paths] + [(p, 1) for p in fake_paths]
    X, y = [], []

    count = 0
    total = len(tasks)
    for path, label in tasks:
        try:
            feat, _ = extract_features(path)
            X.append(feat)
            y.append(label)
            count += 1
            if count % 200 == 0:
                print(f"  Processed {count}/{total} audio files...")
        except Exception as e:
            continue

    X = np.array(X)
    y = np.array(y)
    print(f"Compiled feature matrix: X={X.shape}, y={y.shape} (Real: {np.sum(y==0)}, Fake: {np.sum(y==1)})")

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

    rf = RandomForestClassifier(n_estimators=200, max_depth=16, min_samples_split=4, random_state=42, class_weight="balanced")
    gb = GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
    ensemble = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')

    clf = CalibratedClassifierCV(estimator=ensemble, method='sigmoid', cv=3)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print("=" * 60)
    print(f"NEW MODEL TRAINED ON ASVSPOOF 2021 PA:")
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print("=" * 60)
    print(classification_report(y_test, preds, target_names=["Real Human Voice", "Spoof / Clone Audio"]))

    model_path = os.path.join(MODELS_DIR, "custom_classifier.pkl")
    joblib.dump(clf, model_path)
    print(f"Saved re-trained model to: {model_path}")

if __name__ == "__main__":
    build_features_and_train()
