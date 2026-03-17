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
        st.session_state.active_tab = "home"

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None


def main():
    # Sayfayı Konfigüre eder. Sayfa başlığı ve genişliği
    st.set_page_config(page_title=Config.APP_NAME, layout="wide")

    init_state()  # Hafıza kontrolü yapar. Eğer hafızada bir şey yoksa oluşturur

    texts = load_languages()
    with st.sidebar:
        lang_display = {"tr": "Türkçe 🇹🇷", "en": "English 🇺🇸"}
        current_index = 0 if st.session_state.language == "tr" else 1
        selected_lang_name = st.selectbox("Dil / Language", options=list(lang_display.values()), index=current_index)

        for key, value in lang_display.items():
            if value == selected_lang_name:
                if st.session_state.language != key:
                    st.session_state.language = key
                    st.rerun()

    # Ana Başlık
    st.title(texts["app_title"])

    # Kullanıcıyı bilgilendiren mesaj
    st.info("Proje mimarisi kuruluyor. Modüller yüklendiğinde burası ana çalışma alanına dönüşecek.")

    # --- GECİCİ SIDEBAR ---
    # Henüz Samet sidebarı yazmadığı için geçici olarak sidebar ekliyorum
    with st.sidebar:
        st.title(texts["sidebar_title"])
        tab_options = [texts["home_tab"], texts["convert_tab"], texts["view_tab"], texts["ai_tab"]]

        # Eğer hafızadaki tab seçeneklerde yoksa (ilk açılış veya dil değişimi), ilk tabı varsayılan yap.
        if st.session_state.active_tab not in tab_options:
            st.session_state.active_tab = texts["home_tab"]

        # Bulunduğu tabın listedeki sırasını bul (st.radio'nun doğru yeri göstermesi için)
        current_index = tab_options.index(st.session_state.active_tab)

        st.radio(texts["sidebar_title"], tab_options, index=current_index, key="active_tab")

        st.divider()
        supported = [ext.replace(".", "") for ext in Config.SUPPORTED_EXTENSIONS]  # Dizi içindeki . işaretlerini kaldırır

        file = st.file_uploader(texts["upload_file"], type=supported)  # Dosya yükleme paneli

        if file:  # Eğer dosya yüklenmişse
            st.session_state.uploaded_file = file  # Hafızaya atar
            st.success(f"{texts['file_uploaded']}: {file.name}")

    if st.session_state.active_tab == texts["home_tab"]:
        st.header(texts["home_tab"])
    elif st.session_state.active_tab == texts["convert_tab"]:
        st.header(texts["convert_tab"])
        st.write("Dönüştürme işlemleri burada yapılacak.")
    elif st.session_state.active_tab == texts["view_tab"]:
        st.header(texts["view_tab"])
        st.write("Dosya görüntüleme işlemleri burada yapılacak.")
    elif st.session_state.active_tab == texts["ai_tab"]:
        st.header(texts["ai_tab"])
        st.write("AI analiz işlemleri burada yapılacak.")
    # --- GECİCİ SIDEBAR SONU ---


if __name__ == "__main__":
    main()
