import os
import glob
import numpy as np
import pandas as pd
from features import extract_features
from sklearn.model_selection import train_test_split

AUDIO_EXTS = (".wav", ".flac", ".mp3", ".ogg", ".m4a")

def load_from_folders(base_dirs, real_names=("real", "bonafide"), fake_names=("fake", "spoof")):
    """
    Scans directory tree for audio files categorized into real/bonafide or fake/spoof folders.
    Extracts rich forensic acoustic features.
    """
    if isinstance(base_dirs, str):
        base_dirs = [base_dirs]

    X, y = [], []
    total_found = 0

    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue

        for root, dirs, files in os.walk(base_dir):
            root_lower = os.path.basename(root).lower()
            label_val = None
            if any(r in root_lower for r in real_names):
                label_val = 0
            elif any(f in root_lower for f in fake_names):
                label_val = 1

            if label_val is not None:
                for file in files:
                    if file.lower().endswith(AUDIO_EXTS):
                        path = os.path.join(root, file)
                        total_found += 1
                        try:
                            feat, _ = extract_features(path)
                            X.append(feat)
                            y.append(label_val)
                        except Exception as e:
                            print(f"[Warning] Skipped {path}: {e}")

    return np.array(X), np.array(y)

def load_from_protocol(audio_dir, protocol_path, filename_col=0, label_col=1, fake_label_value="spoof"):
    """
    Loads ASVspoof protocol text or CSV file mapping filename -> label string.
    """
    df = pd.read_csv(protocol_path, sep=None, engine="python", header=None)
    X, y = [], []
    for _, row in df.iterrows():
        fname = str(row[filename_col]).strip()
        label_str = str(row[label_col]).strip().lower()
        
        # Check audio extension
        candidate_paths = [
            os.path.join(audio_dir, fname),
            os.path.join(audio_dir, fname + ".flac"),
            os.path.join(audio_dir, fname + ".wav")
        ]
        chosen_path = next((p for p in candidate_paths if os.path.exists(p)), None)
        if not chosen_path:
            continue

        try:
            feat, _ = extract_features(chosen_path)
            X.append(feat)
            y.append(1 if label_str == fake_label_value.lower() else 0)
        except Exception as e:
            print(f"[Warning] Skipped {fname}: {e}")

    return np.array(X), np.array(y)

def main():
    raw_dir = "ml-model/data/raw"
    processed_dir = "ml-model/data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    # Search for available datasets in raw_dir
    possible_folders = [
        raw_dir,
        os.path.join(raw_dir, "combined_folder"),
        os.path.join(raw_dir, "training"),
        os.path.join(raw_dir, "benchmark"),
    ]

    print("Scanning audio directories for training samples...")
    X, y = load_from_folders(possible_folders)

    # If no audio files exist yet, automatically generate realistic benchmark samples
    if len(X) == 0:
        print("No raw audio files found. Generating benchmark audio dataset...")
        from generate_samples import generate_benchmark_dataset
        generate_benchmark_dataset(os.path.join(raw_dir, "benchmark"), count_per_class=50)
        X, y = load_from_folders(possible_folders)

    real_count = int(np.sum(y == 0))
    fake_count = int(np.sum(y == 1))
    print(f"Dataset successfully compiled: Total={len(X)} | Real={real_count} | Fake/Cloned={fake_count}")

    if len(X) < 10:
        raise ValueError("Insufficient dataset samples to train. Please provide audio files.")

    # Stratified split 80% train / 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    np.save(os.path.join(processed_dir, "X_train.npy"), X_train)
    np.save(os.path.join(processed_dir, "y_train.npy"), y_train)
    np.save(os.path.join(processed_dir, "X_test.npy"), X_test)
    np.save(os.path.join(processed_dir, "y_test.npy"), y_test)

    print(f"Saved processed datasets to {processed_dir}:")
    print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"  X_test:  {X_test.shape}, y_test:  {y_test.shape}")

if __name__ == "__main__":
    main()
