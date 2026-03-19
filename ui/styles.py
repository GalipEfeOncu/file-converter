"""
ui/styles.py — CSS ve Görsel Özelleştirme
Sahibi: Samet Demir (Arayüz Tasarımcısı)

Senin Görevin:
Uygulamayı Streamlit'in standart görünümünden çıkarıp, özel CSS enjeksiyonları ile kurumsal ve modern bir tasarıma (karanlık tema, özel butonlar vb.) kavuşturmak.

Çıktı: "Uygulama geneline uygulanan modern CSS stilleri."
"""

import streamlit as st


def apply_custom_css():
    """Uygulama geneline özel CSS enjekte eder.

    Bu fonksiyon:
    - Kurumsal renk paleti ve tipografi (CSS değişkenleri / design tokens)
    - Streamlit bileşenlerinin (buton, girdi, kenar çubuğu vb.) yeniden stillenmesi
    - Sayfa genelinde modern bir karanlık tema uygulanması

    Kullandığınız renkleri / fontu değiştirmek için aşağıdaki :root blokundaki değişkenleri düzenleyin.
    """
    custom_css = """
    <style>
        /* --- Kurumsal Tasarım Sistemi (Renk & Tipografi) --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            /* Renk Paleti */
            --brand-primary: #0052CC; /* Canlı mavi */
            --brand-secondary: #FFAB00; /* Canlı turuncu */
            --brand-accent: #00D6A7; /* Canlı yeşil */
            --bg-base: #0b1220; /* Ana arka plan */
            --bg-surface: #111b30; /* Kart arka planı */
            --bg-surface-2: #1c2a4a; /* Kart arka planı 2 */
            --text-primary: #f2f7ff; /* Ana metin */
            --text-secondary: rgba(242, 247, 255, 0.75); /* İkincil metin */
            --border: rgba(242, 247, 255, 0.12);
            --shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
            --radius: 14px;

            /* Tipografi */
            --font-base: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
            --text-size-base: 15px;
            --text-size-lg: 18px;
            --text-size-sm: 13px;
            --heading-weight: 700;
            --body-weight: 400;
        }

        /* Sayfa genelini ayarla */
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg-base) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-base) !important;
            font-size: var(--text-size-base) !important;
        }

        /* Başlıklar */
        h1, h2, h3, h4, h5, h6 {
            font-weight: var(--heading-weight) !important;
            letter-spacing: 0.02em;
        }

        /* Metin ve label */
        p, span, label, div, .css-1dp5vir {
            color: var(--text-primary) !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, rgba(5, 65, 119, 0.95) 0%, rgba(12, 16, 33, 0.95) 100%) !important;
            border-right: 1px solid var(--border) !important;
        }

        /* Buttonlar */
        .stButton>button,
        button[kind="secondary"] {
            background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent)) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            border-radius: var(--radius) !important;
            box-shadow: var(--shadow) !important;
            color: var(--text-primary) !important;
            padding: 0.65rem 1.1rem !important;
            font-weight: 600 !important;
            transition: transform 150ms ease, box-shadow 150ms ease, background 150ms ease;
        }

        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 18px 35px rgba(0, 0, 0, 0.45) !important;
            background: linear-gradient(135deg, var(--brand-secondary), var(--brand-accent)) !important;
        }

        .stButton>button:active {
            transform: translateY(0) !important;
            box-shadow: 0 10px 18px rgba(0, 0, 0, 0.35) !important;
        }

        /* Input / Select / Textarea */
        input, textarea, select {
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            color: var(--text-primary) !important;
            padding: 0.6rem 0.8rem !important;
        }

        input:focus, textarea:focus, select:focus {
            outline: none !important;
            border-color: rgba(0, 210, 167, 0.9) !important;
            box-shadow: 0 0 0 3px rgba(0, 214, 167, 0.25) !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.04);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.35);
        }

        /* Streamlit varsayılan üst menü ve footer gizleme */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
