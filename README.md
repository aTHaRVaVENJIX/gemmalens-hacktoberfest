# 👁️ GemmaLens

**Automated Visual Defect Triage powered by Gemma 4**  
*Built for Hacktoberfest KBTCOE 2026 — Track 1: Best Use of Gemma 4*

---

## 🚀 The Problem: "The Bug That Only Exists on Screen"
Frontend developers waste hours trying to reproduce visual UI bugs based on vague user reports (e.g., *"The avatar looks squished on my phone"*). Without clear console errors, debugging CSS flexbox collisions, broken z-index stacking contexts, and mobile viewport blowouts is a tedious game of guess-and-check.

## 💡 The Solution
GemmaLens is a multimodal AI Quality Assurance engineer. Instead of hunting for the CSS failure, developers simply upload a screenshot of the broken UI. GemmaLens uses Google's `gemma-4-31b-it` model to analyze the spatial layout and DOM geometry, outputting:
1. **Visual Geometry Analysis:** Identifies overlapping boundaries and clipping.
2. **Root Cause Diagnosis:** Pinpoints the exact CSS/HTML structural failure.
3. **Actionable Code Patch:** Generates the precise CSS snippet required to fix the layout.

## 🖼️ Dashboard Preview
![GemmaLens Dashboard Preview](docs/dashboard_preview.jpg)

## 🎥 Demo Video
[Insert your YouTube/Vimeo Demo Link Here]

## 🛠️ Tech Stack
* **AI Model:** Google Gemma 4 (`gemma-4-31b-it`) via Gemini API
* **Backend:** Python, FastAPI, Uvicorn, Google GenAI SDK
* **Frontend:** Vanilla JS, HTML5, Tailwind CSS
* **Parsing:** Marked.js (Markdown rendering)

## 🏁 Quickstart (Local Setup)

**1. Clone the repository**
```bash
git clone https://github.com/aTHaRVaVENJIX/gemmalens-hacktoberfest.git
cd gemmalens-hacktoberfest
```

**2. Configure Environment & Install Dependencies**
```bash
cp backend/.env.example backend/.env
pip install -r backend/requirements.txt
```
*Add your `GEMINI_API_KEY` to `backend/.env`.*

**3. Run the Backend & Frontend**
```bash
# Start FastAPI backend
uvicorn backend.main:app --reload --port 8000

# Serve frontend
python -m http.server 3000 --directory frontend
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## 🧪 Built-in Judge Evaluation Suite
Judges can evaluate the triage agent immediately with **zero setup**:
1. Click any of the **Quick Test Cases** buttons on the dashboard:
   - **Case 01 — Flexbox Collision**: Missing `min-width: 0` causes badge and title overlap.
   - **Case 02 — Modal Z-Index Clip**: CSS `transform` traps a `z-index: 9999` dialog behind the sidebar.
   - **Case 03 — Mobile 100vw**: `100vw` introduces unwanted horizontal scrollbars on 375px screens.
2. Click **"Execute Visual Triage"** to watch the model diagnose the screen defect and generate syntax-highlighted CSS fixes with red/green diff annotations.
