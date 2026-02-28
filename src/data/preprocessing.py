"""
preprocessing.py
================
Image preprocessing pipeline: normalization and data augmentation.

Uses mobilenet_v2.preprocess_input() which maps pixel values to [-1, 1].
This matches the FIXED Colab training notebook (colab_train_FIXED.ipynb)
which uses preprocessing_function=preprocess_input in ImageDataGenerator.

After retraining with colab_train_FIXED.ipynb, inference and training
preprocessing will be correctly aligned.

Usage
-----
    from src.data.preprocessing import Preprocessor
    preprocessor = Preprocessor()
    tensor = preprocessor.preprocess_pil_image(pil_img)
"""

from __future__ import annotations
import tensorflow as tf
from src.utils.config import AUGMENTATION, IMAGE_SIZE


def _rescale(image: tf.Tensor) -> tf.Tensor:
    """Scale pixel values from [0, 255] to [0, 1] — matches Colab training."""
    return tf.cast(image, tf.float32) / 255.0


class Preprocessor:
    """
    Encapsulates all image preprocessing steps:
      1. Simple /255 normalization → [0, 1]  (matches ImageDataGenerator(rescale=1/255))
      2. Random augmentation via tf.image transforms (training only)
    """

    def __init__(self) -> None:
        # Augmentation layers (applied only during training)
        self._augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(AUGMENTATION["rotation_range"] / 360),
            tf.keras.layers.RandomZoom(AUGMENTATION["zoom_range"]),
            tf.keras.layers.RandomTranslation(
                height_factor=AUGMENTATION["height_shift_range"],
                width_factor=AUGMENTATION["width_shift_range"],
            ),
            tf.keras.layers.RandomBrightness(factor=0.2),
            tf.keras.layers.RandomContrast(factor=0.2),
        ], name="augmentation")

    # ──────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────

    def normalize(self, dataset: tf.data.Dataset) -> tf.data.Dataset:
        """
        Apply only /255 normalization (no augmentation).
        Use for validation and test sets.
        """
        return dataset.map(
            lambda img, lbl: (_rescale(img), lbl),
            num_parallel_calls=tf.data.AUTOTUNE,
        )

    def augment(self, dataset: tf.data.Dataset) -> tf.data.Dataset:
        """
        Apply augmentation + /255 normalization.
        Use for the training set only.
        """
        return dataset.map(
            lambda img, lbl: (
                _rescale(self._augmentation(tf.cast(img, tf.float32), training=True)),
                lbl,
            ),
            num_parallel_calls=tf.data.AUTOTUNE,
        )

    def preprocess_single_image(self, image_path: str) -> tf.Tensor:
        """
        Load, resize, and preprocess a single image from disk.
        Used at inference time.

        Returns tf.Tensor of shape (1, H, W, 3) in [-1, 1] range
        (matches mobilenet_v2.preprocess_input used in training).
        """
        raw   = tf.io.read_file(image_path)
        image = tf.image.decode_image(raw, channels=3, expand_animations=False)
        image = tf.image.resize(image, IMAGE_SIZE)
        image = tf.cast(image, tf.float32)
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        return tf.expand_dims(image, axis=0)   # (1, H, W, 3)

    def preprocess_pil_image(self, pil_image) -> tf.Tensor:
        """
        Accept a PIL Image and return a preprocessed tensor.
        Used in Flask app where the upload is an in-memory PIL image.

        Returns tf.Tensor of shape (1, H, W, 3) in [-1, 1] range
        (matches mobilenet_v2.preprocess_input used in training).
        """
        import numpy as np
        from PIL import Image as PILImage

        pil_image = pil_image.convert("RGB").resize(IMAGE_SIZE, PILImage.LANCZOS)
        arr = np.array(pil_image, dtype=np.float32)
        arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
        return tf.expand_dims(arr, axis=0)

