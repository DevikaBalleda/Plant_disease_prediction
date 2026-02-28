"""
config.py - Central configuration for Plant Disease Detection System
All hyperparameters, paths, and constants are defined here.
"""

import os

# ─────────────────────────────────────────────
# Project Root
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─────────────────────────────────────────────
# Data Paths
# ─────────────────────────────────────────────
DATA_DIR        = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR    = os.path.join(DATA_DIR, "raw", "plantvillage dataset", "color")
PROCESSED_DIR   = os.path.join(DATA_DIR, "processed")

# ─────────────────────────────────────────────
# Model Paths
# ─────────────────────────────────────────────
MODELS_DIR      = os.path.join(BASE_DIR, "models")
SAVED_MODEL_DIR = os.path.join(MODELS_DIR, "saved_model")
BEST_MODEL_PATH = os.path.join(SAVED_MODEL_DIR, "best_model.keras")
LABELS_PATH     = os.path.join(SAVED_MODEL_DIR, "class_names.json")

# ─────────────────────────────────────────────
# Image Settings
# ─────────────────────────────────────────────
IMAGE_SIZE      = (224, 224)     # MobileNetV2 / EfficientNet input size
IMAGE_CHANNELS  = 3
INPUT_SHAPE     = (*IMAGE_SIZE, IMAGE_CHANNELS)

# ─────────────────────────────────────────────
# Training Hyperparameters
# ─────────────────────────────────────────────
BATCH_SIZE      = 32
EPOCHS          = 50
LEARNING_RATE   = 1e-4
FINE_TUNE_LR    = 1e-5
VALIDATION_SPLIT = 0.2
TEST_SPLIT      = 0.1
RANDOM_SEED     = 42

# Fine-tuning: number of base-model layers to unfreeze
FINE_TUNE_AT    = 100           # Unfreeze layers from this index onwards

# ─────────────────────────────────────────────
# Early Stopping / Checkpoint
# ─────────────────────────────────────────────
PATIENCE        = 7             # Early stopping patience
MIN_DELTA       = 0.001         # Min improvement to reset patience counter
MONITOR_METRIC  = "val_accuracy"

# ─────────────────────────────────────────────
# Data Augmentation Settings
# ─────────────────────────────────────────────
AUGMENTATION = {
    "rotation_range":       30,
    "width_shift_range":    0.2,
    "height_shift_range":   0.2,
    "shear_range":          0.2,
    "zoom_range":           0.2,
    "horizontal_flip":      True,
    "vertical_flip":        False,
    "fill_mode":            "nearest",
    "brightness_range":     [0.8, 1.2],
}

# ─────────────────────────────────────────────
# TensorBoard
# ─────────────────────────────────────────────
LOGS_DIR        = os.path.join(BASE_DIR, "logs")
TENSORBOARD_DIR = os.path.join(LOGS_DIR, "tensorboard")

# ─────────────────────────────────────────────
# Flask App
# ─────────────────────────────────────────────
UPLOAD_FOLDER   = os.path.join(BASE_DIR, "app", "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Confidence threshold below which result is flagged as "uncertain"
CONFIDENCE_THRESHOLD = 0.60

# ─────────────────────────────────────────────
# Grad-CAM Settings
# ─────────────────────────────────────────────
GRADCAM_LAYER   = "out_relu"    # Last conv activation in MobileNetV2

# ─────────────────────────────────────────────
# Severity Thresholds (confidence-based heuristic)
# ─────────────────────────────────────────────
SEVERITY = {
    "mild":     (0.60, 0.75),
    "moderate": (0.75, 0.90),
    "severe":   (0.90, 1.00),
}
