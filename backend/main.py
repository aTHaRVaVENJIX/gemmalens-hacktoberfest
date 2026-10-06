import os
import io
import mimetypes
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize FastAPI app
app = FastAPI(
    title="Visual Defect Triage Agent - Gemma 4",
    description="Track 1 Hacktoberfest: 'The Bug That Only Exists on Screen'. AI-powered visual QA layout defect analysis and CSS patch generator.",
    version="1.0.0",
)

# Enable CORS for developer ease
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rigorous QA System Prompt for Gemma 4
SYSTEM_PROMPT = """You are Gemma Vision QA, an elite Principal Frontend QA Engineer and CSS Layout Architecture Specialist.
Your mission is to analyze visual defects submitted for Hacktoberfest Track 1: "The Bug That Only Exists on Screen".

You specialize in visual anomalies that unit and integration tests cannot catch:
- Stacking context traps (z-index isolation via opacity, transform, filter, or will-change)
- Flexbox child collapse, missing min-width: 0, text truncation failures, and nowrap collisions
- Mobile viewport font / horizontal scroll overflow (100vw vs 100%, unconstrained tables, pre/code blocks)
- CSS Grid auto-placement blowouts, subpixel rounding clipping, and alignment glitches
- Responsive breakpoint collapse and media query boundaries

When analyzing the provided UI screenshot and user description, produce a comprehensive, structured Markdown triage report with the following EXACT structure:

# 🔍 Visual Defect Triage Report

## 1. Executive Summary & Defect Severity
- **Defect Title**: Concise, technical title describing the rendering bug
- **Severity Rating**: [Critical / Major / Moderate / Cosmetic] with clear justification
- **Defect Classification**: [e.g., Flexbox Collapsed Child / Stacking Context Isolation / Viewport Overflow / Subpixel Glitch / Responsive Miscalculation]
- **Visual Symptoms**: Crisp 2-3 sentence overview of what is visually broken on screen.

## 2. Visual Anomaly Analysis
- **Screen Region & Bounding Coordinates**: Exact location where the flaw manifests (e.g., header right-rail, modal backdrop, card content container).
- **Element Collisions & Clipping**: Detailed breakdown of which DOM/rendered bounding boxes are overlapping, clipped, wrapped improperly, or hidden behind other layers.
- **Visual Artifacts**: Note any unwanted scrollbars, cut-off text glyphs, misaligned baselines, or color/contrast legibility failures.

## 3. Probable Root Causes
- Detail the underlying browser rendering engine mechanics and CSS specifications causing this issue.
- Highlight specific CSS properties and anti-patterns responsible (e.g., `flex-shrink: 0` missing, `overflow: hidden` on parent creating unexpected clipping, `transform` inducing a new local stacking context neutralizing `z-index: 9999`, `width: 100vw` factoring in scrollbar widths).

## 4. Minimal Reproduction Steps & Environment Matrix
- **Target Viewport**: Screen resolutions / widths where the defect triggers (e.g., Mobile < 375px, Tablet 768px-1024px, Desktop > 1440px).
- **DOM Hierarchy & Trigger Conditions**: Necessary element nesting and styling conditions.
- **Step-by-Step Reproduction**:
  1. Set viewport to...
  2. Render container with...
  3. Observe visual collision at...

## 5. Recommended Code Patch & CSS Fix
Provide concrete, production-ready code fixes:
- ### ❌ Root Cause Code (Buggy / Before)
  Provide the flawed CSS/HTML snippet in a code block. Highlight the exact error causing the visual bug.
- ### ✅ Patched Code (Fixed / After)
  Provide the corrected CSS/HTML or Tailwind CSS utility classes in a code block.
- **Unified Diff (Optional)**: If helpful, include a ````diff code block using `-` for buggy lines and `+` for patched lines.
- **Explanation of Patch**: Explain why this exact modification resolves the visual defect without introducing layout regressions to adjacent sibling elements.
- **Alternative / Defensive Solutions**: One secondary fix (e.g., CSS clamp(), modern flex-wrap, or container queries).

Format your output in clean, readable, professional GitHub-flavored Markdown. Be precise, technical, and actionable.
"""

def get_gemini_client(use_backup: bool = False):
    key_name = "GEMINI_API_KEY_BACKUP" if use_backup else "GEMINI_API_KEY"
    api_key = os.getenv(key_name) or os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() in ("", "your_gemini_api_key_here"):
        return None, f"{key_name} is not configured. Please set your API key in backend/.env."
    try:
        from google import genai
        client = genai.Client(api_key=api_key.strip())
        return client, None
    except Exception as e:
        return None, f"Failed to initialize google-genai Client: {str(e)}"


@app.get("/api/health")
async def health_check():
    api_key = os.getenv("GEMINI_API_KEY", "")
    has_valid_key = bool(api_key and api_key.strip() != "your_gemini_api_key_here")
    has_backup = bool(os.getenv("GEMINI_API_KEY_BACKUP", "").strip())
    default_model = os.getenv("GEMMA_MODEL", "gemini-3.5-flash-lite")
    return {
        "status": "healthy",
        "api_key_configured": has_valid_key,
        "backup_key_configured": has_backup,
        "default_model": default_model,
        "supported_models": [
            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemma-4-26b-a4b-it",
            "gemma-4-31b-it"
        ],
        "track": "Track 1: The Bug That Only Exists on Screen"
    }


