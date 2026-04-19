# 📋 Product Requirements Document (PRD)
# Universal File Workstation

> **Version:** 1.1
> **Last Updated:** 2026-04-19
> **Status:** In Development (v0.1.0-alpha)
> **Repository:** [GalipEfeOncu/file-converter](https://github.com/GalipEfeOncu/file-converter)
> **Companion Doc:** See `docs/AGENT_GUIDE.md` for a model-friendly, code-free primer of the same scope.

---

## 1. Project Vision

**Universal File Workstation** is a cross-platform desktop application that unifies file conversion, document viewing, media playback, and AI-powered content analysis into a single, elegant interface — eliminating the need for multiple tools or cloud services.

The ultimate goal is to empower students, professionals, and power users with a local-first, privacy-respecting tool that handles any file format they encounter daily, while leveraging AI to extract meaningful insights from their documents.

---

## 2. Core Features (MVP)

> These are the **must-have** features required for the initial release. Each item reflects the actual implementation status in the codebase.

### 2.1 🏗️ Application Foundation & Architecture

- [x] Streamlit-based application shell (`main.py`) with page configuration and wide layout
- [x] Centralized configuration system (`config/settings.py`) with app name, version, supported extensions, and default language
- [x] Session state management for tracking uploaded files, active tab, and selected language
- [x] Secure API key management via `.env` file using `python-dotenv`
- [x] Modular project architecture separating backend logic (`core/`) from UI layer (`ui/`) and configuration (`config/`)

### 2.2 📄 Document Conversion Engine

- [x] **PDF → DOCX** conversion using `pdf2docx` library with start/end page control
- [x] **CSV → XLSX** conversion using `pandas` + `openpyxl` with empty-data validation
- [x] **XLSX → CSV** conversion using `pandas` with proper engine specification
- [x] **DOCX → TXT** extraction preserving paragraph structure (skips empty paragraphs)
- [x] **DOCX → PDF** conversion via `docx2pdf` (requires MS Word on the host system)
- [x] Consistent error handling (`try-except`) across all conversion functions with `FileNotFoundError` and generic exception coverage
- [x] Boolean return values (`True`/`False`) for all conversion methods to signal success/failure to the UI layer

### 2.3 🖼️ Image Conversion Engine

- [x] **PNG ↔ JPG ↔ WEBP** inter-format conversion using `Pillow (PIL)`
- [x] Automatic RGBA/P → RGB mode conversion for JPEG compatibility
- [x] Configurable output quality parameter (`quality: int`, default 100) for lossy formats

### 2.4 🎵 Audio Conversion Engine

- [x] Generic `convert_audio()` method supporting any-to-any audio format conversion via `pydub`
- [x] Dedicated **MP3 → OGG** and **OGG → MP3** shortcut methods
- [x] FFmpeg installation validation on startup (`shutil.which("ffmpeg")`) with warning if missing
- [x] Graceful failure handling: operations are blocked with a clear error message when FFmpeg is unavailable
- [x] `CouldntDecodeError` handling for corrupted or unsupported audio input files

### 2.5 👁️ File Viewing & Preview

- [x] **PDF Rendering**: Convert PDF pages to PNG images using `PyMuPDF (fitz)` (`FileViewer.render_pdf`)
- [x] **Table Data Viewer**: Read CSV and Excel (`.xls`, `.xlsx`) files into `pandas.DataFrame` (`FileViewer.read_table`)
- [x] **Format Validator**: Extension-based validation that rejects unsupported file types with a clear `ValueError`
- [x] **PDF Page Display**: `FileViewer.display_pdf` iterates pages and shows them sequentially via `st.image`
- [x] **Interactive Table Display**: `FileViewer.display_table` presents DataFrames via `st.dataframe`
- [x] **Media Player Integration**: `FileViewer.display_audio` / `display_video` embed `st.audio` and `st.video` widgets
- [x] **Text File Viewer**: `FileViewer.display_text_document` reads DOCX/TXT as UTF-8 and renders with `st.markdown` / `st.text_area`
- [ ] **Tab-level wiring**: The View tab in `Dashboard.render_main_area()` still shows a placeholder; it must dispatch to the appropriate `FileViewer.display_*` based on the uploaded file's extension

### 2.6 🌐 Internationalization (i18n)

- [x] Bilingual support: **Turkish** and **English** via `assets/languages.json`
- [x] Dynamic language switching through a sidebar `st.selectbox` with flag indicators (🇹🇷 / 🇺🇸)
- [x] Automatic page rerun (`st.rerun()`) on language change for seamless UX
- [x] All UI strings loaded dynamically from the JSON language file (no hardcoded text in components)

### 2.7 🎨 Design System & Theming

- [x] Custom CSS injection system via `st.markdown(unsafe_allow_html=True)` in `ui/styles.py`
- [x] Corporate color palette defined as CSS custom properties (`--brand-primary`, `--brand-secondary`, `--brand-accent`)
- [x] Dark theme implementation with gradient sidebar background
- [x] Google Fonts integration (`Inter` font family)
- [x] Styled interactive elements: buttons with gradient backgrounds, hover lift effects, and active press states
- [x] Custom scrollbar styling for a polished dark theme look
- [x] Hidden default Streamlit header menu and footer for a clean, app-like experience
- [x] Dashboard layout with `st.sidebar` and main content area properly structured (`ui/dashboard.py` — `Dashboard` class with `render_sidebar()` + `render_main_area()`)
- [x] Tab-based navigation using `st.tabs` for Convert, View, and AI sections (`render_main_area()` builds them from i18n keys)
- [ ] Move the hardcoded sidebar section labels and warning/info messages in `dashboard.py` to `assets/languages.json`

### 2.8 🧪 Quality Assurance & Testing

- [x] `pytest` configured as the official test runner
- [x] Language key consistency tests (`tests/test_languages.py`) validating TR/EN parity
- [x] Dependency format and duplication tests (`tests/test_requirements.py`)
- [ ] Smoke tests verifying core module imports and `main.py` startup
- [ ] Unit tests for DOCX → PDF and image (JPG/PNG/WEBP) conversion modules
- [ ] Large file (>50MB) stability testing

### 2.9 📂 File Upload & Session Management

- [x] File upload widget (`st.file_uploader`) supporting 30+ file extensions
- [x] Session-based file tracking: uploaded file persisted in `st.session_state.uploaded_file`
- [x] Success notification on file upload with filename display
- [x] Enhanced drag-and-drop upload area with custom CSS styling (gradient + dashed border in `ui/styles.py`)
- [x] File history panel in the sidebar (last 5 files, persisted via `st.session_state.file_history`, populated by `Dashboard._add_to_file_history`)

---

## 3. Future Enhancements (Backlog)

> Features planned for later versions, ordered by priority.

### 3.1 🤖 AI-Powered Document Analysis *(Priority: High)*

- [ ] Integrate Gemini API for document summarization (`ai_engine.py` — currently returns placeholder)
- [ ] Implement context-based Q&A: user asks questions about uploaded document content
- [ ] Keyword extraction from text-based files (PDF, DOCX, TXT)
- [ ] Automatic topic/heading generation for documents
- [ ] Text simplification at multiple levels (basic, intermediate, advanced)
- [ ] System prompt engineering for optimal AI response quality
- [ ] RAG (Retrieval-Augmented Generation) or direct context-feeding architecture decision

### 3.2 🖥️ Advanced Dashboard & Navigation *(Priority: High)*

- [x] Replace temporary `st.radio` sidebar with a modern `render_sidebar()` component
- [x] Implement `render_main_area()` with proper `st.tabs` integration
- [ ] Connect conversion tab to `core/converter.py` with button-triggered format conversion
- [ ] Connect viewing tab to `core/viewer.py` with live file preview (dispatch on file extension)
- [ ] Connect AI tab to `core/ai_engine.py` with interactive analysis interface
- [ ] State-driven button and status management for conversion workflows (progress, error toasts, download buttons)

### 3.3 📦 Desktop Packaging *(Priority: Medium)*

- [ ] Package the application as a standalone `.exe` using PyInstaller
- [ ] Bundle FFmpeg binary to remove the external dependency requirement
- [ ] Create an installer with app icon and Start Menu shortcut
- [ ] Cross-platform packaging for macOS (`.app`) and Linux (`.AppImage`)

### 3.4 🎨 UI/UX Polish *(Priority: Medium)*

- [ ] Light theme variant with toggle switch
- [ ] Responsive layout optimization for different screen sizes
- [ ] Loading spinners and progress bars for long-running conversions
- [ ] Animated transitions between tabs and views
- [ ] Custom file type icons in the upload area and file history panel

### 3.5 ⚙️ Advanced Conversion Features *(Priority: Low)*

- [ ] Batch file conversion (upload multiple files, convert all at once)
- [ ] PDF → PNG/JPG page-by-page image export
- [ ] Merge multiple PDFs into one
- [ ] Split a PDF into individual pages
- [ ] Audio trimming and basic editing before conversion
- [ ] Video format conversion (MP4 ↔ WEBM ↔ MOV)

### 3.6 📊 Analytics & User Experience *(Priority: Low)*

- [ ] Conversion statistics dashboard (total conversions, popular formats, file sizes)
- [ ] Recent files quick-access panel
- [ ] User preferences persistence across sessions (preferred output format, quality presets)
- [ ] Keyboard shortcuts for common actions

---

## 4. User Roles

> This application is designed for a single user role interacting locally. No authentication is required.

### 4.1 👤 End User (Primary)

| Attribute | Description |
|---|---|
| **Profile** | Students, office workers, researchers, and power users who work with diverse file formats daily |
| **Primary Goal** | Convert files between formats, preview documents in-app, and extract insights from text — all without leaving the application |
| **Key Actions** | Upload a file → Select target format → Convert → Download result |
|  | Upload a document → View/read it directly in the browser |
|  | Upload a text file → Ask AI to summarize, extract keywords, or answer questions |
|  | Switch between Turkish and English UI |
| **Technical Level** | Non-technical to intermediate; the tool must work without command-line interaction once launched |
| **Environment** | Windows desktop (primary), with macOS/Linux as secondary targets |

### 4.2 👨‍💻 Developer / Contributor

| Attribute | Description |
|---|---|
| **Profile** | The 5-person engineering team and future open-source contributors |
| **Primary Goal** | Extend the application with new conversion formats, improve UI components, or enhance AI capabilities |
| **Key Actions** | Clone repo → Set up virtual environment → Develop within assigned module → Run tests → Submit PR |
| **Constraints** | Must follow module ownership boundaries defined in `TASK_DISTRIBUTION.md`; changes to other modules require coordination with the module owner |

---

## 5. Success Criteria

> How we determine whether a feature is **successfully completed** and ready for release.

### 5.1 General Acceptance Criteria (All Features)

| # | Criterion | Verification Method |
|---|---|---|
| 1 | The feature works without runtime errors for all supported input formats | Manual testing with representative files + `pytest` unit test passes |
| 2 | Error cases (missing file, corrupted input, unsupported format) are handled gracefully with user-friendly messages — no unhandled exceptions | Negative testing with invalid inputs |
| 3 | All user-facing strings are available in both Turkish and English in `languages.json` | Automated key parity test (`tests/test_languages.py`) |
| 4 | The feature is visually consistent with the established design system (dark theme, Inter font, brand colors) | Visual inspection against the CSS design tokens in `ui/styles.py` |
| 5 | No new Python dependency is added without updating `requirements.txt` with a pinned compatible version (`~=`) | Automated dependency test (`tests/test_requirements.py`) |

### 5.2 Feature-Specific Criteria

| Feature | Success Condition |
|---|---|
| **File Conversion** | Input file is accepted → output file is generated in the target format → output file opens correctly in its native application (e.g., DOCX in Word, XLSX in Excel) → function returns `True` |
| **Image Conversion** | Format is correctly changed (verified by file header, not just extension) → quality parameter visibly affects output file size → RGBA images convert to JPG without errors |
| **Audio Conversion** | FFmpeg check runs on startup and warns if missing → conversion produces a playable audio file → unsupported/corrupted files return `False` with a logged error, not a crash |
| **File Viewing** | PDF renders at readable resolution → tables display with correct column headers and data types → text files are decoded as UTF-8 without mojibake |
| **AI Analysis** | API key is loaded securely from `.env` → summarization returns a coherent summary shorter than the input → Q&A returns relevant answers grounded in the document context → API failure is caught and shown as a user-friendly error |
| **i18n** | Switching language updates **all** visible text immediately → no leftover untranslated strings → language preference persists during the session |
| **Dashboard & Navigation** | All three tabs (Convert, View, AI) are accessible and functional → sidebar displays correctly → file upload works from any tab → navigation state is preserved on page rerun |
| **Desktop Packaging** | `.exe` launches without Python installed on the target machine → all features work identically to the development environment → file size is under 200MB |

---

## Appendix: Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **UI Framework** | Streamlit 1.44 |
| **Document Processing** | PyPDF2, pdf2docx, python-docx, PyMuPDF (fitz) |
| **Data Processing** | pandas, openpyxl |
| **Image Processing** | Pillow (PIL) |
| **Audio Processing** | pydub + FFmpeg |
| **AI Integration** | OpenAI / Google Gemini API |
| **Configuration** | python-dotenv |
| **Testing** | pytest |
| **Packaging** | PyInstaller *(planned)* |
