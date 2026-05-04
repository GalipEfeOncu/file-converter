<div align="center">

# 🗂️ Universal File Workstation

### Convert. View. Analyze. — All in One Place.

A modern, AI-powered desktop application for seamless file conversion, in-app document viewing, and intelligent content analysis — built entirely in Python.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)]()

</div>

---

> 🤖 **For AI agents / contributors:** start with [`docs/AGENT_GUIDE.md`](docs/AGENT_GUIDE.md) — a single-file primer that lets you understand the entire project (architecture, module APIs, session state, i18n rules, conventions, known bugs) without opening any source file.

## 📖 What is Universal File Workstation?

**Universal File Workstation** is a cross-platform desktop application that eliminates the need to juggle multiple tools for everyday file tasks. It brings together **file format conversion**, **document & media viewing**, and **AI-powered content analysis** into a single, elegant Streamlit interface.

Whether you're a student converting lecture PDFs, a data analyst switching between CSV and Excel, or a professional who needs quick document summaries — this tool has you covered, **no cloud upload required**.

---

## ✨ Key Features

- 📄 **Document Conversion** — Convert between PDF, DOCX, TXT, CSV, and XLSX with a single click.
- 🖼️ **Image Format Conversion** — Transform images across PNG, JPG, and WEBP formats with adjustable quality settings.
- 🎵 **Audio Conversion** — Switch between MP3, WAV, and OGG audio formats powered by FFmpeg & pydub.
- 👁️ **Built-in File Viewer** — Render PDFs as images, display tabular data, and read text documents without leaving the app.
- 🤖 **AI-Powered Analysis** — Summarize documents and ask questions about their content using OpenAI or Groq APIs.
- 🌐 **Bilingual Interface** — Full Turkish 🇹🇷 and English 🇺🇸 language support, switchable at runtime.
- 🎨 **Custom Dark Theme** — A polished, dark-mode UI with custom CSS injection for a modern, professional look.
- 🧪 **Tested & Reliable** — Automated test suite with `pytest` covering i18n consistency, dependency hygiene, and core module integrity.

---

## 🏗️ Project Architecture

```
file-converter/
│
├── main.py                  # Application entry point & session state management
│
├── core/                    # Backend logic (no UI dependencies)
│   ├── converter.py         # File format conversion algorithms
│   ├── viewer.py            # PDF rendering, table & text reading
│   ├── player.py            # Audio format conversion (FFmpeg)
│   └── ai_engine.py         # AI summarization & Q&A (OpenAI / Groq)
│
├── ui/                      # Streamlit presentation layer
│   ├── dashboard.py         # Page layout, sidebar & navigation
│   └── styles.py            # CSS injection for custom theming
│
├── config/
│   └── settings.py          # App-wide configuration (name, language, layout)
│
├── assets/
│   └── languages.json       # i18n language strings (tr / en)
│
├── tests/                   # Automated test suite
│   ├── test_languages.py    # i18n key consistency tests
│   └── test_requirements.py # Dependency format & duplication tests
│
├── docs/                    # Project documentation
├── requirements.txt         # Python dependencies
└── LICENSE                  # MIT License
```

---

## 🚀 Installation

Follow these steps to get the project running locally.

### Prerequisites

| Requirement | Notes |
|---|---|
| **Python** | Version 3.10 or higher |
| **pip** | Comes bundled with Python |
| **FFmpeg** | Required for audio conversion (bundled on Windows, install on Linux/macOS) |
| **pandoc** | Required for RTF/ODT support — [install here](https://pandoc.org/installing.html) |

**Installing pandoc:**
- **Windows:** `choco install pandoc` or use the installer.
- **macOS:** `brew install pandoc`
- **Linux:** `sudo apt install pandoc`

### Step 1 — Clone the Repository

```bash
git clone https://github.com/GalipEfeOncu/file-converter.git
cd file-converter
```

### Step 2 — Create & Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure AI Module *(Optional)*

To enable AI-powered document analysis, create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
# OR
GROQ_API_KEY=your_gemini_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### Step 5 — Launch the Application

```bash
streamlit run main.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 💻 Usage

### Running the App

```bash
# Start the Streamlit application
streamlit run main.py
```

Once launched, use the **sidebar** to:
1. **Upload a file** — Supports PDF, DOCX, TXT, CSV, XLSX, PNG, JPG, WEBP, MP3, WAV, and OGG.
2. **Navigate tabs** — Switch between *Convert*, *View*, and *AI Analysis* modes.
3. **Switch language** — Toggle between English and Turkish from the sidebar dropdown.

### Running Tests

```bash
# Run the full test suite
python -m pytest tests -v

# Run a specific test module
python -m pytest tests/test_languages.py -v
```

### Supported Conversions

| Source | Target |
|---|---|
| PDF | DOCX, TXT |
| DOCX | PDF, TXT |
| CSV | XLSX |
| XLSX | CSV |
| PNG / JPG / WEBP | PNG / JPG / WEBP *(with quality control)* |
| MP3 / WAV / OGG | MP3 / WAV / OGG |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web-based application interface |
| `pandas` | CSV and Excel data processing |
| `openpyxl` | Excel (`.xlsx`) read/write support |
| `python-docx` | Word document parsing |
| `PyPDF2` | PDF text extraction |
| `PyMuPDF` | High-quality PDF → image rendering |
| `pdf2docx` | PDF → DOCX conversion |
| `Pillow` | Image processing & format conversion |
| `pydub` | Audio format conversion (requires FFmpeg) |
| `openai` | AI summarization and Q&A |
| `python-dotenv` | Secure API key management via `.env` |
| `pytest` | Automated testing framework |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can get involved:

1. **Fork** the repository.
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes with a clear message:
   ```bash
   git commit -m "feat: add your feature description"
   ```
4. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** against the `main` branch.

### Guidelines

- Follow the module ownership structure defined in [`docs/TASK_DISTRIBUTION.md`](docs/TASK_DISTRIBUTION.md).
- Write or update tests for any new functionality.
- Keep commit messages descriptive and follow [Conventional Commits](https://www.conventionalcommits.org/).
- Ensure `python -m pytest tests -v` passes before submitting.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by the Universal File Workstation team</sub>
</div>