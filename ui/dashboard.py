# =============================================================================
# ui/dashboard.py — Streamlit Sayfa Düzeni ve Bileşenler
# =============================================================================
#
# SORUMLULUK: Arayüz Tasarımcısı
#
# Bu dosya uygulamanın tüm görsel düzenini, sekmeleri ve etkileşimli
# UI bileşenlerini içerir. Görevleri:
#
#   1. SAYFA DÜZENİ (LAYOUT):
#      - st.sidebar kullanarak gezinme, ayarlar ve yükleme alanları sunmak.
#      - st.tabs ile modülleri (Dönüştür / Görüntüle / AI Analiz) ayırmak.
#      - st.columns ile yan yana düzenler oluşturmak (örn. "Orijinal Dosya"
#        ve "Dönüştürülen Dosya").
#
#   2. BİLEŞENLER:
#      - st.file_uploader: Kullanıcıdan giriş dosyalarını almak.
#      - st.button, st.selectbox, st.radio vb.: Kullanıcı etkileşimlerini almak.
#      - st.spinner, st.success, st.error: İşlem durumlarını göstermek.
#      - st.metric: AI analizi sonucu elde edilen sayısal verileri vb. sunmak.
#
#   3. TASARIM KURALLARI:
#      - Bu dosya içinde iş mantığı (API çağırma, dönüşüm algoritması)
#        KESİNLİKLE yer almaz.
#      - Fonksiyonlar sadece UI'ı çizer ve kullanıcı girişlerini main.py'ye
#        veya session_state'e aktarır.
#
# BAĞIMLILIKLAR: streamlit
#
# =============================================================================
