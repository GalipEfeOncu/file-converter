# =============================================================================
# core/viewer.py — Dahili Dosya Görüntüleme Motoru
# =============================================================================
#
# SORUMLULUK: Dosya Görüntüleme Uzmanı
#
# Bu dosya, kullanıcının harici bir programa ihtiyaç duymadan dosyaları uygulama içinde görüntüleyebilmesini sağlar. Görevleri:
#
#   1. PDF GÖRÜNTÜLEME:
#      - PyMuPDF (fitz) ile PDF dosyasının her sayfasını PNG'ye dönüştürür.
#      - Elde edilen PNG byte dizisini Streamlit'te st.image() ile gösterir.
#      - Sayfa navigasyonu (önceki / sonraki sayfa) için hazır veri döndürür.
#
#   2. TABLO GÖRÜNTÜLEME (CSV / XLSX):
#      - pandas ile dosyayı DataFrame'e yükler.
#      - st.dataframe() ile etkileşimli tablo olarak gösterilmek üzere
#        DataFrame nesnesini döndürür.
#
#   3. WORD / METİN GÖRÜNTÜLEME (DOCX / TXT):
#      - python-docx ile .docx paragraflarını okur.
#      - .txt dosyalarını UTF-8 binary-safe olarak açar.
#      - Ham metin veya Markdown formatında string döndürür;
#        st.text_area() veya st.markdown() ile gösterilir.
#
#   4. GÖRSEL GÖRÜNTÜLEME (PNG / JPG / WEBP):
#      - Pillow ile resmi açar, boyut bilgisini ekler.
#      - st.image() için hazır bytes nesnesi döndürür.
#
#   5. SES OYNATICI (MP3):
#      - Ses dosyasını bytes olarak okur.
#      - st.audio() bileşenine aktarılmak üzere hazır hale getirir.
#
# BAĞIMLILIKLAR: PyMuPDF, pandas, openpyxl, python-docx, Pillow
#
# =============================================================================
