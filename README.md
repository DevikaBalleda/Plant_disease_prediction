# 🌿 Plant Disease Detection & Treatment Recommendation System

> **AI-powered deep learning application** for identifying plant diseases from leaf images and providing actionable treatment recommendations — built with TensorFlow, MobileNetV2, and Flask.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange?logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey?logo=flask)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Dataset Setup](#dataset-setup)
- [Training the Model](#training-the-model)
- [Running the Web App](#running-the-web-app)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Disease Coverage](#disease-coverage)
- [Example Output](#example-output)
- [Technologies](#technologies)

---

## 🔍 Overview

This system classifies plant diseases from leaf photographs using a **MobileNetV2** transfer learning model trained on the **PlantVillage** dataset (~54,000 images, 38 classes). It then provides:

- Predicted disease name (English + Hindi)
- Confidence score & severity level
- Chemical and organic treatment recommendations
- Preventive measures
- **Grad-CAM** heatmap showing the model's focus region
- Downloadable PDF diagnosis report

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Transfer Learning | MobileNetV2 pretrained on ImageNet |
| 🔥 Grad-CAM | Visual explanation of model predictions |
| 💊 Treatment DB | 20+ diseases with chemical & organic remedies |
| 🌡️ Severity | Mild / Moderate / Severe classification |
| 🇮🇳 Bilingual | English + Hindi UI toggle |
| 📄 PDF Report | Downloadable diagnosis report (reportlab) |
| 🐳 Docker Ready | One-command containerized deployment |
| 📊 Metrics | Accuracy, Precision, Recall, F1, Confusion Matrix |

---

## 📁 Project Structure

```
plant_disease_prediction/
│
├── data/
│   ├── raw/                    ← Place PlantVillage dataset here
│   └── processed/              ← Auto-generated preprocessed files
│
├── notebooks/
│   └── EDA.ipynb               ← Exploratory Data Analysis
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── data_loader.py      ← tf.data pipeline with train/val/test split
│   │   └── preprocessing.py    ← Augmentation + MobileNetV2 normalization
│   ├── models/
│   │   ├── model.py            ← MobileNetV2 + custom head architecture
│   │   ├── train.py            ← Training pipeline (2-phase + callbacks)
│   │   └── evaluate.py         ← Evaluation metrics & confusion matrix
│   ├── utils/
│   │   ├── config.py           ← All hyperparameters & paths
│   │   ├── metrics.py          ← Plotting & metric utilities
│   │   └── disease_info.py     ← Disease treatment database (20+ diseases)
│   └── inference/
│       └── predict.py          ← Predictor class with Grad-CAM
│
├── app/
│   ├── app.py                  ← Flask web application
│   ├── templates/
│   │   └── index.html          ← Bilingual farmer-friendly UI
│   └── static/
│       ├── css/style.css       ← Premium dark-theme styling
│       └── uploads/            ← Runtime image uploads (gitignored)
│
├── models/
│   └── saved_model/            ← Saved .h5 model + class_labels.json
│
├── requirements.txt
├── README.md
├── Dockerfile
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Clone & Enter Project

```bash
git clone https://github.com/your-username/plant-disease-detection.git
cd plant-disease-detection/plant_disease_prediction
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗂️ Dataset Setup

Download the **PlantVillage Dataset** from Kaggle:

```bash
# Option A – Kaggle CLI
pip install kaggle
kaggle datasets download -d emmarex/plantdisease -p data/raw/ --unzip

# Option B – Manual
# 1. Visit: https://www.kaggle.com/datasets/emmarex/plantdisease
# 2. Download and extract to: data/raw/PlantVillage/
```

Expected structure after extraction:
```
data/raw/PlantVillage/
├── Apple___Apple_scab/
├── Apple___Black_rot/
├── Tomato___Early_blight/
└── ... (38 class folders)
```

---

## 🏋️ Training the Model

### Phase 1 – Feature Extraction (recommended first run)

```bash
python -m src.models.train --data_dir data/raw/PlantVillage --epochs 30
```

### Phase 1 + Phase 2 – Feature Extraction + Fine-Tuning

```bash
python -m src.models.train --data_dir data/raw/PlantVillage --epochs 50 --fine_tune
```

### Monitor with TensorBoard

```bash
tensorboard --logdir logs/tensorboard
# → Open http://localhost:6006
```

### Evaluate the Trained Model

```bash
python -m src.models.evaluate --data_dir data/raw/PlantVillage
```

**Expected Results** (PlantVillage, MobileNetV2):

| Metric | Score |
|---|---|
| Accuracy | ~97% |
| Precision | ~97% |
| Recall | ~97% |
| F1 Score | ~97% |

---

## 🌐 Running the Web App

```bash
# From the project root directory
python app/app.py

# → Navigate to: http://localhost:5000
```

> ⚠️ **Note:** Train the model first. The app will show a "Model Not Trained" banner if `models/saved_model/best_model.h5` is missing.

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t plant-disease-app .
```

### Run Container

```bash
docker run -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  plant-disease-app
```

### Docker Compose (optional)

```yaml
# docker-compose.yml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./models:/app/models
```

```bash
docker-compose up
```

---

## ☁️ Cloud Deployment

### Render (Free Tier)

1. Push repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Set **Build Command:** `pip install -r requirements.txt`
4. Set **Start Command:** `python app/app.py`
5. Add env var: `FLASK_ENV=production`

### Hugging Face Spaces

1. Create a Space → select **Docker** runtime
2. Push your repo (include `Dockerfile`)
3. Upload your trained model under `models/saved_model/`

### AWS EC2

```bash
# On EC2 instance
git clone <your-repo>
cd plant_disease_prediction
pip install -r requirements.txt
# Upload model file via scp
python app/app.py
# For production: use gunicorn + nginx
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 "app.app:create_app()"
```

---

## 🌱 Disease Coverage (20+ in Database)

| Crop | Diseases Covered |
|---|---|
| 🍅 Tomato | Early Blight, Late Blight, Bacterial Spot, Leaf Miner, Healthy |
| 🥔 Potato | Early Blight, Late Blight, Healthy |
| 🌽 Corn | Common Rust, Northern Leaf Blight, Healthy |
| 🍇 Grape | Black Rot, Leaf Blight, Healthy |
| 🍎 Apple | Apple Scab, Black Rot, Healthy |
| 🌶️ Pepper | Bacterial Spot, Healthy |
| 🍓 Strawberry | Leaf Scorch, Healthy |

---

## 📊 Example Output

```
Input  : tomato_leaf.jpg
Result :
  Disease   : Tomato Early Blight
  Hindi     : टमाटर की प्रारंभिक झुलसन
  Confidence: 94.3%
  Severity  : Severe

  Chemical Treatment:
    - Chlorothalonil (Bravo 720) – 2.5 g/L every 7–10 days
    - Mancozeb 75 WP – 2.5 g/L at disease onset

  Organic Treatment:
    - Neem oil (3%) spray every 7–10 days
    - Copper fungicide (Bordeaux mixture 1%)

  Prevention:
    - Practice 2–3 year crop rotation
    - Remove and destroy infected plant debris
```

---

## 🛠️ Technologies

| Category | Technology |
|---|---|
| Deep Learning | TensorFlow 2.13, Keras |
| Model | MobileNetV2 (ImageNet pretrained) |
| Explainability | Grad-CAM |
| Image Processing | OpenCV, Pillow |
| Web Framework | Flask 2.3 |
| Data Science | NumPy, Scikit-learn, Matplotlib, Seaborn |
| PDF Generation | ReportLab |
| Containerization | Docker |
| Dataset | PlantVillage (38 classes, ~54K images) |

---

## ⚠️ Project Limitations

While this Plant Disease Detection & Treatment Recommendation System demonstrates the practical application of deep learning in agriculture, it has the following limitations:

1. **Limited Dataset Diversity**
   - The model is trained on a specific dataset and may not generalize well to unseen environmental conditions.
   - Variations in lighting, background noise, and camera quality can affect prediction accuracy.

2. **Class Imbalance**
   - Some disease classes have fewer training samples, which may reduce prediction performance for those categories.

3. **Not Suitable for Real-Time Field Deployment**
   - The current implementation is designed for demonstration and research purposes.
   - It has not been optimized for edge devices or low-resource agricultural environments.

4. **Confidence Threshold Sensitivity**
   - Predictions with low confidence may not always be reliable.
   - The model may misclassify visually similar diseases.

5. **Limited Crop Coverage**
   - The system supports only the plant species included in the training dataset.
   - It does not generalize to all crops or regional plant varieties.

6. **No Clinical/Expert Validation**
   - The treatment recommendations are dataset-based and not validated by agricultural experts.
   - This system should not replace professional agronomic consultation.

7. **Deployment Constraints**
   - The application may require significant memory due to TensorFlow dependencies.
   - Free-tier hosting platforms may struggle with large ML models.

---

## 🔮 Future Improvements

- Expand dataset with real-world field images.
- Implement advanced architectures (EfficientNet / Vision Transformers).
- Add real-time camera integration.
- Deploy optimized lightweight models using TensorFlow Lite.
- Integrate expert-validated treatment recommendations.
- Improve multi-language support and accessibility.
