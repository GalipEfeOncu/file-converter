<div align="center">

# 🗂️ Universal File Workstation

**A modern, AI-powered desktop application for converting, reading, and managing files — built with Python.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)]()

</div>

---

## 📖 Overview

**Universal File Workstation** is a cross-platform desktop application that brings together file conversion, document viewing, media playback, and AI-powered document analysis into a single, elegant interface.

Built by a team of five engineers, this project targets students, professionals, and power users who frequently work with diverse file formats and need a single tool to handle them all — without relying on external cloud services.

---

## ✨ Features

| Category | Capability |
|---|---|
| 📄 **Document Conversion** | PDF → DOCX, CSV → Excel, and more |
| 👁️ **File Viewer** | Render PDFs as images, display Excel/CSV tables, read TXT & DOCX |
| 🎵 **Media Playback** | Play MP3, MP4, OGG, and WAV files |
| 🤖 **AI Analysis** | Summarize documents and answer questions via OpenAI / Gemini API |
| 🌐 **Internationalization** | Full Turkish & English UI support |
| 🎨 **Theming** | Dark mode with custom CSS injection, modern Streamlit interface |

---

## 🏗️ Project Architecture

```
file-converter/
│
├── main.py                  # Streamlit giriş noktası, session_state & sayfa yapılandırması
│
├── core/                    # Backend mantığı (UI bağımlılığı yok)
│   ├── ai_engine.py         # Yapay zeka özetleme & soru-cevap (OpenAI / Gemini)
│   ├── converter.py         # Dosya format dönüştürme algoritmaları
│   ├── viewer.py            # PDF render, tablo & metin okuma
│   └── player.py            # Ses format dönüştürme
│
├── ui/                      # Streamlit arayüz katmanı
│   ├── dashboard.py         # Ana sayfa düzeni (sidebar, modlar, sekmeler)
│   └── styles.py            # CSS enjeksiyonu ile özel tema
│
├── config/
│   └── settings.py          # Uygulama geneli yapılandırma (ad, dil, düzen)
│
├── assets/
│   ├── languages.json       # i18n dil stringleri (tr / en)
│   ├── icons/               # Uygulama ikonları
│   └── audio/               # Ses varlıkları
│
├── docs/                    # Proje dökümantasyonu
│   ├── PROJECT_DETAILS.md   # Proje detayları
│   ├── ROADMAP.md           # Yol haritası
│   └── TASK_DISTRIBUTION.md # Görev dağılımı
│
├── tests/
│   ├── test_converter.py    # Dönüştürme birim testleri
│   └── test_ai.py           # AI modül testleri
│
├── requirements.txt         # Python bağımlılıkları
└── LICENSE

```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10 or higher**
- **pip** package manager
- **ffmpeg** *(required for audio conversion via pydub — [download here](https://ffmpeg.org/download.html))*

### 1. Clone the Repository

```bash
git clone https://github.com/GalipEfeOncu/file-converter.git
cd file-converter
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the AI Module *(Optional)*

To enable AI-powered analysis, create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
# OR
GEMINI_API_KEY=your_gemini_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 5. Launch the Application

```bash
streamlit run main.py
```

> Your browser will automatically open at `http://localhost:8501`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web-based application interface |
| `Pillow` | Image processing (PNG, JPG, WEBP) |
| `pandas` | CSV and Excel data processing |
| `openpyxl` | Excel (`.xlsx`) file writing |
| `python-docx` | Word file reading/writing |
| `PyPDF2` | PDF text extraction |
| `PyMuPDF` | High-quality PDF → image rendering |
| `pydub` | Audio format conversion (requires ffmpeg) |
| `openai` | AI summarization and Q&A |
| `python-dotenv` | Secure API key management via `.env` |

---

## 👥 Team & Roles

This project is developed collaboratively. Each engineer owns a specific domain. See [`docs/TASK_DISTRIBUTION.md`](docs/TASK_DISTRIBUTION.md) for the full breakdown.

| Role | Module(s) |
|---|---|
| 🏛️ Project Architect & AI | `main.py`, `core/ai_engine.py`, `config/` |
| ⚙️ Logic & Algorithm Engineer | `core/converter.py`, `core/player.py` |
| 🎨 UI / UX Designer | `ui/dashboard.py`, `ui/styles.py` |
| 📄 File Viewer Specialist | `core/viewer.py` |
| 🧪 QA & Test Engineer | `tests/`, `assets/languages.json`, `requirements.txt` |

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run a specific test file
python -m pytest tests/test_converter.py -v
```

---

## 🌐 Internationalization

The application supports **English** and **Turkish** out of the box via `assets/languages.json`. The active language is set in `config/settings.py`:

```python
class Config:
    LANGUAGE = "en"  # Change to "tr" for Turkish
```

---

## 🗺️ Roadmap

- [x] Project architecture & module scaffolding
- [x] Configuration system & i18n skeleton
- [ ] File conversion engine (PDF, CSV, DOCX)
- [ ] PDF viewer with async page loading
- [ ] Media player integration
- [ ] AI document analysis module
- [ ] Full dark/light theme UI
- [ ] Packaging as standalone `.exe` (PyInstaller)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow the module ownership guidelines in [`docs/TASK_DISTRIBUTION.md`](docs/TASK_DISTRIBUTION.md) when making changes.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by the Universal File Workstation team</sub>
</div>