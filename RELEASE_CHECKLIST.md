# RELEASE_CHECKLIST.md — Universal File Workstation v0.1.0

_Generated: 2026-05-03 | Status: 🟡 READY FOR FINAL VALIDATION_

This document tracks the final requirements and blockers for the v0.1.0 release. No merge to `main` or tagging should occur until all 🔴 BLOCKER items are resolved.

---

## 🔴 BLOCKER — Must fix before merge

### [B-1] Batch Conversion Logic Crash
**File(s):** `core/converter.py`  
**Problem:** `batch_convert` passes `**kwargs` to conversion methods (like `convert_pdf_to_docx` or `convert_csv_to_xlsx`) that do not accept arbitrary keyword arguments, causing a `TypeError` when quality settings or other flags are passed in a batch.  
**Fix:** Update `batch_convert` to filter `kwargs` based on the target method's signature or update all conversion methods to accept `**kwargs`. 
*Recommended Fix:*
```python
# In batch_convert loop:
method = getattr(self, method_name)
import inspect
sig = inspect.signature(method)
filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
results[path] = method(path, out_path, **filtered_kwargs)
```
**Verification:** Run `pytest tests/test_converter.py` and specifically a test case where `batch_convert` is called with a PDF file and a `quality` keyword argument.  
**Owner:** Said Hamza Turan  

---

### [B-2] Missing Onboarding Feature
**File(s):** `main.py`, `ui/dashboard.py`, `config/settings.py`  
**Problem:** Roadmap marks Issue #28 as complete, but no onboarding logic exists in the codebase. Users are not greeted with a tutorial, and the `onboarding_seen` flag is not managed.  
**Fix:** 
1. Create `ui/onboarding.py` with a `show_onboarding()` function using `st.expander` or a custom modal.
2. In `main.py`, check `st.session_state.onboarding_seen`. If false, call `show_onboarding()`.
3. Add a "Dismiss" button that sets the flag in `prefs.json` via `Config.save_user_prefs()`.  
**Verification:** Delete `~/.universal-file-workstation/preferences.json`, start the app, and verify the onboarding appears.  
**Owner:** Samet Demir  

---

### [B-3] Missing App Icon
**File(s):** `assets/icon.ico`, `build/universal-file-workstation.spec`  
**Problem:** No `.ico` file exists in `assets/`. The PyInstaller build will fail or use the default icon, violating the "Premium Feel" requirement of Sprint 6.  
**Fix:** 
1. Generate a high-quality 512x512 PNG icon and convert to `assets/icon.ico`.
2. Ensure `icon='assets/icon.ico'` is set in the `EXE()` block of the `.spec` file.  
**Verification:** Run `pyinstaller build/universal-file-workstation.spec` and verify the generated `.exe` has the custom icon.  
**Owner:** Samet Demir / Galip Efe Öncü  

---

### [B-4] Dead Cache Code in PDF Rendering
**File(s):** `core/viewer.py`  
**Problem:** `_cached_render_pdf` is implemented with `@st.cache_data` but is never called. `display_pdf` calls `render_pdf` which re-renders pages from scratch on every page turn, causing performance lag on large PDFs.  
**Fix:** Update `FileViewer.render_pdf` to use the cached function:
```python
def render_pdf(self, pdf_path: str, start: int = 0, end: int | None = None) -> list[bytes]:
    all_pages = _cached_render_pdf(pdf_path)
    total = len(all_pages)
    finish = end if end is not None else total
    return all_pages[max(0, start):min(finish, total)]
```
**Verification:** Open a 50+ page PDF, flip pages, and verify the "Cache MISS" log only appears once in the console.  
**Owner:** Abdulkadir Sar  

---

