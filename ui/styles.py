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

        /* File Uploader Styling */
        [data-testid="stFileUploadDropzone"] {{
          border: 1px dashed rgba(151, 151, 151, 0.3) !important;
          border-radius: var(--radius-md) !important;
          background-color: rgba(151, 151, 151, 0.05) !important;
          padding: 2rem !important;
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
