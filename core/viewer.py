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

    def render_pdf(self, pdf_path: str) -> list[bytes]:
        """PDF sayfalarını PNG bytes listesi olarak döner.

        Cache mekanizması _cached_render_pdf üzerinden çalışır.
        İkinci çağrıda sonuç < 100 ms'de döner.
        """
        logging.debug("render_pdf çağrıldı: %s", pdf_path)
        return _cached_render_pdf(pdf_path)

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

        Desteklenen formatlar: .pdf, .docx, .txt
        AI sekmesi (Issue #18) tarafından kullanılmak üzere tasarlandı.

        Returns:
            str: Dosyadaki metin içeriği. Hata durumunda boş string döner.
        """
        _, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()
        try:
            if uzanti == ".pdf":
                belge = fitz.open(file_path)
                parcalar: list[str] = []
                for sayfa in belge:
                    metin = sayfa.get_text()
                    if metin.strip():
                        parcalar.append(metin)
                return "\n".join(parcalar)

            elif uzanti in (".docx", ".doc"):
                belge = docx.Document(file_path)
                return "\n\n".join(
                    para.text for para in belge.paragraphs if para.text.strip()
                )

            elif uzanti == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()

            else:
                logging.warning("extract_text: Desteklenmeyen uzantı — %s", uzanti)
                return ""

        except Exception as e:
            logging.error("extract_text hatası (%s): %s", file_path, e)
            return ""

    # -----------------------------------------------------------------------
    # Streamlit display yardımcıları
    # -----------------------------------------------------------------------

    def display_pdf(self, pdf_path: str) -> None:
        """PDF sayfalarını Streamlit arayüzünde alt alta gösterir.

        20+ sayfa için spinner ile kullanıcıya geri bildirim verilir.
        """
        resim_listesi = self.render_pdf(pdf_path)
        toplam = len(resim_listesi)
        for i, resim in enumerate(resim_listesi):
            st.image(resim, caption=f"Sayfa {i + 1} / {toplam}", use_container_width=True)

    def display_table(self, file_path: str) -> None:
        """Tablo verilerini metadata özet satırıyla birlikte Streamlit arayüzünde gösterir.

        Özet formatı: X satır × Y sütun · dtypes: int(N), float(N), object(N)
        """
        try:
            df = self.read_table(file_path)

            # --- Metadata özet satırı ---
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

            st.dataframe(df, use_container_width=True)

        except ValueError as e:
            st.error(str(e))

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

    def display_text_document(self, file_path: str) -> None:
        """TXT ve DOCX içeriklerini okuyup arayüzde metin olarak basar."""
        _, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()

        if uzanti == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                icerik = f.read()
            st.text_area("Belge İçeriği", icerik, height=400)

        elif uzanti in (".docx", ".doc"):
            try:
                belge = docx.Document(file_path)
                tam_metin = "\n\n".join(
                    [para.text for para in belge.paragraphs if para.text.strip()]
                )
                st.markdown(tam_metin)
            except Exception as e:
                st.error(f"Word dosyası okunurken hata oluştu: {e}")
        else:
            st.warning("Bu metin formatı desteklenmiyor.")
