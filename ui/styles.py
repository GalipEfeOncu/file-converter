"""
ui/styles.py — CSS ve Görsel Özelleştirme
Sahibi: Samet Demir (Arayüz Tasarımcısı)
"""

import streamlit as st


def apply_custom_css(theme: str = "dark"):
    """Uygulama geneline özel CSS enjekte eder."""
    
    # Try to read theme from session_state if available, falling back to passed parameter
    try:
        if "theme" in st.session_state:
            theme = st.session_state.theme
    except Exception:
        pass

    # Design Tokens
    if theme == "light":
        colors = """
        :root {
          --bg-base: #f8f9fc;
          --bg-surface: #ffffff;
          --bg-elevated: #f1f4f9;
          --border: #e2e8f0;
          --text-primary: #1e293b;
          --text-secondary: #64748b;
          --accent: #5b6af0;
          --accent-hover: #4a59e8;
          --success: #10b981;
          --error: #ef4444;
          --warning: #f59e0b;
        }
        """
    else:
        colors = """
        :root {
          --bg-base: #0f1117;
          --bg-surface: #1a1d27;
          --bg-elevated: #222536;
          --border: #2e3147;
          --text-primary: #e8eaf0;
          --text-secondary: #8b8fa8;
          --accent: #5b6af0;
          --accent-hover: #4a59e8;
          --success: #3d9970;
          --error: #e05c5c;
          --warning: #d4924a;
        }
        """

    custom_css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        {colors}

        :root {{
          --radius-sm: 6px;
          --radius-md: 8px;
          --space-1: 4px;
          --space-2: 8px;
          --space-3: 12px;
          --space-4: 16px;
          --space-5: 20px;
          --space-6: 24px;
          --space-8: 32px;
          --space-10: 40px;
        }}

        /* Global Reset */
        * {{
          font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", system-ui, sans-serif !important;
          -webkit-font-smoothing: antialiased;
        }}

        html, body, [data-testid="stAppViewContainer"] {{
          background-color: var(--bg-base) !important;
          color: var(--text-primary) !important;
        }}

        /* Sidebar Alignment & Color */
        [data-testid="stSidebar"] {{
          background-color: var(--bg-surface) !important;
          border-right: 1px solid var(--border) !important;
        }}
        
        [data-testid="stSidebarContent"] {{
          background-color: var(--bg-surface) !important;
          padding: var(--space-6) var(--space-5) !important;
        }}

        /* Typography Scale */
        h1 {{ 
          font-size: 20px !important; 
          font-weight: 600 !important; 
          letter-spacing: -0.01em !important; 
          margin-bottom: var(--space-1) !important; 
          color: var(--text-primary) !important;
        }}
        h2 {{ 
          font-size: 15px !important; 
          font-weight: 600 !important; 
          letter-spacing: -0.005em !important; 
          margin-bottom: 2px !important; 
          color: var(--text-primary) !important;
        }}
        h3 {{ 
          font-size: 13px !important; 
          font-weight: 500 !important; 
          color: var(--text-secondary) !important; 
        }}

        /* Main Content Area */
        [data-testid="stMainBlockContainer"] {{
          padding: var(--space-8) var(--space-10) !important;
          max-width: 960px !important;
        }}

        /* Cards and Containers */
        .settings-card, .st-emotion-cache-12w0qpk {{ 
          background-color: var(--bg-surface) !important;
          padding: 16px 20px !important; 
          border: 1px solid var(--border) !important; 
          border-radius: 8px !important;
          margin-bottom: 12px !important;
        }}

        /* Buttons */
        .stButton > button {{
          height: 36px !important;
          padding: 0 16px !important;
          font-size: 13px !important;
          font-weight: 500 !important;
          border-radius: 6px !important;
          border: 1px solid var(--border) !important;
          background: var(--bg-elevated) !important;
          color: var(--text-primary) !important;
          transition: all 150ms ease !important;
        }}
        
        .stButton > button:hover {{
          background: var(--accent) !important;
          border-color: var(--accent) !important;
          color: #ffffff !important;
        }}
        
        .stButton > button[kind="primary"] {{
          background: var(--accent) !important;
          border-color: var(--accent) !important;
          color: #ffffff !important;
        }}

        /* File Uploader FIX (Visual inconsistency in screenshot) */
        [data-testid="stFileUploadDropzone"] {{
          background-color: var(--bg-surface) !important;
          border: 1px dashed var(--border) !important;
          border-radius: 8px !important;
          color: var(--text-primary) !important;
        }}
        
        [data-testid="stFileUploadDropzone"] div[data-testid="stMarkdownContainer"] p {{
          color: var(--text-secondary) !important;
        }}

        /* Input Fields */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
          background-color: var(--bg-elevated) !important;
          border: 1px solid var(--border) !important;
          color: var(--text-primary) !important;
        }}

        /* Radio Buttons */
        .stRadio label p {{
          color: var(--text-primary) !important;
        }}

        /* History Items */
        .history-file-item {{
          background-color: var(--bg-elevated) !important;
          border: 1px solid var(--border) !important;
          border-radius: 6px !important;
          margin-bottom: 8px !important;
          padding: 10px !important;
        }}

        /* Divider */
        hr {{
          border-top: 1px solid var(--border) !important;
        }}

        /* Hide elements */
        #MainMenu, footer, header {{
          visibility: hidden !important;
        }}
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
