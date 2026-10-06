# Visual Defect Test Suite for Judges
## Track 1: "The Bug That Only Exists on Screen"
### Model Target: Gemma 4 (`gemma-4-31b-it` / `gemma-4-26b-a4b-it`)

This test suite documents 3 classic visual defects that **pass DOM/Jest unit tests with 100% green checks**, but completely break when rendered on an actual screen.

---

## Test Case 1: Flexbox Child Overlap & Text Truncation Failure

### 1. Defect Profile
- **Test ID**: `TC-VISUAL-001`
- **Category**: Flexbox Spatial Collision
- **Severity**: Major
- **Screen Viewport**: Desktop / Responsive Tablet (Widths < 900px)
- **Why Unit Tests Miss It**: DOM elements exist, inner text matches assertion, and `node.clientHeight > 0`. Jest tests do not compute font metrics, inline text boundaries, or flex item shrink resistance.

### 2. Flawed Code (Before)
```html
<div class="card-header" style="display: flex; align-items: center; width: 450px;">
  <!-- Bug: flex items have min-width: auto by default -->
  <div class="title-wrapper">
    <h3 style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
      Production Incident: PostgreSQL replication lag spike across us-east-1 cluster
    </h3>
  </div>
  <span class="badge" style="background: #ef4444; color: white; padding: 4px 10px; border-radius: 9999px; white-space: nowrap;">
    P0 CRITICAL
  </span>
</div>
```

### 3. Visual Before (Buggy Screen State)
- **Visual Anomaly**: The `.badge` is shoved to the right edge or physically overlaps the `.title-wrapper` text.
- **Defect Symptom**: Despite `text-overflow: ellipsis` on the `h3`, the text does **not** truncate! Instead, the flex item `.title-wrapper` refuses to shrink below its content's intrinsic width because the CSS Flexbox specification gives flex items an implicit `min-width: auto`.
- **User Impact**: Text renders unreadable under the badge; container borders are broken.

### 4. Visual After (Fixed State with Gemma 4 Patch)
- **Corrected Code**:
```html
<div class="card-header" style="display: flex; align-items: center; width: 450px;">
  <!-- Fix: min-width: 0 allows flex item to shrink below intrinsic content width -->
  <div class="title-wrapper" style="min-width: 0; flex: 1 1 0%;">
    <h3 style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin: 0;">
      Production Incident: PostgreSQL replication lag spike across us-east-1 cluster
    </h3>
  </div>
  <span class="badge" style="flex-shrink: 0; margin-left: 12px; background: #ef4444; color: white; padding: 4px 10px; border-radius: 9999px; white-space: nowrap;">
    P0 CRITICAL
  </span>
</div>
```
- **Visual Expectation**: Title truncates smoothly with `...` right before the badge, with clean 12px margin padding between text and badge.

---

## Test Case 2: Modal Z-Index Isolation Trap & Stacking Context Clipping

### 1. Defect Profile
- **Test ID**: `TC-VISUAL-002`
- **Category**: Stacking Context Isolation
- **Severity**: Critical
- **Screen Viewport**: All screen resolutions
- **Why Unit Tests Miss It**: Testing libraries check `element.style.zIndex === '9999'` and check that the modal is visible in the DOM. Stacking contexts are computed solely by the browser's painting engine.

### 2. Flawed Code (Before)
```html
<!-- Parent card uses transform or filter -->
<div class="dashboard-widget" style="position: relative; transform: translate3d(0, 0, 0); overflow: hidden; border: 1px solid #334155;">
  <h3>Server Configuration</h3>
  <button id="open-btn">Delete Server</button>

  <!-- Modal nested inside card -->
  <div class="modal-overlay" style="position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 9999; display: flex; align-items: center; justify-content: center;">
    <div class="modal-dialog" style="background: #1e293b; padding: 24px; border-radius: 12px;">
      <h2>Confirm Destruction</h2>
      <p>Are you sure you want to delete this cluster?</p>
    </div>
  </div>
</div>

<aside class="sidebar-nav" style="position: fixed; top: 0; left: 0; width: 260px; height: 100vh; background: #0f172a; z-index: 10;">
  Navigation Links
</aside>
```

