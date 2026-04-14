# ◈ ChromaFlip — Image Colorizer / Grayscale Converter

> A Flask web app that automatically detects whether an uploaded image is black & white or coloured, then applies the opposite transformation — instantly.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.1-green?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-orange?style=flat-square)

---

## ✨ Features

- **Auto-detection** — analyses pixel channels to determine image type
- **B&W → Color** — applies a warm cinematic colorization to grayscale images
- **Color → Grayscale** — converts full-colour images to high-quality black & white
- **Drag & drop upload** — with instant thumbnail preview
- **Download results** — save both original and processed images
- **Responsive UI** — works on desktop and mobile
- **Production-ready** — Gunicorn + Render/Railway/Heroku deployment out of the box

---

## 📁 Project Structure

```
image-colorizer/
├── app.py                  # Flask backend (routes + image processing)
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment process file (gunicorn)
├── runtime.txt             # Python version for Render/Heroku
├── .gitignore
├── README.md
├── templates/
│   └── index.html          # Main HTML page (Bootstrap + custom JS)
└── static/
    ├── style.css            # Custom stylesheet
    └── uploads/             # Uploaded & processed images (auto-created)
```

---

## 🚀 Local Setup

### 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/image-colorizer.git
cd image-colorizer
```

### 2 — Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Run the development server

```bash
python app.py
```

### 5 — Open in browser

```
http://localhost:5000
```

---

## 🌐 Deployment

### Render (recommended — free tier)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Add environment variable: `SECRET_KEY` → any random string
6. Click **Deploy**

### Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Railway auto-detects the `Procfile`
4. Add `SECRET_KEY` environment variable
5. Deploy

### Heroku

```bash
heroku create your-app-name
git push heroku main
heroku open
```

---

## ⚙️ How It Works

| Input | Detection Logic | Output |
|-------|-----------------|--------|
| Grayscale / B&W image | Mean channel difference < 8 | Warm cinematic colorization |
| Full-colour image | Mean channel difference ≥ 8 | High-quality grayscale |

The colorization algorithm maps luminance values to a warm amber-teal gradient without any ML model, keeping the app lightweight and fast.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask 3.1 |
| Image processing | Pillow (PIL), NumPy |
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| Production server | Gunicorn |

---

## 📄 License

MIT © Adam Jarral

---

*Developed by **Adam Jarral***
