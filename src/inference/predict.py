"""
predict.py
==========
Inference engine for Plant Disease Detection.

Features
--------
- Single-image prediction with confidence score
- Grad-CAM heatmap overlay visualization
- Severity classification (Mild / Moderate / Severe)
- Loads class labels from JSON (no dataset needed at runtime)

Usage
-----
    from src.inference.predict import Predictor
    predictor = Predictor()
    result = predictor.predict("path/to/leaf.jpg")
    print(result)
"""

from __future__ import annotations
import json
import os
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2

from src.utils.config import (
    BEST_MODEL_PATH, LABELS_PATH, CONFIDENCE_THRESHOLD,
    IMAGE_SIZE, GRADCAM_LAYER
)
from src.utils.disease_info import get_disease_info, get_severity
from src.data.preprocessing import Preprocessor


class Predictor:
    """
    Wraps the trained model for easy inference.

    Parameters
    ----------
    model_path  : str  – Path to saved model (.keras).
    labels_path : str  – Path to class_labels.json.
    """

    def __init__(
        self,
        model_path: str = BEST_MODEL_PATH,
        labels_path: str = LABELS_PATH,
    ) -> None:
        # Load trained model
        self.model = tf.keras.models.load_model(model_path)

        # Load class labels
        self.class_names = self._load_labels(labels_path)

        # Image preprocessor
        self.preprocessor = Preprocessor()

        print(f"[INFO] Predictor ready | {len(self.class_names)} classes")

    # ──────────────────────────────────────────────
    #  Public API
    # ──────────────────────────────────────────────

    def predict(self, image_path: str | None = None, pil_image=None) -> dict:
        """
        Run inference on a single image.

        Parameters
        ----------
        image_path : str or None  – Path to image file on disk.
        pil_image  : PIL.Image or None  – In-memory PIL image (from Flask upload).

        Returns
        -------
        dict with keys:
            label, confidence, severity, disease_info,
            top3, is_healthy, low_confidence
        """

        # Preprocess input
        if image_path:
            tensor = self.preprocessor.preprocess_single_image(image_path)
        elif pil_image is not None:
            tensor = self.preprocessor.preprocess_pil_image(pil_image)
        else:
            raise ValueError("Provide either image_path or pil_image.")

        # Model prediction
        probs = self.model.predict(tensor, verbose=0)[0]   # shape (num_classes,)

        top_idx = int(np.argmax(probs))
        confidence = float(probs[top_idx])

        # 🔥 FIX: JSON keys are STRINGS → convert index to string
        label = self.class_names[str(top_idx)]

        # Top-3 predictions
        top3_idx = np.argsort(probs)[::-1][:3]
        top3 = [
            {
                "label": self.class_names[str(i)],   # 🔥 FIX here too
                "confidence": round(float(probs[i]), 4)
            }
            for i in top3_idx
        ]

        disease_info = get_disease_info(label)
        severity = (
            get_severity(confidence)
            if "healthy" not in label.lower()
            else "N/A"
        )

        return {
            "label": label,
            "confidence": round(confidence, 4),
            "confidence_pct": round(confidence * 100, 2),
            "severity": severity,
            "disease_info": disease_info,
            "top3": top3,
            "is_healthy": "healthy" in label.lower(),
            "low_confidence": confidence < CONFIDENCE_THRESHOLD,
        }

    def predict_with_gradcam(
        self,
        image_path: str,
        save_path: str | None = None,
    ) -> tuple[dict, np.ndarray]:
        """
        Run prediction AND generate Grad-CAM heatmap overlay.

        Parameters
        ----------
        image_path : str           – Path to the input image.
        save_path  : str or None   – If set, saves the overlay image here.

        Returns
        -------
        (result_dict, heatmap_overlay_bgr_array)
        """

        result = self.predict(image_path=image_path)
        heatmap = self._compute_gradcam(image_path)
        overlay = self._overlay_heatmap(image_path, heatmap)

        if save_path:
            cv2.imwrite(save_path, overlay)
            print(f"[INFO] Grad-CAM overlay saved → {save_path}")

        return result, overlay

    # ──────────────────────────────────────────────
    #  Grad-CAM
    # ──────────────────────────────────────────────

    def _compute_gradcam(self, image_path: str) -> np.ndarray:
        """
        Compute Grad-CAM heatmap for the predicted class.

        Returns
        -------
        heatmap : np.ndarray of shape (H, W) with values in [0, 1]
        """

        try:
            last_conv = self.model.get_layer(GRADCAM_LAYER)
        except ValueError:
            # Fallback: find last Conv2D layer automatically
            for layer in reversed(self.model.layers):
                if isinstance(layer, tf.keras.layers.Conv2D):
                    last_conv = layer
                    break

        grad_model = tf.keras.Model(
            inputs=self.model.inputs,
            outputs=[last_conv.output, self.model.output],
        )

        img_tensor = self.preprocessor.preprocess_single_image(image_path)

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_tensor, training=False)
            top_class = tf.argmax(predictions[0])
            class_channel = predictions[:, top_class]

        grads = tape.gradient(class_channel, conv_outputs)
        pooled = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_out = conv_outputs[0]
        heatmap = tf.reduce_sum(tf.multiply(pooled, conv_out), axis=-1)

        heatmap = tf.maximum(heatmap, 0)
        heatmap /= (tf.math.reduce_max(heatmap) + 1e-8)

        return heatmap.numpy()

    def _overlay_heatmap(
        self,
        image_path: str,
        heatmap: np.ndarray,
        alpha: float = 0.4,
    ) -> np.ndarray:
        """
        Resize heatmap to original image size and blend as colourmap overlay.

        Returns
        -------
        BGR numpy array (suitable for cv2.imwrite / display)
        """

        img = cv2.imread(image_path)
        img = cv2.resize(img, IMAGE_SIZE)

        heatmap_resized = cv2.resize(heatmap, IMAGE_SIZE)
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        overlay = cv2.addWeighted(img, 1 - alpha, heatmap_color, alpha, 0)

        return overlay

    # ──────────────────────────────────────────────
    #  Helpers
    # ──────────────────────────────────────────────

    @staticmethod
    def _load_model(path: str) -> tf.keras.Model:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Trained model not found at: {path}\n"
                "Please run training first."
            )
        return tf.keras.models.load_model(path)

    @staticmethod
    def _load_labels(path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Class labels not found at: {path}\n"
                "They are created automatically during training."
            )
        with open(path) as f:
            return json.load(f)