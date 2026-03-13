"""
main.py — Uygulama Giriş Noktası ve Ana Kontrol Merkezi
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Uygulamanın ana iskeletini oluşturmak, sayfa yapılandırmasını kurmak ve diğer ekip üyelerinin yazdığı modülleri (converter, viewer, ai_engine vb.) sistemle entegre etmek.

Çıktı: "Tüm modülleri bir araya getiren, kullanıcı dostu ve işlevsel bir Streamlit arayüzü."
"""

import streamlit as st
# Diğer modüller eklenecek (Örn: from core.converter import Converter)

def main():
    # 1. Sayfa Konfigürasyonu
    st.set_page_config(page_title="Universal File Workstation", layout="wide")
    
    # 2. Ana Başlık
    st.title("🗂️ Universal File Workstation")
    
    # TODO: Galip Efe Öncü — Sidebar ve modül sekmelerini (Tabs) oluştur.
    # TODO: Galip Efe Öncü — session_state üzerinden global değişkenleri (dil, yüklü dosya vb.) yönet.
    
    st.info("Proje mimarisi kuruluyor. Modüller yüklendiğinde burası ana çalışma alanına dönüşecek.")

if __name__ == "__main__":
    main()
