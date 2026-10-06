# 👁️ GemmaLens

**Automated Visual Defect Triage & Layout Patch Synthesis powered by Gemma 4**  
*Built for Hacktoberfest KBTCOE 2026 — Track 1: Best Use of Gemma 4*

---

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-Available%20Online-22c55e?style=for-the-badge&logo=googlechrome&logoColor=white)](https://briefs-dragon-aged-sources.trycloudflare.com)
[![Gemma 4](https://img.shields.io/badge/AI%20Model-Gemma%204%20%2F%20Flash-f5b726?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-e97b77?style=for-the-badge)](LICENSE)

---

## 🌐 Try It Online Right Now (No Setup Required)
GemmaLens is deployed and accessible publicly:

👉 **Live Demo:** **[https://briefs-dragon-aged-sources.trycloudflare.com](https://briefs-dragon-aged-sources.trycloudflare.com)**

*Upload any UI bug screenshot from your desktop or phone, describe the symptom, and watch GemmaLens analyze the spatial geometry and output copy-pasteable CSS patches.*

---

## 🚀 The Problem: "The Bug That Only Exists on Screen"
Frontend developers waste hours trying to reproduce visual UI bugs based on vague bug tickets (*"The badge overlaps the title on iPhone"* or *"The modal renders behind the navigation bar"*). 

Without clear console errors, debugging CSS flexbox collisions, broken z-index stacking contexts, and mobile viewport blowouts is a tedious game of guess-and-check. Traditional unit tests (Jest, Vitest) check DOM node existence, but **cannot compute rasterized GPU stacking contexts or subpixel font overflow**.

## 💡 The Solution
GemmaLens is a multimodal AI Quality Assurance engineer. Instead of hunting through thousands of lines of CSS, developers simply upload a screenshot of the broken UI. GemmaLens uses Google's multimodal vision models to analyze the spatial layout and DOM geometry, outputting:
1. **Visual Geometry Analysis:** Identifies overlapping boundaries, clipping zones, and isolated stacking contexts.
2. **Root Cause Diagnosis:** Pinpoints the exact CSS/HTML structural failure.
3. **Actionable Code Patch:** Generates production-ready CSS snippets and Tailwind utility equivalents.

---

## ✨ Key Features & Innovations

* **🎯 Interactive Defect Reticle HUD:** Overlays pulsing bounding boxes with exact coordinate tags on top of anomalous screen regions (`[🎯 HUD: ON/OFF]` toggle).
* **↔️ Interactive Before vs. After Split Slider:** Draggable neo-brutalist divider comparing broken component layout against the synthesized patch in real-time.
* **🎨 Pure CSS vs. ⚡ Tailwind Utility Switcher:** 1-click toggle to instantly swap code blocks between native CSS stylesheets and modern Tailwind utility classes, complete with 1-click clipboard copy.
* **🐙 One-Click GitHub Issue / PR Export:** Generates production-ready GitHub Issue markdown with collapsible `<details>` blocks, spatial telemetry, and suggested patches, with direct links to pre-fill new GitHub issues.
* **🧬 DOM Hierarchy X-Ray Breadcrumbs:** Visual breadcrumb trail (`<body> ➔ <div.dashboard> ➔ <div.flex-header> ➔ [💥 OFFENDING NODE]`) synchronized with the reticle target.
* **📱 Multi-Device Viewport Simulation:** Hardware preview frames with device bezels for **Mobile (375px)**, **Tablet (768px)**, and **Desktop**.
* **🔊 8-Bit Web Audio Sound FX:** Zero-dependency audio feedback using native Web Audio API oscillators for terminal scans, button clicks, and triage victory chords.
* **⚡ Real-Time Diagnostic Telemetry Ribbon:** Tracks live latency (~4–6s), spatial defect confidence (99.4%), viewport dimensions, and failover status.
* **🛡️ Dual-Key High-Availability Failover:** Built-in secondary API key redundancy to prevent rate-limit interruptions during high-traffic judging.

---

## 🖼️ Dashboard Preview
![GemmaLens Dashboard Preview](docs/dashboard_preview.jpg)

## 🎥 Demo Video
[Insert your YouTube/Vimeo Demo Link Here]

## 🛠️ Tech Stack
* **AI Model:** Google Gemma 4 (`gemma-4-31b-it`, `gemma-4-26b-a4b-it`) and Gemini 3.5 Flash via Google GenAI SDK
* **Backend:** Python 3.12, FastAPI, Uvicorn, Pillow (Image optimization & downscaling)
* **Frontend:** Vanilla JS, HTML5, Tailwind CSS, Marked.js, Highlight.js, Web Audio API
* **Deployment:** Render Blueprint (`render.yaml`), Procfile, TLS Tunnel

---

## 🏁 Setup Instructions

### Option A: Instant Web Access (Recommended)
Simply visit **[https://briefs-dragon-aged-sources.trycloudflare.com](https://briefs-dragon-aged-sources.trycloudflare.com)** in any browser.

---

### Option B: 1-Click Cloud Deployment (Render.com)
The repository includes a ready-to-use [`render.yaml`](render.yaml) blueprint:
1. Fork or push this repository to your GitHub account.
2. Sign in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** ➔ **Blueprint** ➔ Select `gemmalens-hacktoberfest`.
4. Add your `GEMINI_API_KEY` when prompted.
5. Click **Apply** — Render automatically builds and hosts the fullstack application on a free HTTPS URL.

---

### Option C: Local Developer Setup

#### 1. Clone the repository
```bash
git clone https://github.com/aTHaRVaVENJIX/gemmalens-hacktoberfest.git
cd gemmalens-hacktoberfest
```

#### 2. Configure Environment Variables
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
GEMINI_API_KEY_BACKUP=your_backup_api_key_here   # Optional backup key
DEFAULT_MODEL=gemini-3.5-flash-lite
```

#### 3. Install Dependencies & Run the Server
```bash
# Using Python venv
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 4. Launch the Frontend
The FastAPI server automatically serves the frontend at `http://localhost:8000`.  
Alternatively, run the frontend standalone:
```bash
cd frontend
python3 -m http.server 3000
```
Open `http://localhost:3000` in your browser.

---

## 🧪 The Judge Test Suite
To evaluate the model's accuracy on deterministic failure modes without manual uploads, click any of the **Judge Quick Test Cases** in the dashboard:

| Case | Bug Pattern | Why Unit Tests Miss It | Gemma 4 Solution |
|---|---|---|---|
| **#01 Flexbox Child Overlap** | Unconstrained flex item pushing sibling badges off screen | DOM node exists; mock layout engines don't calculate flex item min-width auto | Injects `min-width: 0; flex: 1 1 0%;` with text truncation |
| **#02 Modal Z-Index Clip** | Dialog with `z-index: 9999` rendering under `z-index: 10` sidebar | Parent `transform` traps modal in local stacking context | Hoists modal outside trapping transform or recommends native `<dialog>` |
| **#03 Mobile 100vw Blowout** | Content spilling past 375px mobile viewport | `100vw` includes vertical scrollbar width on mobile browsers | Converts fixed viewport unit to fluid `width: 100%` and `clamp()` typography |

---

## 📄 License
Developed by Atharva for Hacktoberfest Nashik 2026. License: MIT.
