"""
ui/styles.py — CSS ve Görsel Özelleştirme (Minimalist Sürüm)
Sahibi: Samet Demir (Arayüz Tasarımcısı)
"""

import streamlit as st


def apply_custom_css(theme: str = "dark"):
    """Uygulama geneline özel CSS enjekte eder (Sadece Streamlit'in kontrol etmediği alanlar)."""
    
    custom_css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {{
          --radius-sm: 6px;
          --radius-md: 10px;
          --space-1: 4px;
          --space-2: 8px;
          --space-3: 12px;
          --space-4: 16px;
          --space-5: 20px;
          --space-6: 24px;
          --space-8: 32px;
          --space-10: 40px;
        }}

        /* Global Reset & Typography */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
          font-family: 'Inter', -apple-system, sans-serif !important;
        }}

        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
          border-right: 1px solid rgba(151, 151, 151, 0.1);
        }}
        
        [data-testid="stSidebarNav"] {{
          background-color: transparent !important;
        }}

        /* Buttons Fix */
        .stButton > button {{
          border-radius: var(--radius-sm) !important;
          transition: all 0.2s ease !important;
          height: 38px !important;
          font-weight: 500 !important;
          display: flex !important;
          align-items: center !important;
          justify-content: center !important;
          padding: 0 20px !important;
        }}

        .stButton > button:hover {{
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        /* ================================================================
           File Uploader — Türkçe Yerelleştirme (CSS Hack)
           Streamlit'in hardcoded metinleri (Drag and drop, Limit 200MB,
           Browse files) font-size:0 ile gizlenir; ::before ile Türkçe
           alternatifler eklenir.
           ================================================================ */

        /* Dropzone kutu stili */
        [data-testid="stFileUploadDropzone"] {{
          border: 1px dashed rgba(151, 151, 151, 0.3) !important;
          border-radius: var(--radius-md) !important;
          background-color: rgba(151, 151, 151, 0.05) !important;
          padding: 2rem !important;
          position: relative !important;
        }}

        /* "Drag and drop file here" metnini gizle, Türkçe ekle */
        [data-testid="stFileUploadDropzone"] > div > div > p {{
          font-size: 0 !important;
          color: transparent !important;
          line-height: 0 !important;
        }}

        [data-testid="stFileUploadDropzone"] > div > div > p::before {{
          content: "Dosyay\0131 buraya s\00FCr\00FCkle ve b\0131rak";
          font-size: 14px !important;
          color: var(--text-primary, #e0e0e0) !important;
          font-family: 'Inter', -apple-system, sans-serif !important;
          font-weight: 400 !important;
          line-height: 1.5 !important;
          display: block;
        }}

        /* "Limit 200MB per file" — small elementi */
        [data-testid="stFileUploadDropzone"] small {{
          font-size: 0 !important;
          color: transparent !important;
        }}

        [data-testid="stFileUploadDropzone"] small::before {{
          content: "Dosya ba\015f\0131na 200 MB s\0131n\0131r";
          font-size: 12px !important;
          color: var(--text-secondary, #9e9e9e) !important;
          font-family: 'Inter', -apple-system, sans-serif !important;
        }}

        /* "Browse files" butonu — sadece dropzone içindeki upload action butonu */
        [data-testid="stFileUploadDropzone"] [data-testid="baseButton-secondary"] {{
          color: transparent !important;
          font-size: 0 !important;
          position: relative !important;
          min-width: 110px;
        }}

        [data-testid="stFileUploadDropzone"] [data-testid="baseButton-secondary"]::before {{
          content: "Dosya Se\00E7";
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 14px !important;
          font-weight: 500 !important;
          font-family: 'Inter', -apple-system, sans-serif !important;
          color: var(--text-primary, #e0e0e0) !important;
          white-space: nowrap;
        }}


        /* Selectbox & Widgets */
        div[data-baseweb="select"] {{
          border-radius: var(--radius-sm) !important;
        }}
        
        /* Settings Specific Layout */
        .settings-section {{
          margin-bottom: var(--space-8);
        }}
        
        .settings-card {{
          background-color: rgba(151, 151, 151, 0.05);
          border: 1px solid rgba(151, 151, 151, 0.1);
          border-radius: var(--radius-md);
          padding: var(--space-5);
          margin-bottom: var(--space-4);
        }}

        /* Tabs Styling */
        [data-testid="stTabs"] [role="tablist"] {{
          gap: 12px;
        }}
        
        [data-testid="stTabs"] button[role="tab"] {{
          background-color: transparent !important;
          border: none !important;
          font-weight: 500 !important;
        }}

        /* History Items Styling */
        .history-file-item {{
          background-color: rgba(151, 151, 151, 0.08);
          border: 1px solid rgba(151, 151, 151, 0.1);
          padding: var(--space-3);
          border-radius: var(--radius-sm);
          margin-bottom: var(--space-2);
          transition: background-color 0.2s;
        }}
        
        .history-file-item:hover {{
          background-color: rgba(151, 151, 151, 0.15);
        }}
        
        .history-file-item-time {{
          font-size: 0.75rem;
          opacity: 0.6;
        }}

        /* Hide Streamlit elements */
        #MainMenu, footer, header {{
          visibility: hidden !important;
        }}
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Streamlit'in hardcoded İngilizce file uploader metinlerini Türkçeleştir.
    # CSS hack ile desteklenen bu JS, MutationObserver + periyodik kontrol
    # kombinasyonuyla Streamlit'in gecikmeli renderını da yakalar.
    # --------------------------------------------------------------------------
    st.markdown("""
    <script>
    (function() {
        var TR = {
            "Drag and drop file here": "Dosyay\u0131 buraya s\u00fcr\u00fckle ve b\u0131rak",
            "Drag and drop files here": "Dosyalar\u0131 buraya s\u00fcr\u00fckle ve b\u0131rak",
            "Limit 200MB per file": "Dosya ba\u015f\u0131na 200\u00a0MB s\u0131n\u0131r",
            "Browse files": "Dosya Se\u00e7"
        };

        function translateNode(node) {
            if (node.nodeType !== Node.TEXT_NODE) return;
            for (var en in TR) {
                if (node.textContent.indexOf(en) !== -1) {
                    node.textContent = node.textContent.replace(en, TR[en]);
                }
            }
        }

        function walkAndTranslate(root) {
            var walker = document.createTreeWalker(
                root, NodeFilter.SHOW_TEXT, null, false
            );
            var node;
            while ((node = walker.nextNode())) { translateNode(node); }
        }

        // İlk çalıştırma
        walkAndTranslate(document.body);

        // MutationObserver: DOM değişikliklerini yakala
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(m) {
                m.addedNodes.forEach(function(n) {
                    if (n.nodeType === Node.ELEMENT_NODE) walkAndTranslate(n);
                    else translateNode(n);
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });

        // setInterval güvenlik ağı: Streamlit gecikmeli render için
        // ilk 10 saniye boyunca her 500ms'de bir tekrar çalışır
        var attempts = 0;
        var interval = setInterval(function() {
            walkAndTranslate(document.body);
            attempts++;
            if (attempts >= 20) clearInterval(interval);
        }, 500);
    })();
    </script>
    """, unsafe_allow_html=True)
