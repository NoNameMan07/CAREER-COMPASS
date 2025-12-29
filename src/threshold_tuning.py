"""
Per-label probability threshold tuning using validation data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score


def tune_thresholds(y_true: np.ndarray, y_proba: np.ndarray, grid=None) -> np.ndarray:
    grid = grid or np.arange(0.1, 0.91, 0.05)
    thresholds = np.zeros(y_true.shape[1])
    for i in range(y_true.shape[1]):
        best_f1 = -1.0
        best_thr = 0.5
        for thr in grid:
            preds = (y_proba[:, i] >= thr).astype(int)
            score = f1_score(y_true[:, i], preds, zero_division=0)
            if score > best_f1:
                best_f1 = score
                best_thr = thr
        thresholds[i] = best_thr
    return thresholds


def main() -> None:
    parser = argparse.ArgumentParser(description="Tune probability thresholds per role label.")
    parser.add_argument("--proba", type=Path, required=True, help="Path to val_proba.npy from training.")
    parser.add_argument("--labels", type=Path, required=True, help="Path to y_val.npy from training.")
    parser.add_argument("--out", type=Path, default=Path("artifacts/thresholds.npy"))
    parser.add_argument("--json_out", type=Path, default=Path("artifacts/thresholds.json"))
    parser.add_argument("--roles", type=Path, default=Path("artifacts/roles.json"))
    args = parser.parse_args()

    y_proba = np.load(args.proba)
    y_true = np.load(args.labels)

    thresholds = tune_thresholds(y_true, y_proba)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.out, thresholds)

    roles = json.loads(args.roles.read_text()) if args.roles.exists() else list(range(len(thresholds)))
    role_thresholds = dict(zip(roles, thresholds.tolist()))
    args.json_out.write_text(json.dumps(role_thresholds, indent=2))
    print(f"Saved thresholds to {args.out} and {args.json_out}")


if __name__ == "__main__":
    main()

