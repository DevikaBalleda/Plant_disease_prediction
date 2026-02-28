"""
evaluate.py
===========
Evaluate a trained plant disease model on the test set.

Usage
-----
    python -m src.models.evaluate --data_dir data/raw/PlantVillage
"""

from __future__ import annotations
import argparse
import numpy as np
import os
import tensorflow as tf

from src.data.data_loader import DataLoader
from src.data.preprocessing import Preprocessor
from src.models.model import load_model
from src.utils.config import BEST_MODEL_PATH, RAW_DATA_DIR, SAVED_MODEL_DIR, BATCH_SIZE
from src.utils.metrics import (
    compute_metrics,
    plot_confusion_matrix,
    save_metrics_json,
)


def evaluate(model_path: str, data_dir: str) -> dict:
    """
    Run full evaluation: metrics + confusion matrix.

    Parameters
    ----------
    model_path : str  – Path to saved .h5 model file.
    data_dir   : str  – Dataset root directory.

    Returns
    -------
    dict of evaluation metrics.
    """
    # ── Load model ──────────────────────────────────────────────
    model = load_model(model_path)

    # ── Load data ───────────────────────────────────────────────
    loader = DataLoader(dataset_dir=data_dir, batch_size=BATCH_SIZE)
    _, _, test_ds = loader.get_datasets()
    class_names   = loader.class_names

    # ── Preprocess ──────────────────────────────────────────────
    prep    = Preprocessor()
    test_ds = prep.normalize(test_ds)

    # ── Predictions ─────────────────────────────────────────────
    print("[INFO] Running predictions on test set …")
    y_true, y_pred = [], []

    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # ── Metrics ─────────────────────────────────────────────────
    metrics = compute_metrics(y_true, y_pred, class_names)

    print("\n" + "="*60)
    print(" EVALUATION RESULTS")
    print("="*60)
    print(f"  Accuracy  : {metrics['accuracy']:.4f}")
    print(f"  Precision : {metrics['precision']:.4f}")
    print(f"  Recall    : {metrics['recall']:.4f}")
    print(f"  F1 Score  : {metrics['f1']:.4f}")
    print("\nClassification Report:\n")
    print(metrics["report"])

    # ── Save outputs ────────────────────────────────────────────
    cm_path = os.path.join(SAVED_MODEL_DIR, "confusion_matrix.png")
    plot_confusion_matrix(y_true, y_pred, class_names, save_path=cm_path)

    json_path = os.path.join(SAVED_MODEL_DIR, "eval_metrics.json")
    save_metrics_json(metrics, save_path=json_path)

    return metrics


# ─────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Plant Disease Model")
    parser.add_argument(
        "--model_path", type=str, default=BEST_MODEL_PATH,
        help="Path to saved Keras model (.h5)"
    )
    parser.add_argument(
        "--data_dir", type=str, default=RAW_DATA_DIR,
        help="Root dataset directory"
    )
    args = parser.parse_args()

    evaluate(model_path=args.model_path, data_dir=args.data_dir)
