# =============================================================================
# core/converter.py — Dosya Format Dönüştürme Motoru
# =============================================================================
#
# SORUMLULUK: Mantık & Algoritma Mühendisi
#
# Bu dosya tüm dosya dönüştürme işlemlerini barındırır. Görevleri:
#
#   1. BELGE DÖNÜŞÜMÜ:
#      - PDF  → DOCX  : PyPDF2 metin çıkarma + python-docx ile yazma
#      - PDF  → TXT   : PyPDF2 ile ham metin çıkarma
#      - PDF  → PNG/JPG: PyMuPDF (fitz) ile her sayfayı görüntüye çevirme
#      - DOCX → PDF   : python-docx okuma, Pillow/WeasyPrint ile dışa aktarma
#      - DOCX → TXT   : python-docx paragraflarını düz metin olarak kaydetme
#      - CSV  → XLSX  : pandas read_csv + to_excel (openpyxl engine)
#      - XLSX → CSV   : pandas read_excel + to_csv
#
#   2. GÖRSEL DÖNÜŞÜMÜ:
#      - PNG  ↔ JPG   : Pillow Image.open() + save(format=...)
#      - PNG/JPG → WEBP: Pillow ile kalite parametresi destekli dönüşüm
#
#   3. HATA YAKALAMA:
#      - Her dönüşüm fonksiyonu try/except ile sarılacak.
#      - Başarı durumunda çıktı dosyasının yolunu, hata durumunda
#        açıklayıcı bir hata mesajını (str) döndürecek.
#
#   4. FONKSİYON İMZASI STANDARDI:
#      Her dönüşüm fonksiyonu şu imzayı izleyecek:
#        convert_X_to_Y(input_path: str, output_path: str) -> dict
#        -> {"success": bool, "output": str, "error": str | None}
#
# BAĞIMLILIKLAR: PyPDF2, PyMuPDF, python-docx, pandas, openpyxl, Pillow
#
# =============================================================================
