"""
model.py
========
MobileNetV2-based Transfer Learning model for Plant Disease Detection.

Architecture
------------
  Base  : MobileNetV2 pretrained on ImageNet (frozen initially)
  Head  : GlobalAveragePooling → BatchNorm → Dense(512) → Dropout → Dense(N)

Usage
-----
    from src.models.model import build_model
    model = build_model(num_classes=38)
    model.summary()
"""

from __future__ import annotations
import tensorflow as tf
from src.utils.config import INPUT_SHAPE, LEARNING_RATE, FINE_TUNE_LR, FINE_TUNE_AT


def build_model(num_classes: int, fine_tune: bool = False) -> tf.keras.Model:
    """
    Build and compile a MobileNetV2–based classification model.

    Parameters
    ----------
    num_classes : int
        Number of output disease classes.
    fine_tune   : bool
        If True, unfreezes top layers of the base model for fine-tuning.

    Returns
    -------
    Compiled tf.keras.Model
    """
    # ── 1. Base model ────────────────────────────────────────────
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=INPUT_SHAPE,
        include_top=False,        # Remove original classifier
        weights="imagenet",       # Use pretrained ImageNet weights
    )
    base_model.trainable = False  # Freeze all layers initially

    # ── 2. Fine-tune option ────────────────────────────────────
    if fine_tune:
        base_model.trainable = True
        # Freeze everything below FINE_TUNE_AT to avoid catastrophic forgetting
        for layer in base_model.layers[:FINE_TUNE_AT]:
            layer.trainable = False
        lr = FINE_TUNE_LR
        print(f"[INFO] Fine-tuning enabled: unfreezing layers from index {FINE_TUNE_AT}")
    else:
        lr = LEARNING_RATE

    # ── 3. Custom classification head ────────────────────────
    inputs  = tf.keras.Input(shape=INPUT_SHAPE, name="input_layer")
    x       = base_model(inputs, training=False)   # BN layers run in inference mode
    x       = tf.keras.layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x       = tf.keras.layers.BatchNormalization(name="bn_head")(x)
    x       = tf.keras.layers.Dense(512, activation="relu", name="dense_512")(x)
    x       = tf.keras.layers.Dropout(0.4, name="dropout")(x)
    outputs = tf.keras.layers.Dense(
        num_classes, activation="softmax", name="predictions"
    )(x)

    model = tf.keras.Model(inputs, outputs, name="PlantDiseaseClassifier")

    # ── 4. Compile ────────────────────────────────────────────
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    print(f"[INFO] Model built → {model.name}")
    print(f"[INFO] Trainable params: {model.count_params():,}")
    return model


def load_model(model_path: str) -> tf.keras.Model:
    """
    Load a previously saved Keras model from disk.

    Parameters
    ----------
    model_path : str
        Path to .h5 or SavedModel directory.

    Returns
    -------
    tf.keras.Model
    """
    if not tf.io.gfile.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = tf.keras.models.load_model(model_path)
    print(f"[INFO] Model loaded from: {model_path}")
    return model
