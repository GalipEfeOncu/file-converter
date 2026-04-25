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

        /* --- Dosya Yükleyici (File Uploader) Tasarımı --- */
        /* Sürükle-bırak kutusu stillemesi */
        [data-testid="stFileUploadDropzone"] {
            background: linear-gradient(135deg, rgba(5, 82, 204, 0.15), rgba(0, 214, 167, 0.1)) !important;
            border: 2px dashed rgba(0, 214, 167, 0.5) !important;
            border-radius: var(--radius) !important;
            padding: 30px 20px !important;
            transition: all 200ms ease !important;
        }

        [data-testid="stFileUploadDropzone"]:hover {
            background: linear-gradient(135deg, rgba(5, 82, 204, 0.25), rgba(0, 214, 167, 0.2)) !important;
            border-color: rgba(0, 214, 167, 0.8) !important;
            box-shadow: 0 8px 24px rgba(0, 214, 167, 0.2) !important;
        }

        /* Dosya yükleyici içindeki metin */
        [data-testid="stFileUploadDropzone"] > div {
            color: rgba(242, 247, 255, 0.8) !important;
            font-weight: 500 !important;
        }

        /* Dosya yükleyici ikon */
        [data-testid="stFileUploadDropzone"] svg {
            color: rgba(0, 214, 167, 0.7) !important;
        }

        /* Browse button */
        [data-testid="stFileUploadDropzone"] > button {
            background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent)) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            margin-top: 10px !important;
            transition: all 150ms ease !important;
        }

        [data-testid="stFileUploadDropzone"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(0, 82, 204, 0.4) !important;
        }

        /* Yüklenen dosya gösterimi */
        [data-testid="stFileUploadDropzone"] + div {
            margin-top: 15px !important;
        }

        /* Tabs Tasarımı */
        [data-testid="stTabs"] [role="tablist"] {
            border-bottom: 2px solid rgba(242, 247, 255, 0.1) !important;
            gap: 5px !important;
        }

        [data-testid="stTabs"] button[role="tab"] {
            background: transparent !important;
            color: rgba(242, 247, 255, 0.6) !important;
            border-bottom: 3px solid transparent !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            transition: all 200ms ease !important;
        }

        [data-testid="stTabs"] button[role="tab"]:hover {
            color: rgba(242, 247, 255, 0.9) !important;
            border-bottom-color: rgba(0, 214, 167, 0.4) !important;
        }

        [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            color: var(--brand-accent) !important;
            border-bottom: 3px solid transparent !important;
            border-image: linear-gradient(90deg, var(--brand-primary), var(--brand-accent)) 1 !important;
        }

        /* Uyarılar (Alerts & Toasts) - Başarı ve Hata Varyantları */
        [data-testid="stAlert"] {
            border-radius: var(--radius) !important;
            font-weight: 500 !important;
            border: 1px solid var(--border) !important;
        }
        
        [data-testid="stAlert"]:has([data-testid="stMarkdownContainer"]) {
            /* General styling for alerts */
            background-color: var(--bg-surface-2) !important;
        }

        /* Sidebar öğeleri */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has(> .stRadio) {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: var(--radius) !important;
            padding: 8px !important;
            margin: 8px 0 !important;
        }

        /* Radio butonları */
        .stRadio > label {
            color: rgba(242, 247, 255, 0.85) !important;
            font-weight: 500 !important;
            padding: 8px 12px !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            transition: all 150ms ease !important;
        }

        .stRadio > label:hover {
            background: rgba(0, 214, 167, 0.15) !important;
        }

        .stRadio input[type="radio"]:checked + span {
            color: var(--brand-accent) !important;
        }

        /* Expander (Ayarlar vb.) */
        [data-testid="stExpander"] > summary {
            color: rgba(242, 247, 255, 0.8) !important;
            font-weight: 600 !important;
            padding: 12px !important;
            background: rgba(0, 214, 167, 0.08) !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            transition: all 150ms ease !important;
        }

        [data-testid="stExpander"] > summary:hover {
            background: rgba(0, 214, 167, 0.15) !important;
        }

        /* Streamlit varsayılan üst menü ve footer gizleme */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
