# 🖼️ Image Editor — Streamlit & OpenCV

An interactive, browser-based image editing application built with **Python**, **Streamlit**, and **OpenCV**.  
Upload any image, apply visual filters in real time, and download the result — no HTML or CSS required.

---

## 📸 Screenshot

> _Add a screenshot of the running app here after your first run._  
> Example: `![
App Screenshot](screenshot.png)`
<img width="1920" height="1080" alt="Screenshot (1007)" src="https://github.com/user-attachments/assets/89fbab75-3dfb-4d10-9b06-9a0f6858848c" />

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/image-editor.git
cd image-editor
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🎛️ Filters Implemented

| Filter | Widget | Key Parameter(s) | OpenCV Function |
|---|---|---|---|
| **Blur** | Slider | `ksize`: 1–51 (odd) | `cv2.GaussianBlur` |
| **Sharpness** | Slider | `alpha`: 0.0–3.0 | Unsharp mask via `cv2.addWeighted` |
| **Brightness** | Slider | `beta`: –100 to 100 | `cv2.convertScaleAbs` |
| **Contrast** | Slider | `alpha`: 0.5–3.0 | `cv2.convertScaleAbs` |
| **Edge Detection** | Checkbox + sliders | `thresh1`, `thresh2` | `cv2.Canny` |
| **Grayscale** | Checkbox | on / off | `cv2.cvtColor` |

> **Filters are stackable** — applied in sequence (grayscale → brightness → contrast → blur → sharpness → edge detection) every time a slider changes, using the original image as the base.

---

## 📁 Project Structure

```
image_editor/
├── app.py           # Main Streamlit application & UI layout
├── filters.py       # All OpenCV filter functions
├── utils.py         # PIL ↔ NumPy ↔ bytes conversion helpers
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---
## 📝 How It Works

1. **Upload** a JPG or PNG via the file uploader.
2. **Adjust** sliders and toggles in the sidebar — changes are applied instantly.
3. **Preview** the original and processed images side-by-side.
4. **Download** the final result as a PNG with one click.
5. **Reset** all filters to defaults using the Reset button.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — Web UI framework
- [OpenCV](https://opencv.org/) (`opencv-python`) — Image processing
- [NumPy](https://numpy.org/) — Array manipulation
- [Pillow](https://python-pillow.org/) — Image loading & format conversion
