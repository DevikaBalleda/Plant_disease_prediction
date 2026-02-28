"""
src/train.py  —  CPU-Safe Training (Plant Disease Detection)
=============================================================
Config
------
  Dataset     : data/raw/plantvillage   (one sub-folder per class)
  Image size  : 160 x 160  (smaller = faster on CPU, lower RAM)
  Batch size  : 16          (low RAM footprint)
  Val split   : 20 %
  Base model  : MobileNetV2 (ImageNet, frozen)
  Head        : GAP → Dense(128, relu) → Dropout(0.3) → Dense(n, softmax)
  Epochs      : 3
  Output      : models/plant_model.keras

Run
---
    cd plant_disease_prediction
    python src/train.py
"""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"          # suppress verbose TF logs
os.environ["TF_ENABLE_ONEDNN_OPTS"]  = "0"        # disable oneDNN messages

import tensorflow as tf

# ── CPU optimisation: use all available logical cores ─────────────────────────
NUM_THREADS = os.cpu_count() or 4
tf.config.threading.set_intra_op_parallelism_threads(NUM_THREADS)
tf.config.threading.set_inter_op_parallelism_threads(NUM_THREADS)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, Input

# ──────────────────────────────────────────────────────────────────────────────
# PATHS  (relative to this file → always correct regardless of cwd)
# ──────────────────────────────────────────────────────────────────────────────
_HERE        = os.path.dirname(os.path.abspath(__file__))
_PROJECT     = os.path.dirname(_HERE)               # plant_disease_prediction/

DATASET_DIR  = os.path.join(_PROJECT, "data", "raw", "plantvillage dataset", "color")
MODEL_SAVE   = os.path.join(_PROJECT, "models", "plant_model.keras")

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG (CPU-safe)
# ──────────────────────────────────────────────────────────────────────────────
TARGET_SIZE      = (160, 160)   # smaller than 224 → faster, less RAM
BATCH_SIZE       = 16           # low memory footprint
EPOCHS           = 3            # quick training run
VALIDATION_SPLIT = 0.2

# ──────────────────────────────────────────────────────────────────────────────
# GUARD: dataset must exist
# ──────────────────────────────────────────────────────────────────────────────
if not os.path.isdir(DATASET_DIR):
    raise FileNotFoundError(
        f"\n[ERROR] Dataset not found: {DATASET_DIR}\n"
        "Place your PlantVillage dataset there (one sub-folder per class)."
    )

# ──────────────────────────────────────────────────────────────────────────────
# DATA GENERATORS
# ──────────────────────────────────────────────────────────────────────────────
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=VALIDATION_SPLIT,
)

train_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=TARGET_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True,
    seed=42,
)

val_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=TARGET_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
    seed=42,
)

# Auto-detect classes from dataset folder structure
class_names = list(train_gen.class_indices.keys())
num_classes  = len(class_names)

print("\n" + "=" * 60)
print("  DATASET SUMMARY")
print("=" * 60)
print(f"  Number of classes        : {num_classes}")
print(f"  Training images          : {train_gen.samples}")
print(f"  Validation images        : {val_gen.samples}")
print("=" * 60 + "\n")

# ──────────────────────────────────────────────────────────────────────────────
# MODEL  (MobileNetV2 + custom head)
# ──────────────────────────────────────────────────────────────────────────────
# 1. Frozen base
base = MobileNetV2(
    input_shape=(*TARGET_SIZE, 3),
    include_top=False,
    weights="imagenet",
)
base.trainable = False   # freeze all base weights

# 2. Classification head
inputs  = Input(shape=(*TARGET_SIZE, 3))
x       = base(inputs, training=False)     # keep BN in inference mode
x       = layers.GlobalAveragePooling2D()(x)
x       = layers.Dense(128, activation="relu")(x)
x       = layers.Dropout(0.3)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(inputs, outputs, name="plant_disease_cpu")

# 3. Compile
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

# ──────────────────────────────────────────────────────────────────────────────
# TRAIN
# ──────────────────────────────────────────────────────────────────────────────
print("\n[INFO] Training on CPU — 3 epochs, batch=16, image=160x160 …\n")

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    verbose=1,
)

# ──────────────────────────────────────────────────────────────────────────────
# SAVE
# ──────────────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(MODEL_SAVE), exist_ok=True)
model.save(MODEL_SAVE)
print(f"\n[INFO] Model saved → {MODEL_SAVE}")

# ──────────────────────────────────────────────────────────────────────────────
# FINAL REPORT
# ──────────────────────────────────────────────────────────────────────────────
final_train_acc = history.history["accuracy"][-1]
final_val_acc   = history.history["val_accuracy"][-1]

print("\n" + "=" * 60)
print("  TRAINING COMPLETE")
print("=" * 60)
print(f"  Number of classes        : {num_classes}")
print(f"  Training images          : {train_gen.samples}")
print(f"  Validation images        : {val_gen.samples}")
print(f"  Final training accuracy  : {final_train_acc:.4f}  ({final_train_acc*100:.2f}%)")
print(f"  Final validation accuracy: {final_val_acc:.4f}  ({final_val_acc*100:.2f}%)")
print(f"  Model saved to           : {MODEL_SAVE}")
print("=" * 60 + "\n")
