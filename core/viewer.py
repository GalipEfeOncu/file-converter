"""
core/viewer.py — Dosya Görüntüleme ve Önizleme Modülü
Sahibi: Abdulkadir Sar (Görüntüleme Uzmanı)

Görev:
    - PDF sayfalarını PNG olarak render eder (PyMuPDF/fitz).
    - CSV/Excel tablolarını pandas DataFrame olarak okur.
    - Ses, video, metin ve görsel dosyaları için Streamlit display yardımcıları sağlar.
    - render_pdf ve read_table sonuçları st.cache_data ile cache'lenir (Issue #29).
    - extract_text: PDF/DOCX/TXT'den ham metin çıkarır (Issue #18 AI sekmesi için).

Mimari Not:
    Bu modül streamlit import eder (legacy istisna — AGENT_GUIDE.md §2.4).
    core/ içindeki yeni modüller streamlit import etmemeli.
"""

import logging
import mimetypes
import os

import fitz
import pandas as pd
import streamlit as st
import docx  # python-docx

# ---------------------------------------------------------------------------
# Modül seviyesi cache'li özel yardımcılar
# st.cache_data self metodlarına uygulanamadığından modül seviyesinde tanımlandı.
# ---------------------------------------------------------------------------


@st.cache_data(ttl=3600)
def _cached_render_pdf(pdf_path: str) -> list[bytes]:
    """Cache'li PDF render yardımcısı — her sayfa için PNG byte listesi döner."""
    logging.debug("Cache MISS: PDF render başlatılıyor — %s", pdf_path)
    doc = fitz.open(pdf_path)
    resim_listesi: list[bytes] = []
    for sayfa_numarasi in range(len(doc)):
        sayfa = doc.load_page(sayfa_numarasi)
        resim_verisi = sayfa.get_pixmap()
        png_formati = resim_verisi.tobytes("png")
        resim_listesi.append(png_formati)
    logging.debug("Cache'e yazıldı: %d sayfa — %s", len(resim_listesi), pdf_path)
    return resim_listesi


@st.cache_data(ttl=3600)
def _cached_read_table(file_path: str) -> pd.DataFrame:
    """Cache'li tablo okuyucu — CSV/XLSX için DataFrame döner, aksi halde ValueError."""
    logging.debug("Cache MISS: Tablo okunuyor — %s", file_path)
    _, uzanti = os.path.splitext(file_path)
    uzanti = uzanti.lower()
    if uzanti == ".csv":
        df = pd.read_csv(file_path)
    elif uzanti in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Desteklenmeyen dosya formatı! Lütfen .csv veya .xlsx yükleyin.")
    logging.debug("Cache'e yazıldı: %d×%d tablo — %s", len(df), len(df.columns), file_path)
    return df


# ---------------------------------------------------------------------------
# FileViewer sınıfı
# ---------------------------------------------------------------------------


