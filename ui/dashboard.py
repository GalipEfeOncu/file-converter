"""
ui/dashboard.py — Kullanıcı Arayüzü Düzeni (Layout)
Sahibi: Samet Demir (Arayüz Tasarımcısı)

Senin Görevin:
Streamlit'in tasarım bileşenlerini kullanarak modern, temiz ve kullanımı kolay bir dashboard tasarlamak. Sidebar, sekmeler ve dosya yükleme butonlarının yerleşimini yönetmek.

Çıktı: "Görsel olarak etkileyici ve fonksiyonel bir uygulama arayüzü iskeleti."
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from config.settings import Config

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
        Geliştirmiş sidebar oluştur: Dil seçimi, Dosya Geçmişi ve navigasyon.
        Samet Demir — Modern sidebar tasarımı, Dosya Geçmişi ve dil yönetimi.
        """
        with st.sidebar:
            # --- Logo/Brand Alanı ---
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                st.markdown("""
                <div style="font-size: 28px; font-weight: 700; 
                    background: linear-gradient(135deg, #0052CC, #00D6A7);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 10px;">
                    ⚡
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="font-size: 18px; font-weight: 700; color: rgba(242, 247, 255, 0.95);">
                    {Config.APP_NAME}
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # --- Dil Seçimi ---
            st.markdown(f"**{self.texts.get('sidebar_language', '🌐 Dil / Language')}**")
            lang_display = {"tr": "Türkçe 🇹🇷", "en": "English 🇺🇸"}
            current_index = 0 if st.session_state.language == "tr" else 1
            selected_lang_name = st.selectbox(
                "Dil seçin",
                options=list(lang_display.values()),
                index=current_index,
                label_visibility="collapsed"
            )

            for key, value in lang_display.items():
                if value == selected_lang_name:
                    if st.session_state.language != key:
                        st.session_state.language = key
                        st.rerun()

            st.divider()

            # --- Navigasyon ---
            st.markdown(f"**{self.texts.get('sidebar_navigation', '📊 Navigasyon')}**")
            nav_options = [
                self.texts.get("convert_tab", "Dönüştür"),
                self.texts.get("view_tab", "Görüntüle"),
                self.texts.get("ai_tab", "AI Analizi")
            ]

            if st.session_state.get("active_tab") not in nav_options:
                st.session_state.active_tab = nav_options[0]

            current_index = nav_options.index(st.session_state.active_tab)
            selected_tab = st.radio(
                "Sekme seçin",
                nav_options,
                index=current_index,
                label_visibility="collapsed"
            )

            if selected_tab != st.session_state.active_tab:
                st.session_state.active_tab = selected_tab

            st.divider()

            # --- Dosya Yükleme ---
            st.markdown(f"**{self.texts.get('sidebar_upload', '📁 Dosya Yükleme')}**")
            supported = [ext.replace(".", "") for ext in Config.SUPPORTED_EXTENSIONS]
            
            uploaded_file = st.file_uploader(
                self.texts.get("upload_file", "Dosya Seç"),
                type=supported,
                label_visibility="collapsed"
            )

            if uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                # Dosya Geçmişine ekle
                self._add_to_file_history(uploaded_file.name)
                st.success(f"{self.texts.get('file_uploaded', 'Yüklendi')}: {uploaded_file.name}")

            st.divider()

            # --- Dosya Geçmişi ---
            st.markdown(f"**{self.texts.get('sidebar_history', '⏱️ Dosya Geçmişi')}**")
            if "file_history" not in st.session_state:
                st.session_state.file_history = []

            history = st.session_state.file_history
            if history:
                st.markdown(f"<div style='font-size: 12px; color: rgba(242, 247, 255, 0.6);'>"
                            f"{len(history)} {self.texts.get('history_files_count', 'dosya')}</div>", unsafe_allow_html=True)
                for idx, file_info in enumerate(reversed(history[-5:])):  # Son 5 dosyayı göster
                    st.markdown(f"""
                    <div style='
                        padding: 8px 10px;
                        margin: 4px 0;
                        background: rgba(255, 255, 255, 0.04);
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 8px;
                        font-size: 11px;
                        color: rgba(242, 247, 255, 0.7);
                        cursor: pointer;
                        transition: all 150ms ease;
                    '>
                    📄 {file_info['name']}<br>
                    <span style='color: rgba(242, 247, 255, 0.5);'>{file_info['time']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: rgba(242, 247, 255, 0.4); font-size: 12px;'>"
                           f"{self.texts.get('history_empty', 'Henüz dosya yüklenmedi')}</div>", unsafe_allow_html=True)

            st.divider()

            # --- Ayarlar ---
            with st.expander(self.texts.get("sidebar_settings", "⚙️ Ayarlar")):
                st.markdown(f"**{self.texts.get('settings_theme', 'Tema')}**")
                st.selectbox(
                    "Tema seçin", 
                    [self.texts.get("settings_theme_dark", "Koyu"), self.texts.get("settings_theme_light", "Açık")], 
                    disabled=True, 
                    label_visibility="collapsed",
                    help=self.texts.get("settings_theme_tooltip", "Açık tema Sprint 5'te gelecek")
                )
                
                st.markdown(f"**{self.texts.get('settings_default_quality', 'Varsayılan Görsel Kalitesi')}**")
                if "default_quality" not in st.session_state:
                    st.session_state.default_quality = 100
                st.slider(
                    "Kalite", 
                    min_value=1, 
                    max_value=100, 
                    key="default_quality",
                    label_visibility="collapsed"
                )

                if st.session_state.get("file_history"):
                    if st.button(self.texts.get("settings_clear_history", "Geçmişi Temizle")):
                        st.session_state.file_history = []
                        st.rerun()

                st.markdown(f"**{self.texts.get('settings_about', 'Hakkında')}**")
                st.markdown(f"v{Config.VERSION}")

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

    # ------------------------------------------------------------------
    # Converter yardımcı metotları
    # ------------------------------------------------------------------
    @staticmethod
    def _save_upload_to_temp(uploaded_file):
        """Yüklenen dosyayı temp/ klasörüne yazar ve dosya yolunu döndürür."""
        os.makedirs("temp", exist_ok=True)
        path = os.path.join("temp", uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return path

    @staticmethod
    def _dispatch_conversion(input_path, source_ext, target_format, output_path):
        """Kaynak uzantı ve hedef formata göre doğru converter metodunu çağırır.

        Returns:
            bool: Dönüşüm başarılıysa True, değilse False.
        """
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

    def render_main_area(self):
        """
        Ana içerik alanını st.tabs ile kurgular.
        Samet Demir — Modern tab sistemi (Dönüştür, Görüntüle, AI) entegrasyonu.
        """
        active_tab = st.session_state.get("active_tab", self.texts.get("home_tab", "Ana Sayfa"))
        
        # Sekmeleri oluştur
        tab_names = [
            self.texts.get("convert_tab", "Dönüştür"),
            self.texts.get("view_tab", "Görüntüle"),
            self.texts.get("ai_tab", "AI Analizi")
        ]
        
        # Active tabnın indeksini bul
        default_index = 0
        try:
            default_index = tab_names.index(active_tab)
        except ValueError:
            pass

        tabs = st.tabs(tab_names)

        with tabs[0]:  # Dönüştür
            st.header(f"🔄 {tab_names[0]}")
            if st.session_state.uploaded_file:
                uploaded = st.session_state.uploaded_file
                st.write(f"📄 **{self.texts.get('selected_file', 'Seçili Dosya')}:** {uploaded.name}")

                ext = os.path.splitext(uploaded.name)[1].lower()
                targets = _FORMAT_MAP.get(ext, [])

                if targets:
                    target = st.selectbox(
                        self.texts.get("select_target_format", "Hedef format seçin"),
                        options=targets,
                        format_func=lambda x: f".{x.upper()}"
                    )

                    if st.button(self.texts.get("btn_convert", "Dönüştür"), type="primary"):
                        with st.spinner(self.texts.get("converting_in_progress", "Dönüştürülüyor...")):
                            input_path = self._save_upload_to_temp(uploaded)
                            output_name = os.path.splitext(uploaded.name)[0] + f".{target}"
                            output_path = os.path.join("temp", output_name)

                            success = self._dispatch_conversion(
                                input_path, ext, target, output_path
                            )

                            if success:
                                st.success(self.texts.get("success_conversion", "Başarılı!"))
                                with open(output_path, "rb") as f:
                                    output_data = f.read()
                                st.download_button(
                                    self.texts.get("btn_download", "İndir"),
                                    data=output_data,
                                    file_name=output_name
                                )
                                # Geçici çıktı dosyasını temizle
                                Path(output_path).unlink(missing_ok=True)
                            else:
                                st.error(self.texts.get("error_unsupported_file", "Dönüştürme başarısız."))

                            # Geçici girdi dosyasını temizle
                            Path(input_path).unlink(missing_ok=True)
                else:
                    st.warning(self.texts.get("no_conversion_available", "Bu dosya türü için dönüştürme desteği bulunmuyor."))
            else:
                st.warning(self.texts.get("no_file_uploaded", "Lütfen önce yan menüden bir dosya yükleyin."), icon="⚠️")

        with tabs[1]:  # Görüntüle
            st.header(f"👁️ {tab_names[1]}")
            if st.session_state.uploaded_file:
                st.write(f"📄 **{self.texts.get('selected_file', 'Seçili Dosya')}:** {st.session_state.uploaded_file.name}")
                st.info(self.texts.get("status_architecture_in_progress", "Görüntüleme modülü yükleniyor..."), icon="ℹ️")
            else:
                st.info(self.texts.get("no_file_uploaded", "Lütfen önce yan menüden bir dosya yükleyin."), icon="ℹ️")

        with tabs[2]:  # AI Analizi
            st.header(f"🤖 {tab_names[2]}")
            if st.session_state.uploaded_file:
                st.write(f"📄 **{self.texts.get('selected_file', 'Seçili Dosya')}:** {st.session_state.uploaded_file.name}")
                st.info(self.texts.get("status_architecture_in_progress", "AI analiz modülü yükleniyor..."), icon="ℹ️")
            else:
                st.info(self.texts.get("no_file_uploaded", "Lütfen önce yan menüden bir dosya yükleyin."), icon="ℹ️")
