import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder


def clean_text(text: str) -> str:
    return str(text).lower().replace(",", " ")


def main():
    random.seed(42)
    np.random.seed(42)

    data_path = Path(__file__).resolve().parents[1] / "data" / "synthetic_career_data.csv"
    df = pd.read_csv(data_path)

    required_cols = {"id", "skills", "education", "experience_years", "role"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["skills"] = df["skills"].fillna("")
    df["role"] = df["role"].fillna("")

    X_train, X_val, y_train, y_val = train_test_split(
        df["skills"], df["role"], test_size=0.2, stratify=df["role"], random_state=42
    )

    labeler = LabelEncoder()
    y_train_enc = labeler.fit_transform(y_train)
    y_val_enc = labeler.transform(y_val)

    pipeline = make_pipeline(
        CountVectorizer(
            preprocessor=clean_text,
            token_pattern=r"[a-zA-Z0-9_\+#\.]+",
            min_df=1,
        ),
        LogisticRegression(max_iter=400, multi_class="multinomial"),
    )
    pipeline.fit(X_train, y_train_enc)

    probs = pipeline.predict_proba(X_val)
    top5_idx = np.argsort(probs, axis=1)[:, -5:]
    hits = sum(1 for i, true_lab in enumerate(y_val_enc) if true_lab in top5_idx[i])
    top5_acc = hits / len(y_val_enc)
    top1_acc = float((pipeline.predict(X_val) == y_val_enc).mean())

    models_dir = Path(__file__).resolve().parents[1] / "models"
    models_dir.mkdir(exist_ok=True)
    artifacts = {
        "pipeline": pipeline,
        "label_encoder": labeler,
        "top1_acc": float(top1_acc),
        "top5_acc": float(top5_acc),
    }
    model_path = models_dir / "role_matcher.joblib"
    joblib.dump(artifacts, model_path)

    print(f"Saved model to {model_path}")
    print(f"Top-1 accuracy: {top1_acc:.3f}")
    print(f"Top-5 accuracy: {top5_acc:.3f}")

    demo_skills = ["python", "django", "postgresql", "docker", "aws"]
    probs_demo = pipeline.predict_proba([", ".join(demo_skills)])[0]
    top_idx = np.argsort(probs_demo)[-5:][::-1]
    roles = labeler.inverse_transform(top_idx)
    scores = probs_demo[top_idx]
    print("Demo prediction (role, score):")
    for role, score in zip(roles, scores):
        print(f"  {role}: {score:.3f}")


if __name__ == "__main__":
    main()