### 3. Visual Before (Buggy Screen State)
- **Visual Anomaly**: The modal with `z-index: 9999` is rendered **underneath** the sidebar navigation that only has `z-index: 10`.
- **Defect Symptom**: Furthermore, the dark backdrop is clipped by `.dashboard-widget`'s `overflow: hidden`, only covering the 300px card instead of the full viewport!
- **Underlying Cause**: `transform: translate3d(0,0,0)` creates a new CSS Stacking Context on `.dashboard-widget`. The child modal's `z-index: 9999` is scoped only *inside* that widget; relative to the root page, the modal only has the stacking rank of its parent.

### 4. Visual After (Fixed State with Gemma 4 Patch)
- **Corrected Code**:
```html
<!-- Clean Widget without stacking traps -->
<div class="dashboard-widget" style="position: relative; border: 1px solid #334155;">
  <h3>Server Configuration</h3>
  <button id="open-btn">Delete Server</button>
</div>

<!-- Modal hoisted to root body (or using HTML5 <dialog> or React createPortal) -->
<dialog class="modal-dialog-native" style="border: none; border-radius: 12px; background: #1e293b; color: white; padding: 24px;">
  <h2>Confirm Destruction</h2>
  <p>Are you sure you want to delete this cluster?</p>
</dialog>
```
- **Visual Expectation**: Modal appears on top layer (`#top-layer` or root stacking context), backdrop smoothly darkens entire 100vw x 100vh screen, completely covering sidebar and widgets.

---

## Test Case 3: Mobile Viewport 100vw Horizontal Scrollbar Blowout

### 1. Defect Profile
- **Test ID**: `TC-VISUAL-003`
- **Category**: Viewport Metrics & Typography Overflow
- **Severity**: Major
- **Screen Viewport**: Mobile Viewport (< 390px, e.g. iPhone 13/14/SE)
- **Why Unit Tests Miss It**: Emulated headless DOM environments like jsdom do not render real scrollbars, so `document.body.scrollWidth` equals `window.innerWidth`.

### 2. Flawed Code (Before)
```html
<body style="margin: 0; padding: 0;">
  <!-- Bug: 100vw includes scrollbar width, causing viewport blowout -->
  <section class="hero-banner" style="width: 100vw; background: linear-gradient(135deg, #0ea5e9, #6366f1); padding: 48px 24px;">
    <!-- Large fixed font doesn't fit on 320px-375px screens -->
    <h1 style="font-size: 42px; font-weight: 800; white-space: nowrap;">
      Accelerate Your AI Engineering Workflow Today
    </h1>
    <pre style="background: #0f172a; padding: 16px;"><code>$ git clone https://github.com/example/very-long-unbroken-command-string-that-stretches-the-container.git</code></pre>
  </section>
</body>
```

### 3. Visual Before (Buggy Screen State)
- **Visual Anomaly**: An unwanted horizontal scrollbar appears at the bottom of the mobile viewport. Users can pan sideways into an unsightly empty white gutter.
- **Defect Symptom**:
  1. `width: 100vw` calculates viewport width *including* vertical scrollbars, forcing an extra ~15px width blowout.
  2. The `h1` has fixed `42px` font with `white-space: nowrap`, spanning over 600px wide.
  3. The `pre > code` block has no `overflow-x: auto` and stretches parent width.

### 4. Visual After (Fixed State with Gemma 4 Patch)
- **Corrected Code**:
```html
<body style="margin: 0; padding: 0; overflow-x: hidden;">
  <!-- Fix: width: 100% or max-width: 100% prevents scrollbar blowouts -->
  <section class="hero-banner" style="width: 100%; box-sizing: border-box; background: linear-gradient(135deg, #0ea5e9, #6366f1); padding: 32px 16px;">
    <!-- Fluid typography via clamp() and wrapping -->
    <h1 style="font-size: clamp(1.75rem, 5vw + 1rem, 2.5rem); font-weight: 800; word-break: break-word; line-height: 1.2;">
      Accelerate Your AI Engineering Workflow Today
    </h1>
    <!-- Scrollable code block -->
    <pre style="background: #0f172a; padding: 16px; border-radius: 8px; overflow-x: auto; max-width: 100%;"><code style="font-family: monospace;">$ git clone https://github.com/example/repo.git</code></pre>
  </section>
</body>
```
- **Visual Expectation**: Clean mobile render with 0 horizontal scroll; typography scales responsively, code snippet scrolls internally without expanding page canvas.
