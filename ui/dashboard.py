"""
ui/dashboard.py — Kullanıcı Arayüzü Düzeni (Layout)
Sahibi: Samet Demir (Arayüz Tasarımcısı)
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from config.settings import Config
from core.viewer import FileViewer

# ---------------------------------------------------------------------------
# Dosya uzantısına göre desteklenen hedef formatlar
# ---------------------------------------------------------------------------
_FORMAT_MAP = {
    ".pdf":  ["docx"],
    ".docx": ["pdf", "txt"],
    ".csv":  ["xlsx"],
    ".xlsx": ["csv"],
    ".jpg":  ["png", "webp", "bmp"],
    ".jpeg": ["png", "webp", "bmp"],
    ".png":  ["jpg", "webp", "bmp"],
    ".webp": ["jpg", "png", "bmp"],
    ".bmp":  ["jpg", "png", "webp"],
    ".mp3":  ["wav", "ogg", "flac"],
    ".wav":  ["mp3", "ogg", "flac"],
    ".ogg":  ["mp3", "wav", "flac"],
    ".flac": ["mp3", "wav", "ogg"],
}

# ---------------------------------------------------------------------------
# Kategori tanımları — upload hero
# ---------------------------------------------------------------------------
_CATEGORIES = {
    "document": {
        "icon": "📄",
        "label_key": "cat_document",
        "formats_key": "cat_document_formats",
        "extensions": ["pdf", "docx", "doc", "txt", "rtf", "odt", "csv", "xlsx", "xls"],
    },
    "image": {
        "icon": "🖼️",
        "label_key": "cat_image",
        "formats_key": "cat_image_formats",
        "extensions": ["png", "jpg", "jpeg", "webp", "bmp"],
    },
    "audio": {
        "icon": "🎵",
        "label_key": "cat_audio",
        "formats_key": "cat_audio_formats",
        "extensions": ["mp3", "wav", "ogg", "flac", "m4a"],
    },
    "video": {
        "icon": "🎬",
        "label_key": "cat_video",
        "formats_key": "cat_video_formats",
        "extensions": ["mp4", "mov", "webm"],
    },
}

# Dosya ikonları
_EXT_ICONS = {
    ".pdf": "📕", ".docx": "📝", ".doc": "📝", ".txt": "📄",
    ".csv": "📊", ".xlsx": "📊", ".xls": "📊",
    ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".webp": "🖼️", ".bmp": "🖼️",
    ".mp3": "🎵", ".wav": "🎵", ".ogg": "🎵", ".flac": "🎵", ".m4a": "🎵",
    ".mp4": "🎬", ".mov": "🎬", ".webm": "🎬",
}

class Dashboard:
    """Uygulamanın genel sayfa düzenini kurgular."""

    def __init__(self, texts):
        """Dashboard'u başlat ve metin yapılandırmasını ayarla."""
        self.texts = texts

    def render_sidebar(self):
        """Sidebar: sadece logo, dosya geçmişi ve ayarlar butonu."""
        with st.sidebar:
            st.markdown(f"""
            <div style="font-size: 17px; font-weight: 700; color: var(--text-primary);
                        margin-bottom: 20px; letter-spacing: -0.3px;">
                {Config.APP_NAME}
            </div>
            """, unsafe_allow_html=True)
            st.divider()

            # --- Dosya Geçmişi ---
            st.markdown(f"**{self.texts.get('sidebar_history', 'File History')}**")
            if "file_history" not in st.session_state:
                st.session_state.file_history = []

            history = st.session_state.file_history
            if history:
                st.markdown(
                    f"<div style='font-size:12px;color:var(--text-secondary);margin-bottom:8px;'>"
                    f"{len(history)} {self.texts.get('history_files_count', 'files')}</div>",
                    unsafe_allow_html=True
                )
                for file_info in reversed(history[-5:]):
                    st.markdown(f"""
                    <div class="history-file-item">
                        {file_info['name']}<br>
                        <span class="history-file-item-time">{file_info['time']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='color:var(--text-secondary);font-size:12px;'>"
                    f"{self.texts.get('history_empty', 'No files uploaded yet')}</div>",
                    unsafe_allow_html=True
                )

            st.divider()
            if st.button(self.texts.get("sidebar_settings", "Settings"),
                         use_container_width=True, key="btn_sidebar_settings"):
                st.session_state.show_settings = not st.session_state.get("show_settings", False)
                st.rerun()
            st.caption(f"v{Config.VERSION}")

    def render_settings_page(self):
        """Geliştirilmiş ayarlar sayfası: iconlu başlıklar, theme kartları, quality badge."""
        c1, c2 = st.columns([0.9, 0.1])
        with c1:
            st.title(self.texts.get("settings_title", "Settings"))
        with c2:
            st.write("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("✕", key="close_settings",
                         help=self.texts.get("settings_close_btn", "Close"),
                         use_container_width=True):
                st.session_state.show_settings = False
                st.rerun()

        st.divider()
        col_main, _ = st.columns([0.8, 0.2])

        with col_main:

            # ── General ───────────────────────────────────────────────────────
            st.markdown(
                f"<div class='settings-section-header'>"
                f"<div class='settings-section-icon'>🌐</div>"
                f"<p class='settings-section-title'>{self.texts.get('settings_section_general', 'General')}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            cl, cr = st.columns([0.45, 0.55])
            with cl:
                st.markdown(f"<p class='settings-field-label'>{self.texts.get('settings_language_label', 'Language')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='settings-field-desc'>{self.texts.get('settings_language_desc', 'Change the application interface language.')}</p>", unsafe_allow_html=True)
            with cr:
                lang_display = {"tr": "Türkçe (TR)", "en": "English (EN)"}
                current_lang_name = lang_display.get(st.session_state.language, "English (EN)")
                selected_lang_name = st.selectbox(
                    "Language",
                    options=list(lang_display.values()),
                    index=list(lang_display.values()).index(current_lang_name),
                    label_visibility="collapsed",
                )
                for key, value in lang_display.items():
                    if value == selected_lang_name and st.session_state.language != key:
                        st.session_state.language = key
                        prefs = Config.load_user_prefs()
                        prefs["language"] = key
                        Config.save_user_prefs(prefs)
                        st.rerun()

            # ── Appearance ────────────────────────────────────────────────────
            st.markdown(
                f"<div class='settings-section-header'>"
                f"<div class='settings-section-icon'>🎨</div>"
                f"<p class='settings-section-title'>{self.texts.get('settings_section_appearance', 'Appearance')}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<p class='settings-field-label'>{self.texts.get('settings_theme_label', 'Theme')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='settings-field-desc'>{self.texts.get('settings_theme_desc', 'Choose between dark or light appearance.')}</p>", unsafe_allow_html=True)
            st.markdown("")
            current_theme = st.session_state.get("theme", "dark")
            st.markdown('<div class="theme-cards-row">', unsafe_allow_html=True)
            tc1, tc2, _, _ = st.columns(4)
            with tc1:
                if st.button(
                    f"🌙  {self.texts.get('settings_theme_dark', 'Dark')}",
                    key="btn_theme_dark",
                    use_container_width=True,
                    type="primary" if current_theme == "dark" else "secondary",
                ):
                    if current_theme != "dark":
                        Config.switch_theme("dark")
                        st.session_state.theme = "dark"
                        st.info(self.texts.get("theme_restart_notice", "Theme changed. Refresh to apply (F5)."))
            with tc2:
                if st.button(
                    f"☀️  {self.texts.get('settings_theme_light', 'Light')}",
                    key="btn_theme_light",
                    use_container_width=True,
                    type="primary" if current_theme == "light" else "secondary",
                ):
                    if current_theme != "light":
                        Config.switch_theme("light")
                        st.session_state.theme = "light"
                        st.info(self.texts.get("theme_restart_notice", "Theme changed. Refresh to apply (F5)."))
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Conversion ────────────────────────────────────────────────────
            st.markdown(
                f"<div class='settings-section-header'>"
                f"<div class='settings-section-icon'>⚙️</div>"
                f"<p class='settings-section-title'>{self.texts.get('settings_section_conversion', 'Conversion')}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<p class='settings-field-label'>{self.texts.get('settings_quality_label', 'Default Image Quality')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='settings-field-desc'>{self.texts.get('settings_quality_desc', 'Quality ratio used in image conversion operations.')}</p>", unsafe_allow_html=True)
            st.markdown("")
            if "default_quality" not in st.session_state:
                st.session_state.default_quality = 100
            st.slider("Quality", 1, 100, key="default_quality", label_visibility="collapsed")
            q = st.session_state.default_quality
            if q == 100:
                qlabel = self.texts.get("quality_lossless", "Lossless")
            elif q >= 71:
                qlabel = self.texts.get("quality_high", "High")
            elif q >= 31:
                qlabel = self.texts.get("quality_medium", "Medium")
            else:
                qlabel = self.texts.get("quality_low", "Low")
            st.markdown(
                f"<div class='quality-badge-row'>"
                f"<span class='quality-label-badge'>{qlabel} — {q}%</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # ── Data Management ───────────────────────────────────────────────
            st.markdown(
                f"<div class='settings-section-header'>"
                f"<div class='settings-section-icon'>🗄️</div>"
                f"<p class='settings-section-title'>{self.texts.get('settings_section_data', 'Data Management')}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            cl2, cr2 = st.columns([0.65, 0.35])
            with cl2:
                st.markdown(f"<p class='settings-field-label'>{self.texts.get('settings_history_label', 'File History')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='settings-field-desc'>{self.texts.get('settings_history_desc', 'Clear the list of uploaded files.')}</p>", unsafe_allow_html=True)
            with cr2:
                st.markdown("")
                if st.button(self.texts.get("settings_clear_btn", "Clear History"), use_container_width=True):
                    st.session_state.file_history = []
                    st.toast(self.texts.get("notify_success_default", "Success"))
                    st.rerun()

        st.write("")
        st.divider()
        st.caption(f"Universal File Workstation v{Config.VERSION} — {datetime.now().year}")

    def _render_empty_state(self, icon: str, title: str, subtitle: str):
        """Sekmeler için görselleştirilmiş boş durum (empty state) render eder."""
        st.markdown(f"""
        <div style="text-align:center;padding:60px 20px;border:1px dashed var(--border);
                    border-radius:var(--radius-xl);margin-top:24px;animation:fadeIn 0.2s ease;">
            <div style="font-size:2.5rem;margin-bottom:16px;">📂</div>
            <h3 style="color:var(--text-primary);margin-bottom:8px;font-weight:600;">{title}</h3>
            <p style="color:var(--text-secondary);font-size:0.875rem;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    def _add_to_file_history(self, filename):
        """Dosya geçmişine yeni dosya ekle."""
        if "file_history" not in st.session_state:
            st.session_state.file_history = []
        file_info = {
            "name": filename,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d.%m.%Y"),
        }
        st.session_state.file_history = [
            f for f in st.session_state.file_history
            if f["name"] != filename
        ]
        st.session_state.file_history.append(file_info)

    def _render_upload_hero(self):
        """Dosya yüklenmemişken merkezi hero upload alanı gösterir."""
        # Init category state
        if "selected_category" not in st.session_state:
            st.session_state.selected_category = None

        # Hero header
        st.markdown(f"""
        <div class="hero-wrapper">
            <h2 class="hero-title">{self.texts.get('upload_hero_title', 'Drop Your File Here')}</h2>
            <p class="hero-subtitle">{self.texts.get('upload_hero_subtitle', 'Convert, view and analyze any file with AI')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Category prompt
        st.markdown(
            f"<p class='category-prompt-label'>{self.texts.get('upload_choose_category', 'Choose a category')}</p>",
            unsafe_allow_html=True,
        )

        # Category cards (4 columns)
        st.markdown('<div class="category-btn-row">', unsafe_allow_html=True)
        cat_cols = st.columns(4)
        for i, (cat_id, cat) in enumerate(_CATEGORIES.items()):
            is_sel = st.session_state.selected_category == cat_id
            label = self.texts.get(cat["label_key"], cat_id.title())
            with cat_cols[i]:
                if st.button(
                    f"{cat['icon']}\n{label}",
                    key=f"btn_cat_{cat_id}",
                    use_container_width=True,
                    type="primary" if is_sel else "secondary",
                ):
                    st.session_state.selected_category = None if is_sel else cat_id
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Format pills for selected category
        sel_cat = st.session_state.selected_category
        if sel_cat and sel_cat in _CATEGORIES:
            pills_html = "".join(
                f'<span class="format-pill">.{ext.upper()}</span>'
                for ext in _CATEGORIES[sel_cat]["extensions"]
            )
            st.markdown(
                f'<div class="format-pills-container">{pills_html}</div>',
                unsafe_allow_html=True,
            )

        # Determine accepted types
        if sel_cat:
            accepted = _CATEGORIES[sel_cat]["extensions"]
        else:
            accepted = [e.lstrip(".") for e in Config.SUPPORTED_EXTENSIONS]

        # File uploader (main hero dropzone)
        st.markdown("")
        st.markdown('<div class="upload-dropzone-wrapper">', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            self.texts.get("upload_file", "Upload file"),
            type=accepted,
            label_visibility="collapsed",
            key="hero_uploader",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Limit badge (centered)
        st.markdown(
            f"<div style='text-align:center'>"
            f"<span class='upload-limit-badge'>🔒 {self.texts.get('upload_limit_badge', 'Max 200 MB per file')}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if uploaded:
            st.session_state.uploaded_file = uploaded
            self._add_to_file_history(uploaded.name)
            st.rerun()

    def _render_file_info_card(self, uploaded, tab_key: str = ""):
        """Yüklenen dosyanın bilgi kartını gösterir (isim, boyut, format, temizle butonu)."""
        ext = os.path.splitext(uploaded.name)[1].lower()
        icon = _EXT_ICONS.get(ext, "📁")
        size_bytes = len(uploaded.getvalue())
        if size_bytes >= 1_048_576:
            size_str = f"{size_bytes / 1_048_576:.1f} MB"
        else:
            size_str = f"{size_bytes / 1024:.0f} KB"

        col_card, col_clear = st.columns([0.85, 0.15])
        with col_card:
            st.markdown(f"""
            <div class="file-info-card">
                <div class="file-icon-wrap">{icon}</div>
                <div class="file-info-body">
                    <p class="file-info-name">{uploaded.name}</p>
                    <div class="file-meta-row">
                        <span class="file-badge">{ext.upper().lstrip('.')}</span>
                        <span class="file-size-badge">{size_str}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_clear:
            st.markdown("<div style='margin-top:14px'>", unsafe_allow_html=True)
            if st.button(
                f"✕ {self.texts.get('btn_clear_file', 'Clear')}",
                key=f"btn_clear_file_{tab_key}",
                use_container_width=True,
            ):
                st.session_state.uploaded_file = None
                st.session_state.selected_target_format = None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    def _render_format_grid(self, ext: str) -> str | None:
        """Hedef format gridini gösterir; seçili formatı döndürür."""
        if "selected_target_format" not in st.session_state:
            st.session_state.selected_target_format = None

        targets = _FORMAT_MAP.get(ext, [])
        if not targets:
            st.warning(self.texts.get("no_conversion_available", "No conversion available for this file type."))
            return None

        st.markdown(
            f"<p class='convert-target-label'>{self.texts.get('convert_target_title', 'Select Target Format')}</p>",
            unsafe_allow_html=True,
        )

        # Reset if current selection no longer valid
        if st.session_state.selected_target_format not in targets:
            st.session_state.selected_target_format = None

        n_cols = min(len(targets), 5)
        st.markdown('<div class="format-grid-row">', unsafe_allow_html=True)
        cols = st.columns(n_cols)
        for i, fmt in enumerate(targets):
            is_sel = st.session_state.selected_target_format == fmt
            with cols[i % n_cols]:
                if st.button(
                    f".{fmt.upper()}",
                    key=f"fmt_{fmt}",
                    use_container_width=True,
                    type="primary" if is_sel else "secondary",
                ):
                    st.session_state.selected_target_format = fmt
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return st.session_state.selected_target_format

    @staticmethod
    def notify_success(msg: str):
        """Merkezi başarı bildirim helper'ı."""
        st.toast(msg)
        st.success(msg)

    @staticmethod
    def notify_error(msg: str):
        """Merkezi hata bildirim helper'ı."""
        st.error(msg)

    def _save_upload_to_temp(self, uploaded_file):
        """Yüklenen dosyayı temp/ klasörüne yazar ve dosya yolunu döndürür."""
        os.makedirs("temp", exist_ok=True)
        path = os.path.join("temp", uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return path

    def _dispatch_conversion(self, input_path, source_ext, target_format, output_path):
        """Kaynak uzantı ve hedef formata göre doğru converter metodunu çağırır."""
        from core.converter import FileConverter
        from core.player import AudioConverter

        fc = FileConverter()
        source = source_ext.lower()
        target = target_format.lower()

        # Doküman dönüşümleri
        if source == ".pdf" and target == "docx":
            return fc.convert_pdf_to_docx(input_path, output_path)
        elif source == ".docx" and target == "pdf":
            return fc.convert_docx_to_pdf(input_path, output_path)
        elif source == ".docx" and target == "txt":
            return fc.convert_docx_to_txt(input_path, output_path)
        elif source == ".csv" and target == "xlsx":
            return fc.convert_csv_to_xlsx(input_path, output_path)
        elif source == ".xlsx" and target == "csv":
            return fc.convert_xlsx_to_csv(input_path, output_path)

        # Görsel dönüşümleri
        image_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        if source in image_exts and target in {"jpg", "jpeg", "png", "webp", "bmp"}:
            quality = st.session_state.get("default_quality", 100)
            return fc.convert_image(input_path, output_path, target, quality=quality)

        # Ses dönüşümleri
        audio_exts = {".mp3", ".wav", ".ogg", ".flac"}
        if source in audio_exts and target in {"mp3", "wav", "ogg", "flac"}:
            ac = AudioConverter()
            return ac.convert_audio(input_path, output_path, target)

        return False

    def _dispatch_viewer(self, uploaded_file) -> None:
        """Yüklenen dosyanın uzantısına göre uygun FileViewer.display_* metodunu çağırır."""
        import mimetypes
        ext = os.path.splitext(uploaded_file.name)[1].lower()

        # Uzantı → metod eşlemesi
        pdf_exts = {".pdf"}
        table_exts = {".csv", ".xls", ".xlsx"}
        audio_exts = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
        video_exts = {".mp4", ".mov", ".webm"}
        image_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
        text_exts = {
            ".txt", ".docx", ".doc", ".rtf", ".odt",
            ".py", ".js", ".html", ".css", ".java",
            ".cpp", ".sql", ".yaml", ".json", ".xml",
        }

        fv = FileViewer()
        file_path = self._save_upload_to_temp(uploaded_file)

        try:
            if ext in pdf_exts:
                with st.spinner(self.texts.get("loading_rendering", "Rendering...")):
                    fv.display_pdf(file_path, texts=self.texts)

            elif ext in table_exts:
                with st.spinner(self.texts.get("loading_rendering", "Rendering...")):
                    fv.display_table(file_path, texts=self.texts)

            elif ext in audio_exts:
                mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                audio_format = mime_type if mime_type else "audio/mp3"
                fv.display_audio(file_path, format=audio_format)

            elif ext in video_exts:
                mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                video_format = mime_type if mime_type else "video/mp4"
                fv.display_video(file_path, format=video_format)

            elif ext in image_exts:
                fv.display_image(file_path, texts=self.texts)

            elif ext in text_exts:
                with st.spinner(self.texts.get("loading_rendering", "Rendering...")):
                    fv.display_text_document(file_path, texts=self.texts)

            else:
                st.warning(
                    self.texts.get("error_unsupported_file", "Unsupported file type."),
                    icon="⚠️"
                )
        finally:
            Path(file_path).unlink(missing_ok=True)

    def render_main_area(self):
        """Ana içerik alanını kurgular: dosya yoksa hero upload, varsa tabs."""
        if not st.session_state.get("uploaded_file"):
            self._render_upload_hero()
            return

        uploaded = st.session_state.uploaded_file
        tab_names = [
            self.texts.get("convert_tab", "Convert"),
            self.texts.get("view_tab", "View"),
            self.texts.get("ai_tab", "AI Analysis"),
        ]
        tabs = st.tabs(tab_names)

        # ── Tab 0: Convert ────────────────────────────────────────────────────
        with tabs[0]:
            self._render_file_info_card(uploaded, tab_key="convert")

            ext = os.path.splitext(uploaded.name)[1].lower()
            selected_fmt = self._render_format_grid(ext)

            if selected_fmt:
                st.markdown("<div class='convert-action-bar'>", unsafe_allow_html=True)
                hint = self.texts.get("convert_select_format_hint", "Selected format")
                st.markdown(
                    f"<span class='selected-format-hint'>{hint}: "
                    f"<strong>.{selected_fmt.upper()}</strong></span>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

                if st.button(
                    self.texts.get("btn_convert", "Convert"),
                    type="primary",
                    key="btn_do_convert",
                ):
                    progress = st.progress(0, text=self.texts.get("loading_converting", "Converting..."))
                    input_path = self._save_upload_to_temp(uploaded)
                    progress.progress(30)
                    output_name = os.path.splitext(uploaded.name)[0] + f".{selected_fmt}"
                    output_path = os.path.join("temp", output_name)
                    success = self._dispatch_conversion(input_path, ext, selected_fmt, output_path)
                    progress.progress(90)
                    Path(input_path).unlink(missing_ok=True)

                    if success:
                        progress.progress(100, text="✅ Done!")
                        self.notify_success(self.texts.get("success_conversion", "Converted!"))
                        with open(output_path, "rb") as f:
                            output_data = f.read()
                        st.download_button(
                            self.texts.get("btn_download", "Download"),
                            data=output_data,
                            file_name=output_name,
                            type="primary",
                        )
                        Path(output_path).unlink(missing_ok=True)
                    else:
                        progress.empty()
                        self.notify_error(self.texts.get("error_unsupported_file", "Conversion failed."))
            else:
                st.markdown(
                    f"<p style='color:var(--text-muted);font-size:0.8rem;margin-top:16px;'>"
                    f"{self.texts.get('convert_select_format_hint', 'Select a format above to continue.')}</p>",
                    unsafe_allow_html=True,
                )

        with tabs[1]:
            self._render_file_info_card(uploaded, tab_key="view")
            self._dispatch_viewer(uploaded)

        # ── Tab 2: AI Analysis ────────────────────────────────────────────────
        with tabs[2]:
            self._render_file_info_card(uploaded, tab_key="ai")
            ext = os.path.splitext(uploaded.name)[1].lower()
            ai_supported_exts = {".pdf", ".docx", ".txt", ".csv", ".doc"}

            if ext not in ai_supported_exts:
                st.info(self.texts.get("ai_unsupported_file_type", "AI not supported."), icon="ℹ️")
            else:
                file_path = self._save_upload_to_temp(uploaded)
                try:
                    from core.ai_engine import AIEngine, PROVIDER_GROQ, PROVIDER_DEEPSEEK
                    from config.settings import Config as _Cfg

                    ai = AIEngine()

                    provider_label = self.texts.get("ai_provider_label", "AI Provider")
                    label_groq = self.texts.get("ai_provider_groq", "Groq (Llama 3.3 70B)")
                    label_ds   = self.texts.get("ai_provider_deepseek", "DeepSeek (DeepSeek-V3)")
                    lbl_ready  = self.texts.get("ai_provider_status_ready", "Ready")
                    lbl_na     = self.texts.get("ai_provider_status_unavailable", "API key missing")

                    provider_options = {
                        PROVIDER_GROQ:     f"{label_groq}  ✅ {lbl_ready}" if ai.is_groq_ready()     else f"{label_groq}  ⚠️ {lbl_na}",
                        PROVIDER_DEEPSEEK: f"{label_ds}  ✅ {lbl_ready}"  if ai.is_deepseek_ready() else f"{label_ds}  ⚠️ {lbl_na}",
                    }
                    provider_keys = list(provider_options.keys())
                    current_provider = st.session_state.get("ai_provider", _Cfg.AI_PROVIDER)
                    if current_provider not in provider_keys:
                        current_provider = provider_keys[0]

                    selected_provider = st.selectbox(
                        label=provider_label,
                        options=provider_keys,
                        index=provider_keys.index(current_provider),
                        format_func=lambda k: provider_options[k],
                        key="sel_ai_provider",
                    )
                    if selected_provider != st.session_state.get("ai_provider"):
                        st.session_state["ai_provider"] = selected_provider
                        st.rerun()
                    else:
                        st.session_state["ai_provider"] = selected_provider

                    st.divider()
                    fv = FileViewer()
                    with st.spinner(self.texts.get("loading_ai_processing", "Processing...")):
                        text_content = fv.extract_text(file_path)

                    if not text_content:
                        st.warning("No text found in document.")
                    else:
                        # ── AI Actions section wrapper (used for CSS scoping) ──
                        st.markdown("<div class='ai-action-section'>", unsafe_allow_html=True)

                        # Section label
                        st.markdown(
                            "<p style='font-size:0.7rem;font-weight:600;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:var(--text-muted);margin:20px 0 14px'>"
                            f"{self.texts.get('ai_actions', 'AI Actions')}</p>",
                            unsafe_allow_html=True,
                        )

                        # ── ROW 1: Summarize │ Keywords │ Simplify ──────────
                        ca, cb, cc = st.columns(3)

                        # — Summarize ————————————————————————————————————————
                        with ca:
                            st.markdown("<div class='ai-card-anchor'></div>", unsafe_allow_html=True)
                            with st.container(border=True, height=185):
                                st.markdown(
                                    "<p style='font-size:0.82rem;font-weight:700;"
                                    "color:var(--text-primary);margin:0 0 4px'>📝 "
                                    f"{self.texts.get('ai_summarize_btn','Summarize')}</p>"
                                    "<p style='font-size:0.72rem;color:var(--text-muted);margin:0 0 10px'>"
                                    f"{self.texts.get('ai_summarize_desc','Choose length and generate a concise summary.')}</p>",
                                    unsafe_allow_html=True,
                                )
                                sum_options = {
                                    "short":  self.texts.get("ai_summary_short",  "Short"),
                                    "medium": self.texts.get("ai_summary_medium", "Medium"),
                                    "long":   self.texts.get("ai_summary_long",   "Long"),
                                }
                                sum_length = st.radio(
                                    "sum_length",
                                    options=list(sum_options.keys()),
                                    format_func=lambda x: sum_options[x],
                                    horizontal=True,
                                    key="rad_sum",
                                    label_visibility="collapsed",
                                )
                                if st.button(
                                    self.texts.get("ai_summarize_btn", "Summarize"),
                                    key="btn_sum",
                                    use_container_width=True,
                                ):
                                    with st.spinner(self.texts.get("loading_ai_processing", "Processing…")):
                                        res = ai.summarize(text_content, length=sum_length)
                                        st.session_state["ai_result"] = ("Summarize", res)
                                        st.rerun()

                        # — Extract Keywords ——————————————————————————————————
                        with cb:
                            st.markdown("<div class='ai-card-anchor'></div>", unsafe_allow_html=True)
                            with st.container(border=True, height=185):
                                st.markdown(
                                    "<p style='font-size:0.82rem;font-weight:700;"
                                    "color:var(--text-primary);margin:0 0 4px'>🔑 "
                                    f"{self.texts.get('ai_keywords_btn','Extract Keywords')}</p>"
                                    "<p style='font-size:0.72rem;color:var(--text-muted);margin:0 0 10px'>"
                                    f"{self.texts.get('ai_keywords_desc','Identify and list the key terms and topics in the document.')}</p>",
                                    unsafe_allow_html=True,
                                )
                                if st.button(
                                    self.texts.get("ai_keywords_btn", "Extract Keywords"),
                                    key="btn_kw",
                                    use_container_width=True,
                                ):
                                    with st.spinner(self.texts.get("loading_ai_processing", "Processing…")):
                                        res = ai.extract_keywords(text_content)
                                        kw_text = "\n".join([f"- {k}" for k in res]) if res else "No keywords found."
                                        st.session_state["ai_result"] = ("Keywords", kw_text)
                                        st.rerun()

                        # — Simplify ——————————————————————————————————————————
                        with cc:
                            st.markdown("<div class='ai-card-anchor'></div>", unsafe_allow_html=True)
                            with st.container(border=True, height=185):
                                st.markdown(
                                    "<p style='font-size:0.82rem;font-weight:700;"
                                    "color:var(--text-primary);margin:0 0 4px'>✨ "
                                    f"{self.texts.get('ai_simplify_btn','Simplify')}</p>"
                                    "<p style='font-size:0.72rem;color:var(--text-muted);margin:0 0 10px'>"
                                    f"{self.texts.get('ai_simplify_desc','Rewrite the content at your desired complexity level.')}</p>",
                                    unsafe_allow_html=True,
                                )
                                simp_options = {
                                    "basic":        self.texts.get("ai_simplify_basic",        "Basic"),
                                    "intermediate": self.texts.get("ai_simplify_intermediate", "Intermediate"),
                                    "advanced":     self.texts.get("ai_simplify_advanced",     "Advanced"),
                                }
                                simp_level = st.radio(
                                    "simp_level",
                                    options=list(simp_options.keys()),
                                    format_func=lambda x: simp_options[x],
                                    horizontal=True,
                                    key="rad_simp",
                                    label_visibility="collapsed",
                                )
                                if st.button(
                                    self.texts.get("ai_simplify_btn", "Simplify"),
                                    key="btn_simp",
                                    use_container_width=True,
                                ):
                                    with st.spinner(self.texts.get("loading_ai_processing", "Processing…")):
                                        res = ai.simplify(text_content, level=simp_level)
                                        st.session_state["ai_result"] = ("Simplify", res)
                                        st.rerun()

                        # ── ROW 2: Ask Question (full width) ─────────────────
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                        with st.container(border=True):
                            st.markdown(
                                "<p style='font-size:0.82rem;font-weight:700;"
                                "color:var(--text-primary);margin:0 0 4px'>💬 "
                                f"{self.texts.get('ai_ask_btn','Ask Question')}</p>"
                                "<p style='font-size:0.72rem;color:var(--text-muted);margin:0 0 10px'>"
                                f"{self.texts.get('ai_ask_desc','Ask anything about the document and get a precise answer.')}</p>",
                                unsafe_allow_html=True,
                            )
                            question = st.text_area(
                                "question_area",
                                key="ai_q",
                                label_visibility="collapsed",
                                placeholder=self.texts.get("ai_question_placeholder", "Ask anything about the document…"),
                                height=90,
                            )
                            ask_col, _ = st.columns([0.2, 0.8])
                            with ask_col:
                                if st.button(
                                    self.texts.get("ai_ask_btn", "Ask"),
                                    key="btn_ask",
                                    use_container_width=True,
                                    type="primary",
                                ):
                                    if question.strip():
                                        with st.spinner(self.texts.get("loading_ai_processing", "Processing…")):
                                            res = ai.answer_question(text_content, question)
                                            st.session_state["ai_result"] = ("Answer", res)
                                            st.rerun()
                                    else:
                                        st.toast("⚠️ " + self.texts.get("ai_question_empty", "Please enter a question first."))

                        # ── Result panel ──────────────────────────────────────
                        if "ai_result" in st.session_state:
                            title, content = st.session_state["ai_result"]

                            st.markdown(
                                "<p style='font-size:0.7rem;font-weight:600;letter-spacing:0.1em;"
                                "text-transform:uppercase;color:var(--text-muted);margin:24px 0 10px'>"
                                f"Result — {title}</p>",
                                unsafe_allow_html=True,
                            )
                            with st.container(border=True):
                                st.markdown(content)

                            raw_col, _ = st.columns([0.28, 0.72])
                            with raw_col:
                                show_raw = st.toggle(
                                    "📋 " + self.texts.get("ai_copy_md_toggle", "Copy as Markdown"),
                                    key="toggle_raw_md",
                                )
                            if show_raw:
                                st.code(content, language="markdown")

                finally:
                    Path(file_path).unlink(missing_ok=True)

