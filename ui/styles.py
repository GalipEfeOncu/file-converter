# =============================================================================
# ui/styles.py — CSS Tema ve Modern Tasarım Sistemi
# =============================================================================
#
# SORUMLULUK: Arayüz Tasarımcısı
#
# Bu modül, Streamlit uygulamasının görünümünü modernize etmek için özel CSS enjeksiyonu sağlar. Görevleri:
#
#   1. TEMA VE RENK PALETİ:
#      - Hem açık hem de karanlık temaya uyumlu, minimal ve düz (flat) bir CSS strüktürü kurmak.
#      - Gradient alanlar ve kutu gölgeleri (box-shadow) KESİNLİKLE kullanılmayacaktır.
#      - Kenar yuvarlatmaları (border-radius) çok ufak (örn. 2px-4px) tutulacaktır.
#
#   2. STREAMLIT OVERRIDES:
#      - Streamlit'in varsayılan buton (st.button) tasarımını daha
#        çekici hale getirmek.
#      - Sidebar ve ana içerik alanlarının arka planlarını ayrıştırmak.
#      - Header ve Typography (Google Fonts vb.) ayarlarını uygulamak.
#
#   3. UYGULAMA METODU:
#      - CSS kodları python string'leri olarak tanımlanır.
#      - st.markdown("<style>...</style>", unsafe_allow_html=True)
#        kullanılarak `main.py` içinde projeye entegre edilir.
#
# =============================================================================
