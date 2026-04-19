# 📋 CONTEXT.md — Source of Truth for AI Agents

> **Project:** Universal File Workstation
> **Version:** `0.1.0-alpha`
> **License:** MIT
> **Language:** Python 3.10+
> **Last Updated:** 2026-04-19

> 💡 **For low-capacity / fast coding models:** read `docs/AGENT_GUIDE.md` first — it is a single-file primer that lets a model contribute without reading the source code. This document is a deeper technical reference.

---

## 1. Tech Stack & Versions

| Category | Technology | Version | Purpose |
|:---|:---|:---|:---|
| **Runtime** | Python | 3.x | Core language |
| **UI Framework** | Streamlit | ~1.44.0 | Web-based GUI |
| **Document Processing** | python-docx | ~1.1.2 | DOCX read/write |
| | pdf2docx | ~0.5.8 | PDF → DOCX conversion |
| | PyMuPDF (fitz) | ~1.25.5 | PDF rendering to images |
| | PyPDF2 | ~3.0.1 | PDF utilities |
| | docx2pdf | *(bundled)* | DOCX → PDF (requires MS Word) |
| **Data Processing** | pandas | ~2.2.3 | CSV/Excel read & manipulation |
| | openpyxl | ~3.1.5 | Excel engine for pandas |
| **Image Processing** | Pillow (PIL) | ~11.2.1 | Image format conversion |
| **Audio Processing** | pydub | ~0.25.1 | Audio format conversion |
| | audioop-lts | ~0.2.1 | Audio operations support |
| **AI Integration** | openai | ~1.70.0 | LLM API client (planned: Gemini) |
| **Config** | python-dotenv | ~1.0.1 | `.env` file loading |
| **Testing** | pytest | ~8.3.5 | Test framework |
| **External Dependency** | FFmpeg | System-level | Required for audio conversions |

> [!IMPORTANT]
> All dependencies use the **compatible release operator** (`~=`) for version pinning.

---

## 2. Core Architecture

### 2.1 High-Level Structure

```
file-converter/
├── main.py                  # Entry point — Streamlit app orchestrator
├── config/
│   └── settings.py          # Centralized config (Config class)
├── core/                    # Business logic layer
│   ├── converter.py         # File format conversion algorithms
│   ├── player.py            # Audio conversion (FFmpeg-dependent)
│   ├── viewer.py            # File preview/rendering
│   └── ai_engine.py         # AI-powered analysis (stub)
├── ui/                      # Presentation layer
│   ├── styles.py            # CSS injection & design system
│   └── dashboard.py         # Dashboard layout (stub)
├── assets/
│   └── languages.json       # i18n string catalog (TR/EN)
├── tests/                   # Pytest test suite
│   ├── test_languages.py    # i18n validation tests
│   └── test_requirements.py # Dependency hygiene tests
├── test.py                  # Manual integration test (image + audio)
├── test_core.py             # Manual integration test (converter)
├── docs/                    # Project documentation
├── temp/                    # Runtime temporary files
├── .env                     # API keys (git-ignored)
└── requirements.txt         # Pinned dependencies
```

### 2.2 Design Patterns

| Pattern | Where | Description |
|:---|:---|:---|
| **Centralized Configuration** | `config/settings.py` → `Config` class | Single static class holds all app constants, supported extensions, API keys. Accessed globally via `Config.ATTR`. |
| **Modular Service Layer** | `core/*` | Each domain (conversion, viewing, audio, AI) is encapsulated in its own class within the `core/` package. |
| **CSS Injection** | `ui/styles.py` | Custom CSS injected via `st.markdown(unsafe_allow_html=True)` to override Streamlit defaults. Uses CSS custom properties (design tokens). |
| **i18n via JSON** | `assets/languages.json` | All UI strings are externalized. `main.py` loads them at runtime based on `st.session_state.language`. Keys must exist in both `tr` and `en`. |
| **Session State Management** | `main.py` → `init_state()` | Streamlit reruns the script on every interaction; persistent state is stored in `st.session_state` (language, active tab, uploaded file). |
| **Graceful Degradation** | `core/player.py` | FFmpeg availability is checked at init time via `shutil.which()`. Operations fail gracefully with `False` return + log if missing. |

### 2.3 Key Classes

