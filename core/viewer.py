"""
core/viewer.py — Dosya Görüntüleme ve Render Modülü
Sahibi: Abdulkadir Sar (Dosya Görüntüleme Uzmanı)

Senin Görevin:
Kullanıcının yüklediği dosyaları (özellikle PDF, Excel, Word) uygulama arayüzünde doğrudan okunabilir hale getirmek. PDF'leri resme çevirmek, tabloları Pandas ile görselleştirmek.

Çıktı: "Streamlit bileşenlerine uygun formatta işlenmiş görsel veya metinsel veri."
"""

import pandas as pd

class FileViewer:
    """Dosyaları önizleme için uygun formata dönüştürür."""

    def render_pdf(self, pdf_path: str):
        """PDF sayfalarını görsel olarak render eder."""
        # TODO: Abdulkadir Sar — PyMuPDF (fitz) ile PDF-to-Image dönüşümü.
        pass

    def read_table(self, file_path: str) -> pd.DataFrame:
        """CSV veya Excel dosyalarını DataFrame olarak okur."""
        # TODO: Abdulkadir Sar — Dosya uzantısına göre Pandas read fonksiyonlarını çağır.
        return pd.DataFrame()
