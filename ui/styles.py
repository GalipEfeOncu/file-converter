"""
ui/styles.py — CSS ve Görsel Özelleştirme
Sahibi: Samet Demir (Arayüz Tasarımcısı)

Senin Görevin:
Uygulamayı Streamlit'in standart görünümünden çıkarıp, özel CSS enjeksiyonları ile kurumsal ve modern bir tasarıma (karanlık tema, özel butonlar vb.) kavuşturmak.

Çıktı: "Uygulama geneline uygulanan modern CSS stilleri."
"""

import streamlit as st

def apply_custom_css():
    """Uygulama geneline özel CSS enjekte eder."""
    custom_css = """
    <style>
        /* Samet Demir — Özel CSS kodları buraya yazılacak */
        /* Örn: .stButton>button { background-color: #4CAF50; } */
    </style>
    """
    # TODO: Samet Demir — Kurumsal kimliğe uygun renk paletini uygula.
    st.markdown(custom_css, unsafe_allow_html=True)
