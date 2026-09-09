import os
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix

def train_model():
    processed_dir = "ml-model/data/processed"
    models_dir = "ml-model/models"
    os.makedirs(models_dir, exist_ok=True)

    X_train_path = os.path.join(processed_dir, "X_train.npy")
    y_train_path = os.path.join(processed_dir, "y_train.npy")
    X_test_path = os.path.join(processed_dir, "X_test.npy")
    y_test_path = os.path.join(processed_dir, "y_test.npy")

    if not os.path.exists(X_train_path):
        print("Processed dataset not found. Running build_dataset.py first...")
        import build_dataset
        build_dataset.main()

    X_train = np.load(X_train_path)
    y_train = np.load(y_train_path)
    X_test = np.load(X_test_path)
    y_test = np.load(y_test_path)

    print(f"Training Classifier on {len(X_train)} samples with {X_train.shape[1]} forensic features...")

    # Ensemble: Random Forest + Gradient Boosting for robust generalization against both replay and vocoder artifacts
    rf = RandomForestClassifier(
        n_estimators=250,
        max_depth=16,
        min_samples_split=3,
        random_state=42,
        class_weight="balanced"
    )
    
    gb = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=5,
        random_state=42
    )

    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb)],
        voting='soft'
    )

    # Calibrated probability output
    clf = CalibratedClassifierCV(estimator=ensemble, method='sigmoid', cv=3)
    clf.fit(X_train, y_train)

    # Evaluate on test set
    preds = clf.predict(X_test)
    probas = clf.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, preds))
    prec = float(precision_score(y_test, preds, zero_division=0))
    rec = float(recall_score(y_test, preds, zero_division=0))
    f1 = float(f1_score(y_test, preds, zero_division=0))
    auc = float(roc_auc_score(y_test, probas)) if len(np.unique(y_test)) > 1 else 1.0
    cm = confusion_matrix(y_test, preds).tolist()

    print("=" * 50)
    print("MODEL PERFORMANCE EVALUATION:")
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall:    {rec * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")
    print(f"ROC-AUC:   {auc * 100:.2f}%")
    print("=" * 50)
    print("Classification Report:")
    print(classification_report(y_test, preds, target_names=["Real / Safe", "Fake / Clone"]))

    # Export model artifact
    model_path = os.path.join(models_dir, "custom_classifier.pkl")
    joblib.dump(clf, model_path)
    print(f"Saved trained classifier to: {model_path}")

    # Export performance metadata
    metadata = {
        "model_type": "Calibrated Soft-Voting Ensemble (RandomForest + GradientBoosting)",
        "features_dim": int(X_train.shape[1]),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": cm
    }
    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    return clf, metadata

if __name__ == "__main__":
    train_model()
