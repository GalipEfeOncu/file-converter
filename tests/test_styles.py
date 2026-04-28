"""
tests/test_styles.py - apply_custom_css birim testleri

CSS enjeksiyonunun tema secimine gore dogru calistigini dogrular.
"""

from ui import styles as styles_module


def test_apply_custom_css_injects_dark_theme_once(monkeypatch):
    """Dark theme varsayilaninda tek CSS blogu enjekte edilmeli."""
    markdown_calls = []
    monkeypatch.setattr(styles_module.st, "markdown", lambda content, unsafe_allow_html=True: markdown_calls.append(content))
    monkeypatch.setattr(styles_module.st, "session_state", {}, raising=False)

    styles_module.apply_custom_css()

    assert len(markdown_calls) == 1
    assert "--bg-base: #0b1220;" in markdown_calls[0]


def test_apply_custom_css_injects_light_theme_when_requested(monkeypatch):
    """Light theme icin temel ve light override CSS blogu enjekte edilmeli."""
    markdown_calls = []
    monkeypatch.setattr(styles_module.st, "markdown", lambda content, unsafe_allow_html=True: markdown_calls.append(content))
    monkeypatch.setattr(styles_module.st, "session_state", {}, raising=False)

    styles_module.apply_custom_css(theme="light")

    assert len(markdown_calls) == 2
    assert "--bg-base: #0b1220;" in markdown_calls[0]
    assert "--bg-base: #f7f9fc;" in markdown_calls[1]


def test_apply_custom_css_prefers_session_state_theme(monkeypatch):
    """Session state'te tema varsa parametreyi override etmeli."""
    markdown_calls = []

    class FakeSessionState:
        theme = "light"

        def __contains__(self, key):
            return key == "theme"

    monkeypatch.setattr(styles_module.st, "markdown", lambda content, unsafe_allow_html=True: markdown_calls.append(content))
    monkeypatch.setattr(styles_module.st, "session_state", FakeSessionState(), raising=False)

    styles_module.apply_custom_css(theme="dark")

    assert len(markdown_calls) == 2


def test_apply_custom_css_ignores_session_state_access_errors(monkeypatch):
    """Session state erisimindeki hata CSS enjeksiyonunu engellememeli."""
    markdown_calls = []

    class BrokenSessionState:
        def __contains__(self, _key):
            raise RuntimeError("session state unavailable")

    monkeypatch.setattr(styles_module.st, "markdown", lambda content, unsafe_allow_html=True: markdown_calls.append(content))
    monkeypatch.setattr(styles_module.st, "session_state", BrokenSessionState(), raising=False)

    styles_module.apply_custom_css(theme="dark")

    assert len(markdown_calls) == 1
