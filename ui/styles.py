"""
ui/styles.py — CSS ve Görsel Özelleştirme
Sahibi: Samet Demir (Arayüz Tasarımcısı)

Linear/Raycast esintili tema: dark & light uyumlu CSS değişkenleri,
upload hero, kategori kartları, format pill'leri, convert grid,
settings bileşenleri.
"""

import streamlit as st


def apply_custom_css(theme: str = "dark"):
    """Tema-aware CSS enjekte eder."""

    is_dark = theme != "light"

    if is_dark:
        color_vars = """
          --accent:        #6366f1;
          --accent-hover:  #4f46e5;
          --accent-subtle: rgba(99,102,241,0.12);
          --accent-border: rgba(99,102,241,0.30);
          --accent-text:   #a5b4fc;
          --surface-1:     rgba(255,255,255,0.03);
          --surface-2:     rgba(255,255,255,0.06);
          --border:        rgba(255,255,255,0.08);
          --border-strong: rgba(255,255,255,0.16);
          --text-primary:  #f1f5f9;
          --text-secondary:#94a3b8;
          --text-muted:    #64748b;
          --sidebar-bg:    rgba(15,15,20,0.7);
        """
    else:
        color_vars = """
          --accent:        #4f46e5;
          --accent-hover:  #4338ca;
          --accent-subtle: rgba(79,70,229,0.08);
          --accent-border: rgba(79,70,229,0.28);
          --accent-text:   #4f46e5;
          --surface-1:     rgba(0,0,0,0.03);
          --surface-2:     rgba(0,0,0,0.055);
          --border:        rgba(0,0,0,0.09);
          --border-strong: rgba(0,0,0,0.16);
          --text-primary:  #0f172a;
          --text-secondary:#475569;
          --text-muted:    #94a3b8;
          --sidebar-bg:    rgba(248,248,252,0.9);
        """

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Design Tokens ─────────────────────────────────────────── */
    :root {{
      {color_vars}
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 20px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
      --shadow-md: 0 4px 16px rgba(0,0,0,0.18);
      --shadow-lg: 0 8px 32px rgba(0,0,0,0.25);
      --transition: all 0.18s cubic-bezier(0.4,0,0.2,1);
    }}

    /* ── Global Typography ──────────────────────────────────────── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* ── Sidebar ────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
      border-right: 1px solid var(--border) !important;
    }}
    [data-testid="stSidebarNav"] {{
      background: transparent !important;
    }}

    /* ── Global Buttons ─────────────────────────────────────────── */
    .stButton > button {{
      border-radius: var(--radius-sm) !important;
      transition: var(--transition) !important;
      height: 38px !important;
      font-weight: 500 !important;
      font-family: 'Inter', sans-serif !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      font-size: 0.875rem !important;
    }}
    .stButton > button:hover {{
      transform: translateY(-1px) !important;
      box-shadow: var(--shadow-md) !important;
    }}

    /* ── Tabs ───────────────────────────────────────────────────── */
    [data-testid="stTabs"] [role="tablist"] {{
      gap: 4px;
      border-bottom: 1px solid var(--border);
    }}
    [data-testid="stTabs"] button[role="tab"] {{
      background: transparent !important;
      border: none !important;
      font-weight: 500 !important;
      font-size: 0.875rem !important;
      padding: 8px 16px !important;
      border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
      transition: var(--transition) !important;
    }}

    /* ── File History Items ──────────────────────────────────────── */
    .history-file-item {{
      background: var(--surface-1);
      border: 1px solid var(--border);
      padding: 10px 12px;
      border-radius: var(--radius-sm);
      margin-bottom: 6px;
      transition: var(--transition);
      font-size: 0.8rem;
      color: var(--text-primary);
      word-break: break-all;
    }}
    .history-file-item:hover {{
      background: var(--surface-2);
      border-color: var(--border-strong);
    }}
    .history-file-item-time {{
      font-size: 0.7rem;
      color: var(--text-muted);
      display: block;
      margin-top: 2px;
    }}

    /* ── Selectbox & Widgets ─────────────────────────────────────── */
    div[data-baseweb="select"] {{
      border-radius: var(--radius-sm) !important;
    }}

    /* ── Hide Streamlit chrome ───────────────────────────────────── */
    #MainMenu, footer, header {{ visibility: hidden !important; }}

    /* ════════════════════════════════════════════════════════════
       UPLOAD HERO SECTION
    ════════════════════════════════════════════════════════════ */
    .hero-wrapper {{
      text-align: center;
      padding: 48px 24px 16px;
      max-width: 720px;
      margin: 0 auto;
    }}
    .hero-title {{
      font-size: 2rem;
      font-weight: 700;
      color: var(--text-primary);
      letter-spacing: -0.5px;
      margin: 0 0 8px;
      line-height: 1.2;
    }}
    .hero-subtitle {{
      font-size: 1rem;
      color: var(--text-secondary);
      margin: 0 0 40px;
      font-weight: 400;
    }}
    .category-prompt-label {{
      font-size: 0.7rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 12px;
      text-align: center;
    }}

    /* ── Category Card Buttons ───────────────────────────────────── */
    .category-btn-row .stButton > button {{
      height: 80px !important;
      flex-direction: column !important;
      gap: 6px !important;
      background: var(--surface-1) !important;
      border: 1px solid var(--border) !important;
      border-radius: var(--radius-md) !important;
      color: var(--text-secondary) !important;
      transition: var(--transition) !important;
    }}
    .category-btn-row .stButton > button:hover {{
      background: var(--surface-2) !important;
      border-color: var(--border-strong) !important;
      color: var(--text-primary) !important;
      transform: translateY(-2px) !important;
      box-shadow: var(--shadow-md) !important;
    }}
    .category-btn-row .stButton > button[kind="primary"] {{
      background: var(--accent-subtle) !important;
      border-color: var(--accent-border) !important;
      color: var(--accent-text) !important;
    }}

    /* ── Format Pills ────────────────────────────────────────────── */
    .format-pills-container {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      justify-content: center;
      margin: 14px auto 24px;
      animation: fadeInUp 0.18s ease;
      max-width: 600px;
    }}
    .format-pill {{
      background: var(--accent-subtle);
      border: 1px solid var(--accent-border);
      color: var(--accent-text);
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      display: inline-block;
    }}

    /* ── Uploader dropzone overrides ─────────────────────────────── */
    .upload-dropzone-wrapper [data-testid="stFileUploadDropzone"] {{
      border: 2px dashed var(--accent-border) !important;
      border-radius: var(--radius-lg) !important;
      background: var(--accent-subtle) !important;
      padding: 2.5rem !important;
      transition: var(--transition) !important;
    }}
    .upload-dropzone-wrapper [data-testid="stFileUploadDropzone"]:hover {{
      border-color: var(--accent) !important;
    }}
    .upload-dropzone-wrapper [data-testid="stFileUploadDropzone"] > div > div > p {{
      font-size: 0 !important;
      color: transparent !important;
      line-height: 0 !important;
    }}
    .upload-dropzone-wrapper [data-testid="stFileUploadDropzone"] > div > div > p::before {{
      content: "Drag & drop or click to browse";
      font-size: 0.95rem !important;
      color: var(--text-primary) !important;
      font-family: 'Inter', sans-serif !important;
      font-weight: 500 !important;
      line-height: 1.5 !important;
      display: block;
    }}
    .upload-dropzone-wrapper [data-testid="stFileUploadDropzone"] small {{ font-size: 0 !important; }}
    .upload-dropzone-wrapper [data-testid="stFileUploadDropzone"] small::before {{
      content: "";
      font-size: 0 !important;
    }}

    /* ── Upload limit badge ──────────────────────────────────────── */
    .upload-limit-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 0.7rem;
      font-weight: 500;
      padding: 2px 10px;
      border-radius: 20px;
      margin-top: 10px;
    }}

    /* ════════════════════════════════════════════════════════════
       FILE INFO CARD (after upload)
    ════════════════════════════════════════════════════════════ */
    .file-info-card {{
      display: flex;
      align-items: center;
      gap: 16px;
      background: var(--accent-subtle);
      border: 1px solid var(--accent-border);
      border-radius: var(--radius-lg);
      padding: 14px 20px;
      margin-bottom: 8px;
      animation: fadeInUp 0.2s ease;
    }}
    .file-icon-wrap {{ font-size: 2.2rem; line-height: 1; flex-shrink: 0; }}
    .file-info-body {{ flex: 1; min-width: 0; }}
    .file-info-name {{
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-primary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 340px;
      margin: 0 0 6px;
    }}
    .file-meta-row {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
    .file-badge {{
      background: var(--accent-subtle);
      border: 1px solid var(--accent-border);
      color: var(--accent-text);
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 2px 9px;
      border-radius: 20px;
    }}
    .file-size-badge {{
      background: var(--surface-2);
      border: 1px solid var(--border);
      color: var(--text-secondary);
      font-size: 0.7rem;
      font-weight: 500;
      padding: 2px 9px;
      border-radius: 20px;
    }}

    /* ════════════════════════════════════════════════════════════
       CONVERT FORMAT GRID
    ════════════════════════════════════════════════════════════ */
    .convert-target-label {{
      font-size: 0.7rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin: 20px 0 12px;
    }}
    .format-grid-row .stButton > button {{
      height: 60px !important;
      flex-direction: column !important;
      font-size: 0.8rem !important;
      font-weight: 600 !important;
      letter-spacing: 0.04em !important;
      background: var(--surface-1) !important;
      border: 1px solid var(--border) !important;
      border-radius: var(--radius-md) !important;
      color: var(--text-secondary) !important;
      transition: var(--transition) !important;
      text-transform: uppercase !important;
    }}
    .format-grid-row .stButton > button:hover {{
      background: var(--surface-2) !important;
      border-color: var(--border-strong) !important;
      color: var(--text-primary) !important;
      transform: translateY(-2px) !important;
    }}
    .format-grid-row .stButton > button[kind="primary"] {{
      background: var(--accent-subtle) !important;
      border-color: var(--accent) !important;
      color: var(--accent-text) !important;
    }}

    /* ── Convert action bar ──────────────────────────────────────── */
    .selected-format-hint {{
      font-size: 0.82rem;
      color: var(--text-secondary);
      margin: 12px 0 8px;
      display: block;
    }}
    .selected-format-hint strong {{ color: var(--accent-text); }}

    /* ════════════════════════════════════════════════════════════
       SETTINGS PAGE
    ════════════════════════════════════════════════════════════ */

    /* Section header: icon + title + thin underline */
    .settings-section-header {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border);
      margin-top: 28px;
      margin-bottom: 16px;
    }}
    .settings-section-icon {{
      font-size: 1rem;
      width: 28px;
      height: 28px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      flex-shrink: 0;
    }}
    .settings-section-title {{
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-primary);
      margin: 0;
      letter-spacing: -0.1px;
    }}

    /* Settings field label + desc */
    .settings-field-label {{
      font-size: 0.875rem;
      font-weight: 600;
      color: var(--text-primary);
      margin: 0 0 3px;
    }}
    .settings-field-desc {{
      font-size: 0.78rem;
      color: var(--text-secondary);
      margin: 0;
      line-height: 1.4;
    }}

    /* Separator between settings rows */
    .settings-row {{
      padding: 14px 0;
      border-bottom: 1px solid var(--border);
    }}
    .settings-row:last-child {{
      border-bottom: none;
    }}

    /* ── Theme toggle cards ──────────────────────────────────────── */
    .theme-cards-row .stButton > button {{
      height: 68px !important;
      flex-direction: column !important;
      gap: 5px !important;
      font-size: 0.85rem !important;
      font-weight: 500 !important;
      background: var(--surface-1) !important;
      border: 1px solid var(--border) !important;
      border-radius: var(--radius-md) !important;
      color: var(--text-secondary) !important;
      transition: var(--transition) !important;
    }}
    .theme-cards-row .stButton > button:hover {{
      background: var(--surface-2) !important;
      border-color: var(--border-strong) !important;
      color: var(--text-primary) !important;
    }}
    .theme-cards-row .stButton > button[kind="primary"] {{
      background: var(--accent-subtle) !important;
      border-color: var(--accent) !important;
      color: var(--accent-text) !important;
    }}

    /* ── Quality label badge ─────────────────────────────────────── */
    .quality-badge-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 6px;
    }}
    .quality-label-badge {{
      display: inline-flex;
      align-items: center;
      background: var(--accent-subtle);
      border: 1px solid var(--accent-border);
      color: var(--accent-text);
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 3px 12px;
      border-radius: 20px;
    }}

    /* ── Animations ──────────────────────────────────────────────── */
    @keyframes fadeInUp {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to   {{ opacity: 1; }}
    }}

    /* ── Empty state ─────────────────────────────────────────────── */
    .empty-state-box {{
      text-align: center;
      padding: 60px 20px;
      border: 1px dashed var(--border);
      border-radius: var(--radius-xl);
      margin-top: 24px;
      animation: fadeIn 0.2s ease;
    }}
    .empty-state-box h3 {{
      color: var(--text-primary);
      margin-bottom: 8px;
      font-weight: 600;
      font-size: 1.1rem;
    }}
    .empty-state-box p {{
      color: var(--text-secondary);
      font-size: 0.875rem;
    }}

    /* ════════════════════════════════════════════════════════════
       AI ACTION CARDS — button pinned to bottom
       All 3 cards have height=220 set by Streamlit (Python).
       We target the border-wrapper directly — no marker needed.
       Use a data attribute we add via Python to scope only AI cards.
    ════════════════════════════════════════════════════════════ */

    .ai-card-anchor      {{ display: none; }}
    .ai-cards-row-marker {{ display: none; }}

    /* Scope: only border-wrappers that are inside .ai-action-section */
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] {{
      position: relative !important;
    }}

    /* The div Streamlit adds for height= has overflow:auto — reset it */
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] > div {{
      overflow: visible !important;
    }}

    /* Button: pinned absolutely to bottom of card */
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] .stButton {{
      position: absolute !important;
      bottom: 14px !important;
      left: 14px !important;
      right: 14px !important;
      margin: 0 !important;
    }}
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {{
      width: 100% !important;
      background: transparent !important;
      border: 1px solid var(--border-strong) !important;
      border-radius: 8px !important;
      padding: 10px 16px !important;
      color: var(--text-primary) !important;
      font-size: 0.85rem !important;
      font-weight: 500 !important;
      height: auto !important;
      transition: var(--transition) !important;
    }}
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {{
      background: var(--surface-2) !important;
      border-color: var(--accent) !important;
      color: var(--accent-text) !important;
    }}

    /* Radio options inside AI cards */
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] .stRadio > div {{
      gap: 8px !important;
      margin: 6px 0 0 !important;
    }}
    .ai-action-section [data-testid="stVerticalBlockBorderWrapper"] .stRadio label {{
      font-size: 0.82rem !important;
      color: var(--text-secondary) !important;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