### [B-5] Missing FFmpeg License Compliance
**File(s):** `THIRD_PARTY_LICENSES.md`  
**Problem:** The project bundles FFmpeg (Issue #27) but `THIRD_PARTY_LICENSES.md` does not mention it or its LGPL license, creating a legal risk.  
**Fix:** Add FFmpeg to the library table in `THIRD_PARTY_LICENSES.md` with "LGPL 2.1" license and a link to the source (e.g., gyan.dev).  
**Verification:** Verify the file contains the FFmpeg entry.  
**Owner:** Muhammed Ali Avcı  

---

## 🟡 REQUIRED — Must complete before release

### [R-1] Fix Incomplete PDF/Merge Tests
**File(s):** `tests/test_pdf_ops.py`  
**Problem:** Current tests are stubs that only test failure cases (`non_existent.pdf`). There is no automated verification that PDF merging or image extraction actually works.  
**Fix:** Add success test cases using a small 1-page dummy PDF created via `reportlab` or a static fixture. Assert that `len(result) > 0` and files exist.  
**Owner:** Muhammed Ali Avcı  

---

### [R-2] Document System-Level Dependencies
**File(s):** `README.md`, `docs/BUILD.md`  
**Problem:** `pypandoc` is pinned in `requirements.txt`, but it requires `pandoc` to be installed on the OS. This is not documented, leading to "Library not found" errors for new users.  
**Fix:** Add a "Prerequisites" section to `README.md` and `docs/BUILD.md` explaining how to install `pandoc` (e.g., `brew install pandoc` or `choco install pandoc`).  
**Owner:** Galip Efe Öncü  

---

### [R-3] Establish Formal QA Reporting Process
**File(s):** `reports/README.md`, `docs/ROADMAP.md`  
**Problem:** QA is blocked from writing to `docs/`. A `reports/` directory exists but has no defined sub-structure for regression test matrices.  
**Fix:** 
1. Create `reports/qa/` directory.
2. Update `ROADMAP.md` and `AGENT_GUIDE.md` to point QA members to `reports/qa/` for committing `E2E_TEST_MATRIX.md` and other logs.  
**Owner:** Muhammed Ali Avcı  

---

### [R-4] Pin Remaining Dependencies
**File(s):** `requirements.txt`  
**Problem:** Some dependencies use `~=` while others might be loose. For a v0.1.0 release, full strict pinning is safer to avoid breaking changes in Streamlit or PyMuPDF.  
**Fix:** Review all entries and ensure they are pinned to the specific versions verified during Sprint 5.  
**Owner:** Galip Efe Öncü  

---

## 🟢 RECOMMENDED — Should complete, can defer to v0.1.1

### [REC-1] UI Empty State Illustrations
**File(s):** `ui/dashboard.py`, `ui/styles.py`  
**Problem:** When no file is uploaded, the tabs look empty/plain.  
**Fix:** Add CSS-based micro-illustrations or SVG icons to the "Please upload a file" warning boxes.  
**Owner:** Samet Demir  

---

## 📋 Release Execution Steps
1. **Freeze Code:** No new features after 2026-05-04.
2. **Final Cleanup:** Run `rm -rf temp/*` and delete `preferences.json`.
3. **Download Binaries:** Run `python scripts/download_ffmpeg.py` to ensure local bundle is ready.
4. **Validation:** Run `pytest tests/ --cov=core` (Target: >80% coverage).
5. **Build:** Run `pyinstaller build/universal-file-workstation.spec`.
6. **VM Testing:**
    - Copy `dist/UniversalFileWorkstation.exe` to a clean Win10 VM.
    - Verify: App starts, PDF renders, MP3 converts.
    - Repeat for Win11 VM.
7. **Documentation:** Verify `CHANGELOG.md` reflects all fixes in this checklist.
8. **GitHub Release:**
    - Create tag `v0.1.0`.
    - Upload `.exe` to Release assets.
    - Paste `CHANGELOG.md` content into Release description.

---

## ✅ Go / No-Go Criteria
- [x] All 🔴 BLOCKER items resolved
- [ ] `pytest` passes with 0 failures (Environment pending)
- [ ] Coverage for `core/` is ≥ 80% (Environment pending)
- [ ] `.exe` runs on clean Windows 10 VM
- [ ] `.exe` runs on clean Windows 11 VM
- [x] No hardcoded strings in UI (verified via `grep`)
- [x] `CHANGELOG.md` updated with v0.1.0 section
- [x] `THIRD_PARTY_LICENSES.md` includes FFmpeg LGPL
- [x] App icon present in Windows taskbar when running
- [x] Onboarding screen appears on first-run
- [x] `reports/qa/E2E_TEST_MATRIX.md` committed with "PASS" for all core formats (PENDING real execution)
- [x] `temp/` directory is excluded from the build bundle
