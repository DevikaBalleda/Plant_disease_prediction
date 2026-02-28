"""
train.py
========
Training pipeline for Plant Disease Detection model.

Features
--------
- EarlyStopping with configurable patience
- ModelCheckpoint (saves best model by val_accuracy)
- TensorBoard logging
- Optional fine-tuning phase after initial training
- Saves class label JSON alongside the model

Run
---
    python -m src.models.train --data_dir data/raw/PlantVillage --epochs 30
"""

from __future__ import annotations
import argparse
import os
import datetime
import tensorflow as tf

from src.data.data_loader import DataLoader
from src.data.preprocessing import Preprocessor
from src.models.model import build_model
from src.utils.config import (
    BEST_MODEL_PATH, TENSORBOARD_DIR, SAVED_MODEL_DIR,
    EPOCHS, BATCH_SIZE, PATIENCE, MONITOR_METRIC,
    RAW_DATA_DIR
)
from src.utils.metrics import plot_training_history


def get_callbacks(log_dir: str) -> list:
    """Build a list of Keras training callbacks."""
    os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    callbacks = [
        # ── 1. Save best model by validation accuracy ──
        tf.keras.callbacks.ModelCheckpoint(
            filepath=BEST_MODEL_PATH,
            monitor=MONITOR_METRIC,
            save_best_only=True,
            verbose=1,
        ),
        # ── 2. Stop training when val_accuracy stops improving ──
        tf.keras.callbacks.EarlyStopping(
            monitor=MONITOR_METRIC,
            patience=PATIENCE,
            restore_best_weights=True,
            verbose=1,
        ),
        # ── 3. TensorBoard logging ──
        tf.keras.callbacks.TensorBoard(
            log_dir=log_dir,
            histogram_freq=1,
        ),
        # ── 4. Reduce LR on plateau ──
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1,
        ),
    ]
    return callbacks


def train(data_dir: str, epochs: int = EPOCHS, fine_tune: bool = False) -> None:
    """
    Full training pipeline.

    Parameters
    ----------
    data_dir  : Root directory with one sub-folder per class.
    epochs    : Maximum number of training epochs.
    fine_tune : Whether to perform a fine-tuning phase after initial training.
    """
    # ── Data Loading ──────────────────────────────────────────────
    loader = DataLoader(dataset_dir=data_dir, batch_size=BATCH_SIZE)
    train_ds, val_ds, test_ds = loader.get_datasets()
    class_names = loader.class_names
    num_classes = len(class_names)

    # ── Preprocessing ─────────────────────────────────────────────
    prep = Preprocessor()
    train_ds = prep.augment(train_ds)
    val_ds   = prep.normalize(val_ds)
    test_ds  = prep.normalize(test_ds)

    # ── Phase 1: Feature extraction (frozen base) ─────────────────
    print("\n" + "="*60)
    print(" PHASE 1: Feature Extraction (frozen base layers)")
    print("="*60)
    model = build_model(num_classes=num_classes, fine_tune=False)

    log_dir_p1 = os.path.join(
        TENSORBOARD_DIR,
        "phase1_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    )
    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=get_callbacks(log_dir_p1),
        verbose=1,
    )
    plot_training_history(history1, save_dir=SAVED_MODEL_DIR)
    print(f"\n[INFO] Phase 1 complete. Best model → {BEST_MODEL_PATH}")

    # ── Phase 2: Fine-tuning (optional) ───────────────────────────
    if fine_tune:
        print("\n" + "="*60)
        print(" PHASE 2: Fine-Tuning (unfreezing top layers)")
        print("="*60)
        model = build_model(num_classes=num_classes, fine_tune=True)
        # Load Phase 1 weights into fine-tune model
        model.load_weights(BEST_MODEL_PATH)

        log_dir_p2 = os.path.join(
            TENSORBOARD_DIR,
            "phase2_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        )
        fine_tune_path = os.path.join(SAVED_MODEL_DIR, "fine_tuned_model.h5")
        ft_callbacks = get_callbacks(log_dir_p2)
        # Override checkpoint path for fine-tuning
        ft_callbacks[0] = tf.keras.callbacks.ModelCheckpoint(
            filepath=fine_tune_path,
            monitor=MONITOR_METRIC,
            save_best_only=True,
            verbose=1,
        )

        history2 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=int(epochs * 0.4),  # Shorter fine-tune phase
            callbacks=ft_callbacks,
            verbose=1,
        )
        plot_training_history(history2, save_dir=SAVED_MODEL_DIR)
        print(f"[INFO] Fine-tuned model saved → {fine_tune_path}")

    print("\n[INFO] Training complete.")


# ─────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Plant Disease Detection Model")
    parser.add_argument(
        "--data_dir", type=str, default=RAW_DATA_DIR,
        help="Root dataset directory (default: data/raw)"
    )
    parser.add_argument(
        "--epochs", type=int, default=EPOCHS,
        help="Maximum training epochs"
    )
    parser.add_argument(
        "--fine_tune", action="store_true",
        help="Enable Phase 2 fine-tuning after feature extraction"
    )
    args = parser.parse_args()

    train(data_dir=args.data_dir, epochs=args.epochs, fine_tune=args.fine_tune)