| Class | Module | Responsibility |
|:---|:---|:---|
| `Config` | `config/settings.py` | App name, version, supported extensions, API keys |
| `FileConverter` | `core/converter.py` | PDF↔DOCX, CSV↔XLSX, image conversion, DOCX→TXT/PDF |
| `AudioConverter` | `core/player.py` | MP3↔OGG, generic audio conversion via pydub+FFmpeg |
| `FileViewer` | `core/viewer.py` | PDF page rendering (PyMuPDF), tabular data reading |
| `AIEngine` | `core/ai_engine.py` | Text summarization & Q&A (stub — TODO) |
| `Dashboard` | `ui/dashboard.py` | Sidebar (logo, language, navigation, uploader, file history, settings) & main area with `st.tabs` (Convert / View / AI) |

---

## 3. Coding Standards

### 3.1 Naming Conventions

| Element | Convention | Example |
|:---|:---|:---|
| Files & modules | `snake_case.py` | `ai_engine.py` |
| Classes | `PascalCase` | `FileConverter` |
| Functions & methods | `snake_case` | `convert_pdf_to_docx` |
| Constants | `UPPER_SNAKE_CASE` | `SUPPORTED_EXTENSIONS` |
| i18n keys | `snake_case` | `upload_file`, `file_uploaded` |
| i18n section markers | `__UPPER_SNAKE__` | `__NAV_SECTION__` |

### 3.2 Error Handling Rules

1. **Every conversion method** must be wrapped in `try/except` and return `bool` (`True` = success, `False` = failure).
2. **Specific exceptions first** (`FileNotFoundError`, `EmptyDataError`, `CouldntDecodeError`), then generic `Exception` as fallback.
3. **Logging, not crashing** — errors are logged via `logging.error()` / `logging.warning()`, never raised to the caller. The UI layer decides how to report to the user.
4. The `logging` module is configured at module level: `logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')`.

### 3.3 Folder Organization Rules

| Directory | Contents | Rule |
|:---|:---|:---|
| `core/` | Business logic only | No Streamlit imports allowed (current exception: `core/viewer.py` exposes optional `display_*` helpers that import `streamlit` — do not extend this pattern to other `core/` modules) |
| `ui/` | Presentation logic only | May import Streamlit; no file I/O |
| `config/` | App-wide constants & env loading | Static class, no business logic |
| `assets/` | Static data files (JSON, images) | No code files |
| `tests/` | Pytest test modules | Prefix with `test_` |
| `docs/` | Project documentation | Markdown only |
| `temp/` | Runtime scratch files | Git-ignored content |

### 3.4 i18n Rules

1. Every new UI string **must** be added to both `tr` and `en` blocks in `assets/languages.json`.
2. Keys must be `snake_case`.
3. Section markers (`__SECTION__`) are for human readability only — never referenced in code.
4. Tests in `tests/test_languages.py` enforce: both root keys exist, key sets are symmetric, required runtime keys are present.

### 3.5 Dependency Rules

- All packages in `requirements.txt` must use the `~=` (compatible release) operator.
- No duplicate entries allowed.
- Enforced by `tests/test_requirements.py`.

---

## 4. Critical Logic & Data Flow

### 4.1 Application Startup Flow

```
main.py → main()
  ├── st.set_page_config()          # Page title & layout
  ├── apply_custom_css()            # Inject design system (ui/styles.py)
  ├── init_state()                  # Initialize session_state defaults
  │     ├── language = "tr"
  │     ├── active_tab = "convert"
  │     ├── uploaded_file = None
  │     └── file_history = []
  ├── load_languages()              # Read assets/languages.json → dict (selected lang slice)
  └── Dashboard(texts)
        ├── render_sidebar()        # logo, language selectbox, navigation radio,
        │                           # file_uploader (writes to session_state.uploaded_file
        │                           # and appends to file_history), settings expander
        └── render_main_area()      # st.tabs(Convert, View, AI) — tab bodies are still
                                    # placeholders waiting for core/ wiring
```

### 4.2 File Conversion Flow

```
User uploads file via st.file_uploader
  → File stored in st.session_state.uploaded_file
  → User selects target format + clicks convert
  → main.py calls appropriate FileConverter / AudioConverter method
       ├── converter.convert_pdf_to_docx(input, output) → bool
       ├── converter.convert_csv_to_xlsx(input, output) → bool
       ├── converter.convert_image(input, output, fmt, quality) → bool
       └── player.convert_audio(input, output, fmt) → bool
  → Result: True/False
  → UI shows success/error message
```