class FileViewer:
    """Dosyaları önizleme için uygun formata dönüştürür ve arayüzde gösterir."""

    # -----------------------------------------------------------------------
    # Saf veri metotları (UI bağımsız)
    # -----------------------------------------------------------------------

    def render_pdf(self, pdf_path: str, start: int = 0, end: int | None = None) -> list[bytes]:
        """PDF sayfalarini gorsel olarak render eder.

        Args:
            pdf_path: Render edilecek PDF dosyasinin yolu.
            start: Baslangic sayfa indeksi (dahil, 0-tabanli). Varsayilan: 0.
            end: Bitis sayfa indeksi (haric, None ise son sayfa). Varsayilan: None.

        Returns:
            Her sayfa icin PNG byte dizisi iceren liste.

        Cache mekanizması _cached_render_pdf üzerinden çalışır (tam sayfa çağrılarında).
        """
        doc = fitz.open(pdf_path)
        toplam_sayfa = len(doc)
        bitis = end if end is not None else toplam_sayfa
        # Sinir kontrolu
        bitis = min(bitis, toplam_sayfa)
        baslangic = max(0, start)

        resim_listesi = []
        for sayfa_numarasi in range(baslangic, bitis):
            sayfa = doc.load_page(sayfa_numarasi)
            resim_verisi = sayfa.get_pixmap()
            png_formati = resim_verisi.tobytes("png")
            resim_listesi.append(png_formati)

        return resim_listesi

    def read_table(self, file_path: str) -> pd.DataFrame:
        """CSV veya Excel dosyalarını DataFrame olarak okur.

        Cache mekanizması _cached_read_table üzerinden çalışır.
        Desteklenmeyen uzantı veya okuma hatası durumunda ValueError fırlatır.
        """
        try:
            logging.debug("read_table çağrıldı: %s", file_path)
            return _cached_read_table(file_path)
        except Exception as e:
            raise ValueError(f"Dosya okunurken bir hata oluştu: {e}") from e

    def extract_text(self, file_path: str) -> str:
        """Metin tabanlı dosyalardan ham metin çıkarır.

        Desteklenen formatlar: .pdf, .docx, .txt, .csv
        AI sekmesi (Issue #18) tarafından kullanılmak üzere tasarlandı.

        Returns:
            str: Dosyadaki metin içeriği. Hata durumunda boş string döner.
        """
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()
        metin = ""

        try:
            if uzanti == '.pdf':
                doc = fitz.open(file_path)
                for page in doc:
                    metin += page.get_text() + "\n"
            elif uzanti in ['.docx', '.doc']:
                doc = docx.Document(file_path)
                metin = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            elif uzanti in ['.txt', '.csv']:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    metin = f.read()
            else:
                logging.warning(f"Desteklenmeyen dosya türü, metin çıkarılamadı: {uzanti}")
        except Exception as e:
            logging.error(f"Metin çıkarılırken hata oluştu ({file_path}): {e}")

        return metin.strip()

    # -----------------------------------------------------------------------
    # Streamlit display yardımcıları
    # -----------------------------------------------------------------------

    def display_pdf(self, pdf_path: str, texts: dict | None = None) -> None:
        """PDF sayfalarini Streamlit arayuzunde sayfa sayfa (lazy) gosterir.

        Pagination: st.session_state['pdf_current_page'] ile sayfa takibi yapilir.
        Her seferinde yalnizca tek bir sayfa render edilir — buyuk PDF'lerde performans icin.

        Args:
            pdf_path: Gosterilecek PDF dosyasinin yolu.
            texts: i18n sozlugu (opsiyonel). Fallback Turkce string'ler mevcuttur.
        """
        if texts is None:
            texts = {}

        try:
            doc = fitz.open(pdf_path)
            toplam_sayfa = len(doc)
        except Exception as e:
            logging.error(f"Hata: PDF acilamadi ({pdf_path}): {e}")
            st.error(f"PDF acilamadi: {e}")
            return

        if toplam_sayfa == 0:
            st.warning("PDF bos gorunuyor.")
            return

        # --- Session state ile sayfa indeksini yonet ---
        if "pdf_current_page" not in st.session_state:
            st.session_state["pdf_current_page"] = 0

        # Dosya degistiginde sayfayi sifirla
        pdf_key = f"pdf_key_{pdf_path}"
        if st.session_state.get("_pdf_last_path") != pdf_path:
            st.session_state["pdf_current_page"] = 0
            st.session_state["_pdf_last_path"] = pdf_path

        current = st.session_state["pdf_current_page"]
        pdf_page_of = texts.get("pdf_page_of", "/ toplam sayfa")

        # --- Sayfa numarasi input + bilgi satiri ---
        col_info, col_nav = st.columns([3, 2])
        with col_info:
            sayfa_no = st.number_input(
                f"Sayfa ({pdf_page_of} {toplam_sayfa})",
                min_value=1,
                max_value=toplam_sayfa,
                value=current + 1,
                step=1,
                key="pdf_page_input",
            )
            current = sayfa_no - 1
            st.session_state["pdf_current_page"] = current

        with col_nav:
            st.write("")
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("◀ Onceki", key="pdf_prev", disabled=(current == 0)):
                    st.session_state["pdf_current_page"] = max(0, current - 1)
                    st.rerun()
            with nav_col2:
                if st.button("Sonraki ▶", key="pdf_next", disabled=(current >= toplam_sayfa - 1)):
                    st.session_state["pdf_current_page"] = min(toplam_sayfa - 1, current + 1)
                    st.rerun()

        # --- Yalnizca aktif sayfayi render et (lazy) ---
        resimler = self.render_pdf(pdf_path, start=current, end=current + 1)
        if resimler:
            st.image(resimler[0], caption=f"Sayfa {current + 1} / {toplam_sayfa}", use_container_width=True)
            logging.info(f"Basarili: PDF sayfa {current + 1}/{toplam_sayfa} gosterildi ({pdf_path})")

    def display_table(self, file_path: str, texts: dict | None = None) -> None:
        """Tablo verilerini arama/filtreleme ve metadata destegi ile Streamlit arayuzunde gosterir.

        Args:
            file_path: Gosterilecek CSV veya Excel dosyasinin yolu.
            texts: i18n sozlugu (opsiyonel). Fallback Turkce string'ler mevcuttur.
        """
        if texts is None:
            texts = {}

        try:
            df = self.read_table(file_path)

            # --- Metadata özet satırı (Issue #29) ---
            dtype_counts: dict[str, int] = {}
            for dtype in df.dtypes:
                kind = dtype.kind  # 'i'=int, 'f'=float, 'O'=object/str, 'b'=bool, vb.
                if kind == "i":
                    label = "int"
                elif kind == "f":
                    label = "float"
                elif kind == "b":
                    label = "bool"
                else:
                    label = "object"
                dtype_counts[label] = dtype_counts.get(label, 0) + 1

            dtype_str = ", ".join(f"{k}({v})" for k, v in dtype_counts.items())
            st.caption(f"{len(df)} satır × {len(df.columns)} sütun · dtypes: {dtype_str}")

        except ValueError as e:
            st.error(str(e))
            return

        # --- Arama inputu ---
        search_label = texts.get("pdf_search_label", "Tabloda ara...")
        query = st.text_input(search_label, key="table_search_query")

        if query:
            try:
                filtered = df[df.apply(
                    lambda row: row.astype(str).str.contains(query, case=False, na=False).any(),
                    axis=1
                )]
            except Exception as e:
                logging.error(f"Hata: Tablo filtresi uygulanamadi: {e}")
                filtered = df

            if filtered.empty:
                no_match_msg = texts.get("table_no_match", "Aramanizla eslesen satir bulunamadi.")
                st.info(no_match_msg)
                logging.info(f"Tablo aramasinda sonuc bulunamadi. Sorgu: '{query}'")
            else:
                st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

    def display_image(self, file_path: str) -> None:
        """Görsel dosyaları zoom kontrolü ile Streamlit arayüzünde gösterir.

        Zoom seçenekleri: Fit (tam genişlik), 100% (orijinal), 200% (2×).
        """
        zoom_options = ["Fit", "100%", "200%"]
        selected_zoom = st.radio(
            "Zoom",
            zoom_options,
            horizontal=True,
            label_visibility="collapsed",
            key=f"zoom_{os.path.basename(file_path)}",
        )

        with open(file_path, "rb") as f:
            image_bytes = f.read()

        if selected_zoom == "Fit":
            st.image(image_bytes, use_container_width=True)
        elif selected_zoom == "100%":
            st.image(image_bytes, use_container_width=False)
        else:  # 200%
            # Streamlit width parametresi piksel; 1200px ~200% ortak ekran için yeterli
            st.image(image_bytes, width=1200)

    def display_audio(self, file_path: str, format: str = "audio/mp3") -> None:
        """Ses dosyalarını arayüzde oynatır."""
        with open(file_path, "rb") as f:
            st.audio(f.read(), format=format)

    def display_video(self, file_path: str, format: str = "video/mp4") -> None:
        """Video dosyalarını arayüzde oynatır."""
        with open(file_path, "rb") as f:
            st.video(f.read(), format=format)

    def display_text_document(self, file_path: str):
        """TXT, DOCX ve kod/veri metin dosyalarını okuyup arayüzde gösterir.

        Desteklenen uzantılar:
            .txt, .py, .js, .html, .css, .java, .cpp, .sql,
            .yaml, .json, .xml  → UTF-8 düz metin, st.code ile gösterilir
            .docx, .doc         → python-docx ile st.markdown
            .rtf, .odt          → düz metin olarak okunmaya çalışılır
        """
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()

        # --- DOCX / DOC: python-docx ile paragraf çıkar ---
        if uzanti in ['.docx', '.doc']:
            try:
                doc = docx.Document(file_path)
                tam_metin = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                st.markdown(tam_metin)
            except Exception as e:
                logging.error(f"Hata: Word dosyası okunurken hata oluştu ({file_path}): {e}")
                st.error(f"Word dosyası okunurken hata oluştu: {e}")

        # --- TXT: basit metin alanı ---
        elif uzanti == '.txt':
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                icerik = f.read()
            # TODO(i18n): "Belge İçeriği" → document_content anahtarına taşınacak (Ali koordinasyonu)
            st.text_area("Belge İçeriği", icerik, height=400)

        # --- Kod ve veri dosyaları: syntax highlighting ile st.code ---
        else:
            # Uzantıya göre dil adını belirle (Streamlit st.code için)
            _lang_map = {
                ".py": "python", ".js": "javascript", ".html": "html",
                ".css": "css", ".java": "java", ".cpp": "cpp",
                ".sql": "sql", ".yaml": "yaml", ".json": "json",
                ".xml": "xml", ".rtf": "text", ".odt": "text",
            }
            lang = _lang_map.get(uzanti, "text")
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    icerik = f.read()
                logging.info(f"Başarılı: Metin dosyası gösterildi ({file_path})")
                st.code(icerik, language=lang)
            except Exception as e:
                logging.error(f"Hata: Metin dosyası okunurken hata oluştu ({file_path}): {e}")
                st.error(f"Dosya okunurken hata oluştu: {e}")
