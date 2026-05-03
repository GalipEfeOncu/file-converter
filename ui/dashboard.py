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
    # Dokümanlar
    ".pdf": ["docx"],
    ".docx": ["pdf", "txt"],
    # Tablo ve Veri
    ".csv": ["xlsx"],
    ".xlsx": ["csv"],
    # Görseller
    ".jpg": ["png", "webp", "bmp"],
    ".jpeg": ["png", "webp", "bmp"],
    ".png": ["jpg", "webp", "bmp"],
    ".webp": ["jpg", "png", "bmp"],
    ".bmp": ["jpg", "png", "webp"],
    # Ses
    ".mp3": ["wav", "ogg", "flac"],
    ".wav": ["mp3", "ogg", "flac"],
    ".ogg": ["mp3", "wav", "flac"],
    ".flac": ["mp3", "wav", "ogg"],
}

class Dashboard:
    """Uygulamanın genel sayfa düzenini kurgular."""

    def __init__(self, texts):
        """Dashboard'u başlat ve metin yapılandırmasını ayarla."""
        self.texts = texts

    def render_sidebar(self):
        """
        Geliştirmiş sidebar oluştur.
        BUG 1 Fix: Removed empty column causing title misalignment.
        """
        with st.sidebar:
            # --- Logo/Brand Alanı (BUG 1 FIX) ---
            st.markdown(f"""
            <div style="font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 24px;">
                {Config.APP_NAME}
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            # --- Dosya Yükleme ---
            st.markdown(f"**{self.texts.get('sidebar_upload', 'File Upload')}**")
            supported = [ext.replace(".", "") for ext in Config.SUPPORTED_EXTENSIONS]
            
            uploaded_file = st.file_uploader(
                self.texts.get("upload_file", "Select File"),
                type=supported,
                label_visibility="collapsed"
            )

            if uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                # Dosya Geçmişine ekle
                self._add_to_file_history(uploaded_file.name)
                st.success(f"{self.texts.get('file_uploaded', 'Uploaded')}: {uploaded_file.name}")

            st.divider()

            # --- Dosya Geçmişi ---
            st.markdown(f"**{self.texts.get('sidebar_history', 'File History')}**")
            if "file_history" not in st.session_state:
                st.session_state.file_history = []

            history = st.session_state.file_history
            if history:
                st.markdown(f"<div style='font-size: 12px; color: var(--text-secondary);'>"
                            f"{len(history)} {self.texts.get('history_files_count', 'files')}</div>", unsafe_allow_html=True)
                for idx, file_info in enumerate(reversed(history[-5:])):
                    st.markdown(f"""
                    <div class="history-file-item">
                    {file_info['name']}<br>
                    <span class="history-file-item-time">{file_info['time']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: var(--text-secondary); font-size: 12px;'>"
                           f"{self.texts.get('history_empty', 'No files uploaded yet')}</div>", unsafe_allow_html=True)

            # --- Bottom Sidebar ---
            st.markdown("""<div style='flex-grow: 1;'></div>""", unsafe_allow_html=True)
            st.divider()
            
            if st.button(self.texts.get("sidebar_settings", "Settings"), use_container_width=True, key="btn_sidebar_settings"):
                st.session_state.show_settings = not st.session_state.get("show_settings", False)
                st.rerun()

            st.caption(f"v{Config.VERSION}")

    def render_settings_page(self):
        """Profesyonel ve temiz bir ayarlar sayfası render eder. BUG 3 Fix: Removed hardcoded strings."""
        # Header with Title and Close button
        c1, c2 = st.columns([0.9, 0.1])
        with c1:
            st.title(self.texts.get("settings_title", "Settings"))
        with c2:
            st.write("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("✕", key="close_settings", help=self.texts.get("settings_close_btn", "Close"), use_container_width=True):
                st.session_state.show_settings = False
                st.rerun()
        
        st.divider()

        # Settings Content
        col_main, _ = st.columns([0.8, 0.2])
        
        with col_main:
            # --- Genel Ayarlar ---
            st.markdown(f"<div class='settings-section'>", unsafe_allow_html=True)
            st.subheader(self.texts.get("settings_section_general", "General"))
            with st.container():
                st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([0.4, 0.6])
                with c1:
                    st.markdown(f"**{self.texts.get('settings_language_label', 'Language')}**")
                    st.caption(self.texts.get("settings_language_desc", "Change the application interface language."))
                with c2:
                    lang_display = {"tr": "Türkçe (TR)", "en": "English (EN)"}
                    current_lang_name = lang_display.get(st.session_state.language, "English (EN)")
                    selected_lang_name = st.selectbox(
                        "Language", 
                        options=list(lang_display.values()), 
                        index=list(lang_display.values()).index(current_lang_name),
                        label_visibility="collapsed"
                    )
                    
                    for key, value in lang_display.items():
                        if value == selected_lang_name and st.session_state.language != key:
                            st.session_state.language = key
                            prefs = Config.load_user_prefs()
                            prefs["language"] = key
                            Config.save_user_prefs(prefs)
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Görünüm ---
            st.markdown(f"<div class='settings-section'>", unsafe_allow_html=True)
            st.subheader(self.texts.get("settings_section_appearance", "Appearance"))
            with st.container():
                st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([0.4, 0.6])
                with c1:
                    st.markdown(f"**{self.texts.get('settings_theme_label', 'Theme')}**")
                    st.caption(self.texts.get("settings_theme_desc", "Choose between dark or light appearance."))
                with c2:
                    selected_theme = st.radio(
                        self.texts.get("settings_theme_label", "Theme"),
                        options=["dark", "light"],
                        format_func=lambda x: self.texts.get(f"settings_theme_{x}", x),
                        index=0 if st.session_state.get("theme", "dark") == "dark" else 1,
                        horizontal=True,
                        label_visibility="collapsed"
                    )

                    if selected_theme != st.session_state.get("theme", "dark"):
                        Config.switch_theme(selected_theme)
                        st.session_state.theme = selected_theme
                        st.info(self.texts.get("theme_restart_notice", 
                                "Theme changed. Please refresh the page (F5) to apply."))
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Dönüştürme Ayarları ---
            st.markdown(f"<div class='settings-section'>", unsafe_allow_html=True)
            st.subheader(self.texts.get("settings_section_conversion", "Conversion"))
            with st.container():
                st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([0.4, 0.6])
                with c1:
                    st.markdown(f"**{self.texts.get('settings_quality_label', 'Default Image Quality')}**")
                    st.caption(self.texts.get("settings_quality_desc", "Quality ratio used in image conversion operations."))
                with c2:
                    if "default_quality" not in st.session_state:
                        st.session_state.default_quality = 100
                    st.slider("Quality", 1, 100, key="default_quality", label_visibility="collapsed")
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Veri Yönetimi ---
            st.markdown(f"<div class='settings-section'>", unsafe_allow_html=True)
            st.subheader(self.texts.get("settings_section_data", "Data Management"))
            with st.container():
                st.markdown("<div class='settings-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([0.4, 0.6])
                with c1:
                    st.markdown(f"**{self.texts.get('settings_history_label', 'File History')}**")
                    st.caption(self.texts.get("settings_history_desc", "Clear the list of uploaded files."))
                with c2:
                    if st.button(self.texts.get("settings_clear_btn", "Clear History"), use_container_width=True):
                        st.session_state.file_history = []
                        st.toast(self.texts.get("notify_success_default", "Success"))
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.divider()
        st.caption(f"Universal File Workstation v{Config.VERSION} — {datetime.now().year}")

    def _render_empty_state(self, icon: str, title: str, subtitle: str):
        """Sekmeler için görselleştirilmiş boş durum (empty state) render eder."""
        st.markdown(f"""
        <div style="text-align: center; padding: 50px 20px; border: 2px dashed var(--border); border-radius: 20px; margin-top: 20px;">
            <h3 style="color: var(--text-primary); margin-bottom: 10px;">{title}</h3>
            <p style="color: var(--text-secondary); font-size: 14px;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("") # Spacer

    def _add_to_file_history(self, filename):
        """Dosya geçmişine yeni dosya ekle."""
        if "file_history" not in st.session_state:
            st.session_state.file_history = []
        
        file_info = {
            "name": filename,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d.%m.%Y")
        }
        
        # Aynı dosya zaten varsa, eski kaydını kaldır ve en üste ekle
        st.session_state.file_history = [
            f for f in st.session_state.file_history 
            if f["name"] != filename
        ]
        st.session_state.file_history.append(file_info)

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
        """Ana içerik alanını st.tabs ile kurgular."""
        # Sekmeleri oluştur
        tab_names = [
            self.texts.get('convert_tab', 'Convert'),
            self.texts.get('view_tab', 'View'),
            self.texts.get('ai_tab', 'AI Analysis')
        ]
        
        # Ana içerik alanını sınırla (Responsive max-width)
        col_main, _ = st.columns([0.8, 0.2])
        
        with col_main:
            tabs = st.tabs(tab_names)

        with tabs[0]:  # Dönüştür
            st.header(tab_names[0])
            if st.session_state.uploaded_file:
                uploaded = st.session_state.uploaded_file
                st.write(f"**{self.texts.get('selected_file', 'Selected File')}:** {uploaded.name}")

                ext = os.path.splitext(uploaded.name)[1].lower()
                targets = _FORMAT_MAP.get(ext, [])

                if targets:
                    target = st.selectbox(
                        self.texts.get("select_target_format", "Select target format"),
                        options=targets,
                        format_func=lambda x: f".{x.upper()}"
                    )

                    if st.button(self.texts.get("btn_convert", "Convert"), type="primary"):
                        with st.spinner(self.texts.get("loading_converting", "Converting...")):
                            input_path = self._save_upload_to_temp(uploaded)
                            output_name = os.path.splitext(uploaded.name)[0] + f".{target}"
                            output_path = os.path.join("temp", output_name)

                            success = self._dispatch_conversion(
                                input_path, ext, target, output_path
                            )

                            if success:
                                self.notify_success(self.texts.get("success_conversion", "Success!"))
                                with open(output_path, "rb") as f:
                                    output_data = f.read()
                                st.download_button(
                                    self.texts.get("btn_download", "Download"),
                                    data=output_data,
                                    file_name=output_name
                                )
                                Path(output_path).unlink(missing_ok=True)
                            else:
                                self.notify_error(self.texts.get("error_unsupported_file", "Failed."))

                            Path(input_path).unlink(missing_ok=True)
                else:
                    st.warning(self.texts.get("no_conversion_available", "No conversion available."))
            else:
                self._render_empty_state(
                    "", 
                    tab_names[0], 
                    self.texts.get("empty_state_convert", "Please upload a file.")
                )

        with tabs[1]:  # Görüntüle
            st.header(tab_names[1])
            if st.session_state.uploaded_file:
                uploaded = st.session_state.uploaded_file
                st.write(f"**{self.texts.get('selected_file', 'Selected File')}:** {uploaded.name}")
                self._dispatch_viewer(uploaded)
            else:
                self._render_empty_state(
                    "", 
                    tab_names[1], 
                    self.texts.get("empty_state_view", "Please upload a file.")
                )

        with tabs[2]:  # AI Analizi
            st.header(tab_names[2])
            if st.session_state.uploaded_file:
                uploaded = st.session_state.uploaded_file
                st.write(f"**{self.texts.get('selected_file', 'Selected File')}:** {uploaded.name}")

                ext = os.path.splitext(uploaded.name)[1].lower()
                ai_supported_exts = {".pdf", ".docx", ".txt", ".csv", ".doc"}

                if ext not in ai_supported_exts:
                    st.info(self.texts.get("ai_unsupported_file_type", "AI not supported."), icon="ℹ️")
                else:
                    file_path = self._save_upload_to_temp(uploaded)
                    try:
                        fv = FileViewer()
                        with st.spinner(self.texts.get("loading_ai_processing", "Processing...")):
                            text_content = fv.extract_text(file_path)

                        if not text_content:
                            st.warning("No text found.")
                        else:
                            from core.ai_engine import AIEngine
                            ai = AIEngine()

                            st.markdown(f"### {self.texts.get('ai_actions', 'AI Actions')}")
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                with st.container(border=True):
                                    st.subheader(self.texts.get("ai_summarize_btn", "Summarize"))
                                    
                                    sum_options = {
                                        "short": self.texts.get("ai_summary_short", "Short"),
                                        "medium": self.texts.get("ai_summary_medium", "Medium"),
                                        "long": self.texts.get("ai_summary_long", "Long")
                                    }
                                    
                                    sum_length = st.radio(
                                        self.texts.get("ai_summary_length", "Length"), 
                                        options=list(sum_options.keys()),
                                        format_func=lambda x: sum_options[x],
                                        horizontal=True, 
                                        key="rad_sum"
                                    )
                                    
                                    if st.button(self.texts.get("ai_summarize_btn", "Summarize"), key="btn_sum", use_container_width=True):
                                        with st.spinner(self.texts.get("loading_ai_processing", "Processing...")):
                                            res = ai.summarize(text_content, length=sum_length)
                                            st.session_state["ai_result"] = (self.texts.get("ai_summarize_btn", "Summarize"), res)
                                            
                                with st.container(border=True):
                                    st.subheader(self.texts.get("ai_keywords_btn", "Keywords"))
                                    if st.button(self.texts.get("ai_keywords_btn", "Keywords"), key="btn_kw", use_container_width=True):
                                        with st.spinner(self.texts.get("loading_ai_processing", "Processing...")):
                                            res = ai.extract_keywords(text_content)
                                            if not res:
                                                st.session_state["ai_result"] = (self.texts.get("ai_keywords_btn", "Keywords"), "No keywords.")
                                            else:
                                                st.session_state["ai_result"] = (self.texts.get("ai_keywords_btn", "Keywords"), "\n".join([f"- {k}" for k in res]))

                            with c2:
                                with st.container(border=True):
                                    st.subheader(self.texts.get("ai_ask_btn", "Ask"))
                                    question = st.text_input(self.texts.get("ai_question_label", "Question"), key="ai_q")
                                    if st.button(self.texts.get("ai_ask_btn", "Ask"), key="btn_ask", use_container_width=True):
                                        with st.spinner(self.texts.get("loading_ai_processing", "Processing...")):
                                            res = ai.answer_question(text_content, question)
                                            st.session_state["ai_result"] = (self.texts.get("ai_ask_btn", "Ask"), res)

                                with st.container(border=True):
                                    st.subheader(self.texts.get("ai_simplify_btn", "Simplify"))
                                    
                                    simp_options = {
                                        "basic": self.texts.get("ai_simplify_basic", "Basic"),
                                        "intermediate": self.texts.get("ai_simplify_intermediate", "Intermediate"),
                                        "advanced": self.texts.get("ai_simplify_advanced", "Advanced")
                                    }
                                    
                                    simp_level = st.radio(
                                        self.texts.get("ai_simplify_level", "Level"), 
                                        options=list(simp_options.keys()),
                                        format_func=lambda x: simp_options[x],
                                        horizontal=True, 
                                        key="rad_simp"
                                    )
                                    
                                    if st.button(self.texts.get("ai_simplify_btn", "Simplify"), key="btn_simp", use_container_width=True):
                                        with st.spinner(self.texts.get("loading_ai_processing", "Processing...")):
                                            res = ai.simplify(text_content, level=simp_level)
                                            st.session_state["ai_result"] = (self.texts.get("ai_simplify_btn", "Simplify"), res)
                                            
                            if "ai_result" in st.session_state:
                                title, content = st.session_state["ai_result"]
                                with st.expander(title, expanded=True):
                                    st.markdown(content)
                                    st.code(content, language="markdown")
                                    st.caption(self.texts.get("ai_copy_hint", "Copy hint."))

                    finally:
                        Path(file_path).unlink(missing_ok=True)
                        
            else:
                self._render_empty_state(
                    "", 
                    tab_names[2], 
                    self.texts.get("empty_state_ai", "Please upload a file.")
                )
