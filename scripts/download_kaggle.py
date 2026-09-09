import os
import subprocess
import sys

def download_dataset():
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml-model", "data", "raw"))
    os.makedirs(raw_dir, exist_ok=True)

    if not os.path.exists(kaggle_json_path):
        print("=" * 60)
        print("KAGGLE API TOKEN REQUIRED")
        print("=" * 60)
        print(f"File not found at: {kaggle_json_path}")
        print("\nSteps to download the official dataset:")
        print("1. Go to https://www.kaggle.com/settings -> Click 'Create New Token'")
        print("2. Save the downloaded 'kaggle.json' to:")
        print(f"   Windows: {kaggle_json_path}")
        print("3. Re-run this script: python scripts/download_kaggle.py")
        print("=" * 60)
        return False

    print(f"Downloading 'abdallamohamed312/ready-to-input-for-training' into {raw_dir}...")
    cmd = [
        sys.executable, "-m", "kaggle", "datasets", "download",
        "-d", "abdallamohamed312/ready-to-input-for-training",
        "-p", raw_dir,
        "--unzip"
    ]

    try:
        res = subprocess.run(cmd, check=True)
        print("\nDataset successfully downloaded and extracted!")
        print("Now re-run training: python ml-model/src/train.py")
        return True
    except Exception as e:
        print(f"Error downloading Kaggle dataset: {e}")
        return False

if __name__ == "__main__":
    download_dataset()
