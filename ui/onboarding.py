import streamlit as st
from config.settings import Config

def show_onboarding(texts: dict):
    """
    Kullanıcıya uygulamayı tanıtan ilk açılış ekranını gösterir.
    """
    st.markdown("""
        <style>
            .onboarding-card {
                background-color: var(--bg-surface);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 24px;
                height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                transition: border-color 0.2s ease;
            }
            .onboarding-card:hover {
                border-color: var(--accent);
            }
            .onboarding-num {
                font-size: 24px;
                font-weight: 700;
                color: var(--accent);
                margin-bottom: 12px;
            }
            .onboarding-text {
                color: var(--text-primary);
                font-size: 14px;
                line-height: 1.5;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader(texts.get("onboarding_title", "Welcome"))
        st.write("")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""<div class="onboarding-card"><div class="onboarding-num">01</div><div class="onboarding-text">{texts.get("onboarding_step_1", "")}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="onboarding-card"><div class="onboarding-num">02</div><div class="onboarding-text">{texts.get("onboarding_step_2", "")}</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="onboarding-card"><div class="onboarding-num">03</div><div class="onboarding-text">{texts.get("onboarding_step_3", "")}</div></div>""", unsafe_allow_html=True)
            
        st.write("")
        st.write("")
        if st.button(texts.get("onboarding_dismiss", "Got it"), type="primary", use_container_width=True):
            st.session_state.onboarding_seen = True
            
            # Tercihleri kaydet
            prefs = Config.load_user_prefs()
            prefs["onboarding_seen"] = True
            Config.save_user_prefs(prefs)
            st.rerun()
