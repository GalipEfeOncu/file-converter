# Changelog

## [v0.1.0] - 2026-05-03

### Added
- Core architecture with Streamlit and i18n support.
- Conversion support for PDF, DOCX, CSV, XLSX, Image, and Audio formats.
- Interactive File Viewer with PDF pagination and Table filtering.
- AI Analysis tab powered by Gemini 1.5 Flash (Summarize, Keywords, Q&A).
- User preferences persistence (Theme, Language, Quality).
- Batch conversion logic (Internal API).
- FFmpeg bundling and validation.
- Onboarding screen for new users (Step-by-step introduction).
- App icons (PNG and ICO) for professional desktop presence.
- Empty state UI illustrations for better UX.
- Pandoc prerequisite documentation for RTF/ODT support.
- Formal QA reporting structure in `reports/qa/`.

### Fixed
- "Double class" bug in `player.py`.
- Temporary file cleanup logic in conversion flows.
- PDF rendering performance with Lazy Loading and caching.
- `batch_convert` crash when passing extra kwargs (fixed via signature filtering).
- PDF/Merge tests implemented with real fixtures.
- Dependency pinning for all packages in `requirements.txt`.

### Technical Debt
- Batch conversion UI integration pending.
- Architecture documentation formalized in `AGENT_GUIDE.md`.
