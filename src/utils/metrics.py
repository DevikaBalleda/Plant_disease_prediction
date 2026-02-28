"""
metrics.py - Evaluation utilities for Plant Disease Detection
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")          # Non-interactive backend (safe for servers)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
import os
import json


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray,
                    class_names: list[str]) -> dict:
    """
    Compute classification metrics.

    Parameters
    ----------
    y_true      : 1-D array of true class indices
    y_pred      : 1-D array of predicted class indices
    class_names : ordered list of class name strings

    Returns
    -------
    dict with keys: accuracy, precision, recall, f1, report
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    report = classification_report(
        y_true, y_pred, target_names=class_names, zero_division=0
    )

    return {
        "accuracy":  round(float(acc),  4),
        "precision": round(float(prec), 4),
        "recall":    round(float(rec),  4),
        "f1":        round(float(f1),   4),
        "report":    report,
    }


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray,
                           class_names: list[str],
                           save_path: str | None = None) -> plt.Figure:
    """
    Plot and optionally save a confusion matrix heatmap.

    Parameters
    ----------
    y_true      : True labels
    y_pred      : Predicted labels
    class_names : Class name strings
    save_path   : If provided, saves the figure to this path

    Returns
    -------
    matplotlib Figure object
    """
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(max(10, len(class_names)), max(8, len(class_names) - 2)))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=ax,
        linewidths=0.5,
    )
    ax.set_xlabel("Predicted Label", fontsize=12)
    ax.set_ylabel("True Label", fontsize=12)
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"[INFO] Confusion matrix saved → {save_path}")

    return fig


def plot_training_history(history, save_dir: str | None = None) -> None:
    """
    Plot training & validation accuracy / loss curves.

    Parameters
    ----------
    history  : Keras History object returned by model.fit()
    save_dir : Directory to save the plots
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ── Accuracy ──
    axes[0].plot(history.history["accuracy"],     label="Train Acc",      color="#2196F3")
    axes[0].plot(history.history["val_accuracy"], label="Val Acc",        color="#FF9800", linestyle="--")
    axes[0].set_title("Model Accuracy", fontsize=13)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # ── Loss ──
    axes[1].plot(history.history["loss"],         label="Train Loss",     color="#F44336")
    axes[1].plot(history.history["val_loss"],     label="Val Loss",       color="#9C27B0", linestyle="--")
    axes[1].set_title("Model Loss", fontsize=13)
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.suptitle("Training History", fontsize=15, fontweight="bold")
    plt.tight_layout()

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, "training_history.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"[INFO] Training history saved → {path}")

    plt.close(fig)


def save_metrics_json(metrics: dict, save_path: str) -> None:
    """Save metrics dictionary as a JSON file."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump({k: v for k, v in metrics.items() if k != "report"}, f, indent=2)
    print(f"[INFO] Metrics JSON saved → {save_path}")
