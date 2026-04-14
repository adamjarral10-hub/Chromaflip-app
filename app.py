"""
Image Colorizer / Grayscale Converter
Flask Web Application
Developed by Adam Jarral
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

# ── App Configuration ────────────────────────────────────────────────────────

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max upload

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    """Return True if the file extension is in the allowed set."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_grayscale(img: Image.Image) -> bool:
    """
    Detect whether a PIL image is grayscale (or near-grayscale).
    Works for both 'L' mode images and 'RGB' images whose channels are equal.
    """
    if img.mode == 'L':
        return True

    rgb = img.convert('RGB')
    arr = np.array(rgb).astype(np.int16)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    # Mean absolute difference between channels
    diff = (np.abs(r - g) + np.abs(g - b) + np.abs(r - b)) / 3
    return float(diff.mean()) < 8.0     # threshold: < 8 intensity units avg


def colorize_image(img: Image.Image) -> Image.Image:
    """
    Apply a warm-tinted false colorization to a grayscale image.
    Uses a perceptually-inspired LUT that maps luminance →
    a warm amber-teal gradient, giving a realistic antique-photo feel.
    """
    gray = img.convert('L')
    arr = np.array(gray, dtype=np.float32) / 255.0  # [0, 1]

    # Build RGB channels from luminance using a warm cinematic grade
    r = np.clip(0.9 * arr + 0.15 * (arr ** 2), 0, 1)          # warm highlights
    g = np.clip(0.75 * arr + 0.05 * np.sin(arr * np.pi), 0, 1) # mid-tone green
    b = np.clip(0.55 * arr + 0.20 * (1 - arr) ** 2, 0, 1)      # cool shadows

    rgb = np.stack([r, g, b], axis=-1)
    rgb = (rgb * 255).astype(np.uint8)
    return Image.fromarray(rgb, 'RGB')


def process_image(src_path: str) -> tuple[str, str]:
    """
    Load the image, detect type, apply transformation, save result.
    Returns (mode_label, output_filename).
    """
    img = Image.open(src_path)

    if is_grayscale(img):
        # B&W → Colorized
        result = colorize_image(img)
        mode = 'colorized'
    else:
        # Color → Grayscale
        result = img.convert('L').convert('RGB')  # keep 3-ch for consistent display
        mode = 'grayscale'

    # Save with unique name
    ext = os.path.splitext(src_path)[1].lower() or '.jpg'
    out_name = f"processed_{uuid.uuid4().hex[:8]}{ext}"
    out_path = os.path.join(UPLOAD_FOLDER, out_name)
    result.save(out_path)
    return mode, out_name


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Handle image upload + processing; return JSON with file paths."""

    # ── Validation ──
    if 'image' not in request.files:
        return jsonify({'error': 'No file field in request.'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type. Please upload JPG, PNG, or WEBP.'}), 400

    # ── Save original ──
    safe_name = secure_filename(file.filename)
    orig_name = f"orig_{uuid.uuid4().hex[:8]}_{safe_name}"
    orig_path = os.path.join(UPLOAD_FOLDER, orig_name)
    file.save(orig_path)

    # ── Process ──
    try:
        mode, proc_name = process_image(orig_path)
    except Exception as exc:
        return jsonify({'error': f'Image processing failed: {str(exc)}'}), 500

    return jsonify({
        'original': f'static/uploads/{orig_name}',
        'processed': f'static/uploads/{proc_name}',
        'mode': mode,          # 'colorized' | 'grayscale'
    })


# ── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
