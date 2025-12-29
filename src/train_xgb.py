"""
Training pipeline for the Sensei Phase 1 Career Compass model.

Loads a dataset generated via `data/data_gen.py`, performs feature encoding,
trains an XGBoost One-vs-Rest classifier, and saves all artifacts required for
inference (model, encoders, label binarizer, validation probabilities).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from xgboost import XGBClassifier

from src.feature_pipeline import FeatureEncoder
import ast


def load_dataset(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file extension: {path.suffix}")


def precision_at_k(y_true: np.ndarray, scores: np.ndarray, k: int) -> float:
    top_k_idx = np.argsort(scores, axis=1)[:, -k:]
    hits = 0
    for row, idxs in enumerate(top_k_idx):
        hits += y_true[row, idxs].sum()
    return hits / (len(y_true) * k)


def recall_at_k(y_true: np.ndarray, scores: np.ndarray, k: int) -> float:
    top_k_idx = np.argsort(scores, axis=1)[:, -k:]
    hits = 0
    total = y_true.sum()
    total = total if total > 0 else 1
    for row, idxs in enumerate(top_k_idx):
        hits += y_true[row, idxs].sum()
    return hits / total


def main() -> None:
    parser = argparse.ArgumentParser(description="Train XGBoost One-vs-Rest model for Sensei.")
    parser.add_argument("--data", type=Path, required=True, help="Path to dataset (parquet/csv).")
    parser.add_argument("--artifacts_dir", type=Path, default=Path("artifacts"), help="Output directory.")
    parser.add_argument("--test_size", type=float, default=0.2)
    args = parser.parse_args()

    df = load_dataset(args.data)

    def ensure_list(value):
        if isinstance(value, list):
            return value
        if hasattr(value, "tolist"):
            return value.tolist()
        if isinstance(value, str) and value:
            try:
                return json.loads(value)
            except Exception:
                try:
                    return ast.literal_eval(value)
                except Exception:
                    return [v.strip() for v in value.split(",") if v.strip()]
        return []

    # Adapt minimal CSV schema: id, skills, education, experience, role
    if "labels" not in df.columns and "role" in df.columns:
        df["labels"] = df["role"].apply(lambda r: [str(r).strip()] if pd.notna(r) else [])
    if "desired_roles" not in df.columns:
        df["desired_roles"] = [[] for _ in range(len(df))]

    if "skills" in df.columns:
        df["skills"] = df["skills"].apply(ensure_list)
    else:
        df["skills"] = [[] for _ in range(len(df))]

    # Normalize education values to categories used in encoder
    if "education" in df.columns:
        mapping = {
            "Bachelors": "UG",
            "Masters": "PG",
            "PhD": "PhD",
            "Bootcamp": "Bootcamp",
        }
        df["education"] = df["education"].map(lambda x: mapping.get(str(x), "UG"))
    else:
        df["education"] = "UG"

    # Map experience to years_experience
    if "years_experience" not in df.columns:
        if "experience" in df.columns:
            df["years_experience"] = pd.to_numeric(df["experience"], errors="coerce").fillna(0).astype(int)
        else:
            df["years_experience"] = 0

    encoder = FeatureEncoder.create()
    # Ensure required columns exist with defaults
    for col in encoder.numeric_cols:
        if col not in df.columns:
            df[col] = 0
    for col in encoder.categorical_cols:
        if col not in df.columns:
            if col == "field_of_study":
                df[col] = "CS"
            elif col == "personality":
                df[col] = "ambivert"
            elif col == "work_preference":
                df[col] = "team"
            elif col == "sentiment":
                df[col] = "neutral"
            else:
                df[col] = "UG"
    encoder.fit(df)
    X = encoder.transform(df)

    label_binarizer = MultiLabelBinarizer()
    Y = label_binarizer.fit_transform(df["labels"])

    X_train, X_val, y_train, y_val = train_test_split(
        X, Y, test_size=args.test_size, random_state=42
    )

    model = OneVsRestClassifier(
        XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            n_jobs=-1,
            objective="binary:logistic",
            eval_metric="logloss",
        )
    )

    model.fit(X_train, y_train)
    y_val_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)

    metrics = {
        "hamming_loss": float(hamming_loss(y_val, y_val_pred)),
        "precision@3": float(precision_at_k(y_val, y_proba, k=3)),
        "recall@3": float(recall_at_k(y_val, y_proba, k=3)),
    }
    report = classification_report(y_val, y_val_pred, target_names=label_binarizer.classes_)
    print(json.dumps(metrics, indent=2))
    print(report)

    artifacts_dir = args.artifacts_dir
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, artifacts_dir / "xgb_onevsrest.joblib")
    joblib.dump(encoder, artifacts_dir / "feature_encoder.joblib")
    joblib.dump(label_binarizer, artifacts_dir / "label_binarizer.joblib")
    np.save(artifacts_dir / "val_proba.npy", y_proba)
    np.save(artifacts_dir / "y_val.npy", y_val)
    (artifacts_dir / "roles.json").write_text(json.dumps(label_binarizer.classes_.tolist(), indent=2))
    (artifacts_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(f"Artifacts saved under {artifacts_dir}")


if __name__ == "__main__":
    main()

