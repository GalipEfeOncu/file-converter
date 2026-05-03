import pytest
from unittest.mock import MagicMock, patch
from ui.onboarding import show_onboarding
from config.settings import Config

def test_onboarding_shows_on_first_run(monkeypatch):
    """prefs.get("onboarding_seen", False) False dönerse onboarding gösterilmeli."""
    # st.session_state'e onboarding_seen ekle
    import streamlit as st
    st.session_state.onboarding_seen = False
    
    # st bileşenlerini mockla
    with patch("ui.onboarding.st.container") as mock_container, \
         patch("ui.onboarding.st.columns") as mock_cols, \
         patch("ui.onboarding.st.button", return_value=False):
        
        mock_cols.return_value = [MagicMock(), MagicMock(), MagicMock()]
        show_onboarding({"onboarding_step_1": "Step 1"})
        
        assert mock_container.called
        assert mock_cols.called

def test_onboarding_dismissed(monkeypatch):
    """Dismiss butonuna basılınca onboarding_seen True olmalı ve Config.save_user_prefs çağrılmalı."""
    import streamlit as st
    st.session_state.onboarding_seen = False
    
    mock_prefs = {"onboarding_seen": False}
    
    with patch("ui.onboarding.st.container"), \
         patch("ui.onboarding.st.columns", return_value=[MagicMock(), MagicMock(), MagicMock()]), \
         patch("ui.onboarding.st.button", return_value=True), \
         patch("ui.onboarding.st.rerun"), \
         patch("config.settings.Config.load_user_prefs", return_value=mock_prefs), \
         patch("config.settings.Config.save_user_prefs") as mock_save:
        
        show_onboarding({})
        
        assert st.session_state.onboarding_seen is True
        mock_save.assert_called_once()
        # Kaydedilen tercihlerde onboarding_seen True olmalı
        saved_prefs = mock_save.call_args[0][0]
        assert saved_prefs["onboarding_seen"] is True

def test_onboarding_skipped_on_return():
    """main.py içinde onboarding_seen True ise show_onboarding çağrılmamalı (bu mantık main.py'dedir).
    Burada sadece onboarding_seen True iken show_onboarding'in bir yan etkisi olmadığını veya main.py mock testi yapabiliriz.
    Ancak talimat main.py'deki kontrolü test etmemizi istiyor gibi.
    """
    from main import main
    import streamlit as st
    
    # Session state'i hazırla
    st.session_state.onboarding_seen = True
    st.session_state.theme = "dark"
    st.session_state.language = "tr"
    st.session_state.active_tab = "convert"
    st.session_state.uploaded_file = None
        
    with patch("main.st.set_page_config"), \
         patch("main.init_state"), \
         patch("main.apply_custom_css"), \
         patch("main.load_languages", return_value={}), \
         patch("main.Dashboard"), \
         patch("main.show_onboarding") as mock_show:
        
        main()
        mock_show.assert_not_called()
