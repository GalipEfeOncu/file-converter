"""
main.py — Uygulama Giriş Noktası ve Ana Kontrol Merkezi
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Uygulamanın ana iskeletini oluşturmak, sayfa yapılandırmasını kurmak ve diğer ekip üyelerinin yazdığı modülleri (converter, viewer, ai_engine vb.) sistemle entegre etmek.

Çıktı: "Tüm modülleri bir araya getiren, kullanıcı dostu ve işlevsel bir Streamlit arayüzü."
"""

import streamlit as st
import json
from config.settings import Config
from ui.styles import apply_custom_css
from ui.dashboard import Dashboard
from ui.onboarding import show_onboarding


def load_languages():
    """
    JSON dosyasından dil verilerini okur.
    """
    try:
        # with içindeki blok bittiğinde dosya otomatik kapanır. Bu sayede dosya ile ilgili bir hata oluşmaz.
        with open("assets/languages.json", "r", encoding="utf-8") as f:  # r = read, utf-8 = türkçe karakter desteği
            all_langs = json.load(f)  # JSON dosyasını okur.
            return all_langs[st.session_state.language]  # Hafızadaki dile göre çeviriyi döndürür.
    except FileNotFoundError:
        st.error("languages.json dosyası bulunamadı!")
        return {}


def init_state():
    """
    Pythonda her işlem (butonlara basmak gibi) sayfayı yeniler ve en üstten okumaya başlar. Bundan dolayı her yenilemede
    yapılan işlemler yok olmasın diye st.session_state kullanılır.
    """
    prefs = Config.load_user_prefs()

    if "language" not in st.session_state:
        st.session_state.language = prefs.get("language", "en")

    if "theme" not in st.session_state:
        st.session_state.theme = prefs.get("theme", "dark")

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "convert"

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    if "file_history" not in st.session_state:
        st.session_state.file_history = []

    if "onboarding_seen" not in st.session_state:
        st.session_state.onboarding_seen = prefs.get("onboarding_seen", False)
    
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False


def main():
    # Sayfayı Konfigüre eder. Sayfa başlığı ve genişliği
    st.set_page_config(page_title=Config.APP_NAME, layout="wide")
    
    init_state()  # Hafıza kontrolü yapar. Eğer hafızada bir şey yoksa oluşturur
    apply_custom_css(theme=st.session_state.theme)  # Tasarım sistemi ve özel renk/tipografi kurulumunu uygula

    texts = load_languages()
    
    # Dashboard'u başlat - Galip Efe ile eş zamanlı uzatma tasarımlarının entegrasyonu
    dashboard = Dashboard(texts)
    
    # Sidebar'ı render et (Samet Demir - Modern sidebar with File History & Language Selection)
    dashboard.render_sidebar()
    
    # Onboarding kontrolü
    if not st.session_state.onboarding_seen:
        show_onboarding(texts)
        return

    # Ana alanı veya Ayarlar sayfasını render et
    if st.session_state.get("show_settings"):
        dashboard.render_settings_page()
    else:
        dashboard.render_main_area()


if __name__ == "__main__":
    main()
