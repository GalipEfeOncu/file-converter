# =============================================================================
# main.py — Streamlit Uygulama Giriş Noktası & Durum Yönetimi
# =============================================================================
#
# SORUMLULUK: Mimar (Galip Efe Öncü)
#
# Bu dosya uygulamanın kalbidir. Görevleri:
#
#   1. Streamlit sayfa konfigürasyonunu (st.set_page_config) kurmak.
#   2. session_state üzerinden global uygulama durumunu (seçili dosya, aktif mod, seçili dil vb.) başlatmak ve yönetmek.
#   3. ui/dashboard.py'den sayfa düzenini, ui/styles.py'den CSS enjeksiyonunu import ederek uygulamak.
#   4. Kullanıcının seçtiği moda göre (Dönüştür / Görüntüle / AI Analiz) core/ modüllerini (converter, viewer, ai_engine, player) çağırmak.
#   5. Sidebar'da dosya yükleme (st.file_uploader / sürükle-bırak), mod seçimi ve dil seçeneği sunmak.
#   6. config/settings.py'den uygulama geneli sabitleri okumak.
#
# KULLANIM:
#   streamlit run main.py
#
# =============================================================================
