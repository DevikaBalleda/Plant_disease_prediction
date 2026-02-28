"""
data_loader.py
==============
Handles loading and splitting the PlantVillage dataset from disk.

Usage
-----
    from src.data.data_loader import DataLoader

    loader = DataLoader(dataset_dir="data/raw/PlantVillage")
    train_ds, val_ds, test_ds = loader.get_datasets()
    class_names = loader.class_names
"""

from __future__ import annotations
import os
import json
import tensorflow as tf
from src.utils.config import (
    IMAGE_SIZE, BATCH_SIZE, VALIDATION_SPLIT, TEST_SPLIT,
    RANDOM_SEED, LABELS_PATH
)


class DataLoader:
    """
    Loads PlantVillage (or any ImageFolder-style) dataset using
    tf.keras.utils.image_dataset_from_directory.

    Parameters
    ----------
    dataset_dir : str
        Root directory where each subfolder represents a class.
    image_size  : tuple
        Target (height, width) for resizing.
    batch_size  : int
        Number of samples per batch.
    """

    def __init__(
        self,
        dataset_dir: str,
        image_size: tuple = IMAGE_SIZE,
        batch_size: int = BATCH_SIZE,
    ) -> None:
        if not os.path.isdir(dataset_dir):
            raise FileNotFoundError(
                f"Dataset directory not found: {dataset_dir}\n"
                "Download PlantVillage from https://www.kaggle.com/datasets/"
                "emmarex/plantdisease and extract to data/raw/PlantVillage"
            )

        self.dataset_dir = dataset_dir
        self.image_size  = image_size
        self.batch_size  = batch_size
        self.class_names: list[str] = []

    # ──────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────

    def get_datasets(self) -> tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
        """
        Returns
        -------
        (train_ds, val_ds, test_ds) — batched, prefetched tf.data.Dataset objects
        """
        # Load full dataset first (no batching yet) to split manually
        full_ds = tf.keras.utils.image_dataset_from_directory(
            self.dataset_dir,
            image_size=self.image_size,
            batch_size=None,             # Load sample-by-sample for splitting
            shuffle=True,
            seed=RANDOM_SEED,
            label_mode="int",
        )

        self.class_names = full_ds.class_names
        self._save_class_labels()

        total = tf.data.experimental.cardinality(full_ds).numpy()
        test_count = int(total * TEST_SPLIT)
        val_count  = int(total * VALIDATION_SPLIT)
        train_count = total - test_count - val_count

        train_ds = full_ds.take(train_count)
        remaining = full_ds.skip(train_count)
        val_ds   = remaining.take(val_count)
        test_ds  = remaining.skip(val_count)

        # Batch and prefetch for performance
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.batch(self.batch_size).prefetch(AUTOTUNE)
        val_ds   = val_ds.batch(self.batch_size).prefetch(AUTOTUNE)
        test_ds  = test_ds.batch(self.batch_size).prefetch(AUTOTUNE)

        print(
            f"[INFO] Dataset split → "
            f"Train: {train_count} | Val: {val_count} | Test: {test_count} samples"
        )
        print(f"[INFO] Number of classes: {len(self.class_names)}")

        return train_ds, val_ds, test_ds

    # ──────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────

    def _save_class_labels(self) -> None:
        """Save class label list as JSON for use at inference time."""
        os.makedirs(os.path.dirname(LABELS_PATH), exist_ok=True)
        with open(LABELS_PATH, "w") as f:
            json.dump(self.class_names, f, indent=2)
        print(f"[INFO] Class labels saved → {LABELS_PATH}")

    def get_class_names(self) -> list[str]:
        return self.class_names