@app.get("/api/samples")
async def get_samples():
    """Return preset test cases for judges and demo testing."""
    return [
        {
            "id": "flexbox-overlap",
            "title": "Flexbox Child Overlap & Truncation Bug",
            "category": "Flexbox Layout",
            "severity": "Major",
            "description": "In a card layout with flex-row, an action badge overlaps the long title text instead of wrapping or truncating cleanly with an ellipsis. The container shrinks on narrow viewports but child elements collide.",
            "expected_fix": "Add min-width: 0 to flex child container, flex-shrink: 1, and text-overflow: ellipsis."
        },
        {
            "id": "modal-zindex-clip",
            "title": "Modal Z-Index Trap & Stacking Context Isolation",
            "category": "Stacking Context",
            "severity": "Critical",
            "description": "A modal dialog with z-index: 9999 renders behind an adjacent sidebar that only has z-index: 10. The modal appears cut off and dark overlay is trapped inside a parent div.",
            "expected_fix": "Remove transform/filter/will-change on the parent element or hoist the modal to the document body via React Portal / native <dialog>."
        },
        {
            "id": "mobile-viewport-overflow",
            "title": "Mobile Viewport Horizontal Scrollbar Blowout",
            "category": "Responsive Layout",
            "severity": "Major",
            "description": "On mobile devices (< 390px), horizontal scrolling appears unexpectedly. A headline with large fixed font-size and an unconstrained code block forces the viewport body width to 480px, causing white margin gaps on the right.",
            "expected_fix": "Replace width: 100vw with width: 100%, apply overflow-x: auto and max-width: 100% on code containers, and use clamp() for fluid typography."
        }
    ]


@app.post("/api/triage")
async def triage_visual_defect(
    file: UploadFile = File(...),
    description: str = Form(""),
    model: Optional[str] = Form(None)
):
    """
    Accepts an uploaded UI screenshot and bug description, forwarding them
    to Gemma 4 via Google AI Studio API for visual defect analysis and automated CSS patching.
    Optimized for high-speed evaluation in 5-10 seconds with automatic key failover.
    """
    import time
    start_time = time.time()

    client, error_msg = get_gemini_client(use_backup=False)
    if not client:
        raise HTTPException(status_code=400, detail=error_msg)

    # Validate image file
    filename = file.filename or "screenshot.png"
    guessed_type, _ = mimetypes.guess_type(filename)
    content_type = file.content_type or guessed_type or "image/png"
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded file must be an image (received: {content_type})"
        )

    try:
        image_bytes = await file.read()
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Validate with Pillow
        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            pil_image.load()
        except Exception as img_err:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image format or corrupt file: {str(img_err)}"
            )

        orig_w, orig_h = pil_image.width, pil_image.height

        # Optimize image: downscale if width/height > 1024 to dramatically accelerate vision tokens
        if pil_image.width > 1024 or pil_image.height > 1024:
            pil_image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

        opt_buf = io.BytesIO()
        if pil_image.mode in ("RGBA", "P"):
            rgb_img = Image.new("RGB", pil_image.size, (255, 255, 255))
            if pil_image.mode == "RGBA":
                rgb_img.paste(pil_image, mask=pil_image.split()[3])
            else:
                rgb_img.paste(pil_image)
            rgb_img.save(opt_buf, format="JPEG", quality=85, optimize=True)
        else:
            pil_image.save(opt_buf, format="JPEG", quality=85, optimize=True)

        opt_bytes = opt_buf.getvalue()

        # Determine target model (defaults to ultra-fast gemini-3.5-flash-lite)
        target_model = model or os.getenv("GEMMA_MODEL", "gemini-3.5-flash-lite")

        user_prompt_text = (
            f"### User Bug Description:\n{description.strip() if description.strip() else 'Visually examine this screenshot for layout collisions, text overflows, or stacking anomalies.'}\n\n"
            f"Image Dimensions: {orig_w}x{orig_h}.\n"
            f"Please conduct an in-depth visual triage and provide the complete CSS defect triage report according to your instructions. Be technical, precise, and concise."
        )

        from google.genai import types

        image_part = types.Part.from_bytes(
            data=opt_bytes,
            mime_type="image/jpeg"
        )

        # Call with primary client, with auto-failover to backup client if needed
        response = None
        used_model = target_model
        try:
            response = client.models.generate_content(
                model=target_model,
                contents=[image_part, user_prompt_text],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=950
                )
            )
        except Exception as primary_err:
            backup_client, _ = get_gemini_client(use_backup=True)
            if backup_client:
                # Retry with backup key & fallback model if needed
                fallback_model = "gemini-3.5-flash-lite" if target_model in ("gemma-4-31b-it", "gemma-4-26b-a4b-it") else target_model
                response = backup_client.models.generate_content(
                    model=fallback_model,
                    contents=[image_part, user_prompt_text],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2,
                        max_output_tokens=950
                    )
                )
                used_model = fallback_model
            else:
                raise primary_err

        report_markdown = response.text or "No report content was returned."
        elapsed = round(time.time() - start_time, 2)

        return {
            "status": "success",
            "model": used_model,
            "filename": filename,
            "dimensions": {"width": orig_w, "height": orig_h},
            "elapsed_seconds": elapsed,
            "report": report_markdown
        }

    except HTTPException:
        raise
    except Exception as e:
        error_detail = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Triage Inference Error: {error_detail}"
        )


# Mount frontend if available
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists() and (frontend_dir / "index.html").exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(frontend_dir / "index.html")


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    print(f"🚀 Starting Gemma 4 Visual Defect Triage Server on http://{host}:{port}")
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)
