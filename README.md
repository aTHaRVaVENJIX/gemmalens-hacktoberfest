# 🔍 Gemma 4 Visual Defect Triage Agent
### Hacktoberfest Track 1: *"The Bug That Only Exists on Screen"*

![Gemma 4 Vision QA Dashboard Preview](docs/dashboard_preview.jpg)

An AI-powered visual QA triage agent built with **FastAPI**, **Gemma 4** (`gemma-4-31b-it` / `gemma-4-26b-a4b-it`) via the **Google GenAI SDK**, and a dark-mode **Tailwind CSS** dashboard. It diagnoses frontend layout defects that unit tests miss and synthesizes surgical CSS/HTML patches.

---

## 🌟 Why This Exists (Track 1 Challenge)

Traditional automated testing suites (Jest, Cypress DOM assertions, Playwright unit tests) check DOM presence and element attributes, but:
1. **They cannot perceive spatial collisions** caused by default flexbox shrinking behavior.
2. **They do not compute GPU compositor stacking contexts** that trap high `z-index` modals behind lower `z-index` sidebars.
3. **They miss horizontal viewport blowouts** caused by `100vw` ignoring scrollbar metrics on mobile screens.

This agent takes real screen renders and uses **Gemma 4's multimodal spatial vision** paired with an expert CSS layout diagnostic system prompt to inspect bounding boxes, identify the rendering failure, and generate the exact CSS fix.

---

## 🚀 Project Architecture

```
├── backend/
│   ├── .env.example          # Environment variable template with GEMINI_API_KEY
│   ├── requirements.txt      # FastAPI, Uvicorn, google-genai, Pillow, etc.
│   └── main.py               # FastAPI backend with Gemma 4 visual QA prompt & triage endpoint
├── frontend/
│   └── index.html            # Dark-mode dashboard (Tailwind, Marked.js, Canvas bug simulators)
├── tests/
│   ├── sample_test_notes.md  # Detailed test notes with Before/After specs for judges
│   ├── case1_flexbox_overlap.html            # Interactive reproduction for Case 1
│   ├── case2_modal_zindex_clip.html          # Interactive reproduction for Case 2
│   └── case3_mobile_viewport_overflow.html   # Interactive reproduction for Case 3
└── README.md
```

---

## 🛠️ Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- A Google AI Studio API key with access to Gemma 4

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env
```
Edit `backend/.env` and insert your Gemini API Key:
```env
GEMINI_API_KEY=AIzaSy...
GEMMA_MODEL=gemma-4-31b-it
HOST=0.0.0.0
PORT=8000
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Run the Server
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Open your browser at **[http://localhost:8000](http://localhost:8000)**. The FastAPI server automatically serves the frontend dashboard at `/`!

---

## 🧪 Built-in Judge Evaluation Suite

Judges can evaluate the triage agent immediately with **zero setup**:
1. Click any of the **Quick Test Cases** buttons on the dashboard:
   - **1. Flex Overlap**: Missing `min-width: 0` causes badge and title collisions.
   - **2. Modal Z-Clip**: CSS `transform` isolates `z-index: 9999` dialog behind sidebar.
   - **3. Mobile 100vw**: `100vw` causes unwanted horizontal scrollbars on 375px screens.
2. The UI instantly synthesizes a high-fidelity visual defect screenshot using HTML5 canvas.
3. Click **"Execute Visual Triage"** to watch Gemma 4 analyze the image and generate the Markdown triage report.
4. Open the standalone test cases in `tests/` (`case1_flexbox_overlap.html`, `case2_modal_zindex_clip.html`, `case3_mobile_viewport_overflow.html`) to toggle live between Before (Buggy) and After (Fixed) states!
