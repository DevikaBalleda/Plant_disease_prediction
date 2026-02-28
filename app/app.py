"""
app.py
======
Flask web application for Plant Disease Detection & Treatment Recommendation.

Features
--------
- Image upload & live preview
- MobileNetV2 prediction with confidence score
- Grad-CAM visualization
- Treatment & medicine recommendations
- Severity indicator (Mild / Moderate / Severe)
- Downloadable PDF report
- Bilingual UI (English + Hindi toggle via JS)

Run
---
    cd plant_disease_prediction
    python app/app.py
    # → http://localhost:5000
"""

from __future__ import annotations
import os
import sys
import uuid
import base64
import io
import json
from datetime import datetime

from flask import (
    Flask, request, render_template, jsonify,
    send_file, redirect, url_for
)
from PIL import Image

# ── Make `src` importable when running from project root ──────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import (
    UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH,
    BEST_MODEL_PATH, LABELS_PATH
)


# ─────────────────────────────────────────────────────────────────
# Flask application factory
# ─────────────────────────────────────────────────────────────────

def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # ── Lazy-load predictor (avoids TF import at module level) ────
    predictor = None

    def get_predictor():
        nonlocal predictor
        if predictor is None:
            from src.inference.predict import Predictor
            predictor = Predictor(
                model_path=BEST_MODEL_PATH,
                labels_path=LABELS_PATH,
            )
        return predictor

    # ──────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────

    def allowed_file(filename: str) -> bool:
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def encode_image_base64(path: str) -> str:
        """Return base64 data URI for embedding an image in HTML."""
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = path.rsplit(".", 1)[1].lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        return f"data:image/{mime};base64,{data}"

    # ──────────────────────────────────────────────────────────────
    # Routes
    # ──────────────────────────────────────────────────────────────

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/predict", methods=["POST"])
    def predict():
        """
        Accept an image upload, run inference, return JSON result.
        """
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400

        # Save upload with unique name
        ext       = file.filename.rsplit(".", 1)[1].lower()
        uid       = uuid.uuid4().hex[:8]
        filename  = f"{uid}.{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        try:
            pred = get_predictor()

            # Run prediction
            pil_img = Image.open(save_path)
            result  = pred.predict(pil_image=pil_img)

            # Grad-CAM (only for disease, not healthy)
            gradcam_b64 = None
            if not result["is_healthy"]:
                cam_path = os.path.join(
                    UPLOAD_FOLDER, f"cam_{uid}.jpg"
                )
                try:
                    import cv2
                    _, cam_overlay = pred.predict_with_gradcam(
                        image_path=save_path, save_path=cam_path
                    )
                    gradcam_b64 = encode_image_base64(cam_path)
                except Exception as e:
                    print(f"[WARN] Grad-CAM failed: {e}")

            # Original image as base64
            orig_b64 = encode_image_base64(save_path)

            # Build response
            disease  = result["disease_info"]
            response = {
                "success":        True,
                "label":          result["label"],
                "display_name":   disease.get("name", result["label"]),
                "hindi_name":     disease.get("hindi_name", ""),
                "confidence_pct": result["confidence_pct"],
                "severity":       result["severity"],
                "is_healthy":     result["is_healthy"],
                "low_confidence": result["low_confidence"],
                "top3":           result["top3"],
                "disease_info":   {
                    "description":        disease.get("description", ""),
                    "cause":              disease.get("cause", ""),
                    "symptoms":           disease.get("symptoms", []),
                    "chemical_treatment": disease.get("chemical_treatment", []),
                    "organic_treatment":  disease.get("organic_treatment", []),
                    "prevention":         disease.get("prevention", []),
                },
                "original_image": orig_b64,
                "gradcam_image":  gradcam_b64,
                "timestamp":      datetime.now().strftime("%d %b %Y, %H:%M:%S"),
                "uid":            uid,
            }
            return jsonify(response)

        except FileNotFoundError as e:
            # Model not trained yet
            return jsonify({
                "error": "model_not_found",
                "message": str(e)
            }), 503
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

    @app.route("/report/<uid>")
    def download_report(uid: str):
        """
        Generate a PDF diagnosis report and send it to the browser.
        Requires reportlab: pip install reportlab
        """
        # Load cached JSON from temp file if available, else return 404
        report_json = os.path.join(UPLOAD_FOLDER, f"report_{uid}.json")
        if not os.path.exists(report_json):
            return "Report not found. Please re-submit your image.", 404

        with open(report_json) as f:
            data = json.load(f)

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import (
                SimpleDocTemplate, Paragraph, Spacer,
                Table, TableStyle, HRFlowable
            )
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                                    rightMargin=40, leftMargin=40,
                                    topMargin=50, bottomMargin=40)
            styles = getSampleStyleSheet()
            green  = colors.HexColor("#2E7D32")
            story  = []

            # Title
            story.append(Paragraph(
                "🌿 Plant Disease Diagnosis Report", styles["Title"]
            ))
            story.append(Paragraph(
                f"Generated: {data.get('timestamp', '')}", styles["Normal"]
            ))
            story.append(HRFlowable(width="100%", thickness=1, color=green))
            story.append(Spacer(1, 12))

            di = data.get("disease_info", {})

            # Summary table
            summary = [
                ["Disease",    data.get("display_name", "")],
                ["Hindi Name", data.get("hindi_name", "")],
                ["Confidence", f"{data.get('confidence_pct', 0):.1f}%"],
                ["Severity",   data.get("severity", "N/A")],
                ["Cause",      di.get("cause", "")],
            ]
            t = Table(summary, colWidths=[130, 360])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F5E9")),
                ("FONTNAME",   (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE",   (0, 0), (-1, -1), 10),
                ("GRID",       (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING",    (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 16))

            def section(title, items):
                story.append(Paragraph(title, styles["Heading2"]))
                for item in items:
                    story.append(Paragraph(f"• {item}", styles["Normal"]))
                story.append(Spacer(1, 10))

            section("Symptoms",             di.get("symptoms", []))
            section("Chemical Treatment",   di.get("chemical_treatment", []))
            section("Organic Treatment",    di.get("organic_treatment", []))
            section("Preventive Measures",  di.get("prevention", []))

            doc.build(story)
            buf.seek(0)
            return send_file(
                buf,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"plant_diagnosis_{uid}.pdf",
            )

        except ImportError:
            return "PDF generation requires reportlab. Run: pip install reportlab", 500

    @app.route("/save_report", methods=["POST"])
    def save_report():
        """Save prediction JSON for PDF generation."""
        data = request.get_json()
        uid  = data.get("uid", uuid.uuid4().hex[:8])
        path = os.path.join(UPLOAD_FOLDER, f"report_{uid}.json")
        with open(path, "w") as f:
            json.dump(data, f)
        return jsonify({"status": "saved"})

    @app.errorhandler(413)
    def too_large(_):
        return jsonify({"error": "File too large (max 16 MB)"}), 413

    return app


# ─────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import socket
    import sys
    import io

    # Force UTF-8 output so emoji in banners don't crash on Windows cp1252
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    app = create_app()

    port = int(os.environ.get("PORT", 8000))
    debug = False

    # Determine public URL
    render_url   = os.environ.get("RENDER_EXTERNAL_URL")         # Render
    hf_url       = os.environ.get("SPACE_HOST")                  # HuggingFace Spaces
    public_url   = render_url or (f"https://{hf_url}" if hf_url else None)

    # Fallback: local IP
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        local_ip = "127.0.0.1"

    print("\n" + "=" * 55)
    print("  [Plant Disease Detection App]  [PRODUCTION]")
    print("=" * 55)
    print(f"  Host  : 0.0.0.0")
    print(f"  Port  : {port}")
    print(f"  Debug : {debug}")
    print(f"  Local : http://{local_ip}:{port}")
    if public_url:
        print(f"  Public: {public_url}")
    print("=" * 55 + "\n")

    app.run(host="0.0.0.0", port=port, debug=debug,
            use_reloader=False, threaded=True)