### 4.3 Supported Conversion Matrix

| From | To | Module | Method |
|:---|:---|:---|:---|
| PDF | DOCX | `converter.py` | `convert_pdf_to_docx()` |
| CSV | XLSX | `converter.py` | `convert_csv_to_xlsx()` |
| XLSX | CSV | `converter.py` | `convert_xlsx_to_csv()` |
| PNG/JPG/WEBP/BMP | Any image format | `converter.py` | `convert_image()` |
| DOCX | TXT | `converter.py` | `convert_docx_to_txt()` |
| DOCX | PDF | `converter.py` | `convert_docx_to_pdf()` |
| MP3 | OGG | `player.py` | `convert_mp3_to_ogg()` |
| OGG | MP3 | `player.py` | `convert_ogg_to_mp3()` |
| Any audio | Any audio | `player.py` | `convert_audio()` |

### 4.4 File Viewing Flow

```
FileViewer.render_pdf(path)
  → PyMuPDF opens PDF → iterates pages
  → Each page → pixmap → PNG bytes
  → Returns list[bytes] for st.image display

FileViewer.read_table(path)
  → Detects extension (.csv / .xls / .xlsx)
  → Reads via pd.read_csv() or pd.read_excel()
  → Returns pd.DataFrame for st.dataframe display
  → Raises ValueError for unsupported formats
```

---

## 5. Environment Setup

### 5.1 Prerequisites

- **Python 3.x** (tested with 3.10+)
- **FFmpeg** — must be on system PATH for audio conversion features
- **Microsoft Word** — required on Windows for DOCX → PDF conversion (`docx2pdf`)

### 5.2 Installation

```bash
# Clone the repository
git clone https://github.com/GalipEfeOncu/file-converter.git
cd file-converter

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 5.3 Configuration

Create/edit `.env` in project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> The `.env` file is git-ignored. The key is loaded via `python-dotenv` in `config/settings.py`.

### 5.4 Running the Application

```bash
streamlit run main.py
```

### 5.5 Running Tests

```bash
# Run all pytest tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_languages.py
```

### 5.6 Manual Tests

```bash
# Image conversion + FFmpeg check
python test.py

# Core converter module test
python test_core.py
```

---

## 6. Known Issues & TODOs

| Area | Status | Detail |
|:---|:---|:---|
| `core/player.py` | ⚠️ Bug | Contains **duplicate class definitions** (`AudioConverter` defined twice) and **duplicate `__init__`** methods. Python keeps only the last one, but the file must be cleaned up. |
| `core/ai_engine.py` | 🔲 Stub | `summarize()` and `answer_question()` return placeholder strings. Gemini/OpenAI integration pending. |
| `requirements.txt` | ⚠️ Missing | `core/converter.py` imports `docx2pdf` but the package is not listed in `requirements.txt`. Add `docx2pdf~=<version>`. |
| `ui/dashboard.py` | 🌐 Hardcoded i18n | Sidebar section labels (`🌐 Dil / Language`, `📊 Navigasyon`, `📁 Dosya Yükleme`, `⏱️ Dosya Geçmişi`, `⚙️ Ayarlar`, etc.) and warning/info messages are hardcoded in Turkish. They should be moved to `assets/languages.json`. |
| Tab content (Convert / View / AI) | 🔌 Not wired | `Dashboard.render_main_area()` shows placeholder text ("Dönüştürme modülü yükleniyor...") and is not yet connected to `FileConverter`, `FileViewer`, or `AIEngine`. |
| `core/viewer.py` | 🏗️ Architecture | Imports `streamlit` to expose `display_pdf/table/audio/video/text_document` helpers — violates the "no Streamlit in core" rule. Tolerated for now; do not replicate elsewhere. |

---

## 7. Team & Ownership

| Member | Role | Modules Owned |
|:---|:---|:---|
| **Galip Efe Öncü** | Project Architect | `main.py`, `config/settings.py`, `core/ai_engine.py` |
| **Said Hamza Turan** | Logic & Algorithm Engineer | `core/converter.py`, `core/player.py` |
| **Abdulkadir Sar** | Viewer Developer | `core/viewer.py` |
| **Samet Demir** | UI/UX Designer | `ui/styles.py`, `ui/dashboard.py` |
| **Muhammed Ali Avcı** | QA & Testing | `tests/`, `assets/languages.json` |
