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
    if "language" not in st.session_state:  # Hafızada language yok ise tr olarak atar
        st.session_state.language = "tr"

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "convert"

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    if "file_history" not in st.session_state:
        st.session_state.file_history = []


def main():
    # Sayfayı Konfigüre eder. Sayfa başlığı ve genişliği
    st.set_page_config(page_title=Config.APP_NAME, layout="wide")
    apply_custom_css()  # Tasarım sistemi ve özel renk/tipografi kurulumunu uygula

    init_state()  # Hafıza kontrolü yapar. Eğer hafızada bir şey yoksa oluşturur

    texts = load_languages()
    
    # Dashboard'u başlat - Galip Efe ile eş zamanlı uzatma tasarımlarının entegrasyonu
    dashboard = Dashboard(texts)
    
    # Sidebar'ı render et (Samet Demir - Modern sidebar with File History & Language Selection)
    dashboard.render_sidebar()
    
    # Ana alanı render et (Samet Demir - st.tabs entegrasyonu)
    dashboard.render_main_area()


if __name__ == "__main__":
    main()
