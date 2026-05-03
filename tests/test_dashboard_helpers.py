"""
tests/test_dashboard_helpers.py — Dashboard yardımcı metotlarının birim testleri
Ekleme: Issue #11 — Galip Efe Öncü

_save_upload_to_temp ve _dispatch_conversion yardımcılarının
doğru çalıştığını doğrular.
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

# docx2pdf modülü yüklü olmayabilir (bilinen eksik bağımlılık).
# converter.py import'unu kırmamak için test başlamadan önce mock enjekte ediyoruz.
if "docx2pdf" not in sys.modules:
    sys.modules["docx2pdf"] = MagicMock()

from ui.dashboard import Dashboard, _FORMAT_MAP


# ---------------------------------------------------------------------------
# _add_to_file_history ve bildirim helper testleri
# ---------------------------------------------------------------------------

def test_add_to_file_history_deduplicates_and_appends_latest(monkeypatch):
    """Ayni dosya tekrar eklenince eski kayit silinip sona eklenmeli."""
    class FakeSessionState(SimpleNamespace):
        def __contains__(self, key):
            return hasattr(self, key)

    fake_session_state = FakeSessionState(
        file_history=[
            {"name": "old.txt", "time": "10:00:00", "date": "28.04.2026"},
            {"name": "keep.txt", "time": "10:01:00", "date": "28.04.2026"},
        ]
    )
    monkeypatch.setattr("ui.dashboard.st.session_state", fake_session_state)

    Dashboard({})._add_to_file_history("old.txt")

    assert [item["name"] for item in fake_session_state.file_history] == ["keep.txt", "old.txt"]


def test_notify_helpers_call_streamlit_feedback(monkeypatch):
    """Basari ve hata helper'lari ilgili Streamlit API'lerini cagirmali."""
    calls = {"toast": [], "success": [], "error": []}
    monkeypatch.setattr("ui.dashboard.st.toast", calls["toast"].append)
    monkeypatch.setattr("ui.dashboard.st.success", calls["success"].append)
    monkeypatch.setattr("ui.dashboard.st.error", lambda message, icon=None: calls["error"].append((message, icon)))

    Dashboard.notify_success("tamam")
    Dashboard.notify_error("problem")

    assert calls["toast"] == ["✅ tamam"]
    assert calls["success"] == ["tamam"]
    assert calls["error"] == [("problem", "🚨")]


# ---------------------------------------------------------------------------
# render_main_area testleri
# ---------------------------------------------------------------------------

def test_render_main_area_without_uploaded_file_shows_guidance(monkeypatch):
    """Dosya yokken tum sekmeler kullaniciya yukleme yonlendirmesi gostermeli."""
    class FakeSessionState(SimpleNamespace):
        def get(self, key, default=None):
            return getattr(self, key, default)

    class DummyTab:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    fake_session_state = FakeSessionState(active_tab="Dönüştür", uploaded_file=None)
    warnings = []
    infos = []
    headers = []

    monkeypatch.setattr("ui.dashboard.st.session_state", fake_session_state)
    monkeypatch.setattr("ui.dashboard.st.tabs", lambda names: [DummyTab(), DummyTab(), DummyTab()])
    monkeypatch.setattr("ui.dashboard.st.header", headers.append)
    monkeypatch.setattr("ui.dashboard.st.warning", lambda message, icon=None: warnings.append((message, icon)))
    monkeypatch.setattr("ui.dashboard.st.info", lambda message, icon=None: infos.append((message, icon)))

    Dashboard({"convert_tab": "Dönüştür", "view_tab": "Görüntüle", "ai_tab": "AI"}).render_main_area()

    assert headers == ["🔄 Dönüştür", "👁️ Görüntüle", "🤖 AI"]
    assert warnings == [("Lütfen önce yan menüden bir dosya yükleyin.", "⚠️")]
    assert infos == [
        ("Lütfen önce yan menüden bir dosya yükleyin.", "ℹ️"),
        ("Lütfen önce yan menüden bir dosya yükleyin.", "ℹ️"),
    ]


def test_render_main_area_with_unsupported_file_warns_conversion_unavailable(monkeypatch):
    """Desteklenmeyen uzantida convert sekmesi uygun uyariyi gostermeli."""
    class FakeSessionState(SimpleNamespace):
        def get(self, key, default=None):
            return getattr(self, key, default)

    class DummyTab:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    uploaded_file = MagicMock()
    uploaded_file.name = "notes.xyz"
    uploaded_file.getbuffer.return_value = b"fake content"
    fake_session_state = FakeSessionState(active_tab="Dönüştür", uploaded_file=uploaded_file)
    warnings = []
    infos = []
    writes = []

    monkeypatch.setattr("ui.dashboard.st.session_state", fake_session_state)
    monkeypatch.setattr("ui.dashboard.st.tabs", lambda names: [DummyTab(), DummyTab(), DummyTab()])
    monkeypatch.setattr("ui.dashboard.st.header", lambda _message: None)
    monkeypatch.setattr("ui.dashboard.st.write", writes.append)
    monkeypatch.setattr("ui.dashboard.st.warning", lambda message, icon=None: warnings.append((message, icon)))
    monkeypatch.setattr("ui.dashboard.st.info", lambda message, icon=None: infos.append((message, icon)))

    Dashboard({"convert_tab": "Dönüştür", "view_tab": "Görüntüle", "ai_tab": "AI"}).render_main_area()

    assert any("notes.xyz" in message for message in writes)
    assert warnings == [
        ("Bu dosya türü için dönüştürme desteği bulunmuyor.", None),
        ("Desteklenmeyen dosya türü.", "⚠️")
    ]
    assert infos == [
        ("Görüntüleme modülü yükleniyor...", "ℹ️"),
        ("AI analiz modülü yükleniyor...", "ℹ️"),
        ("Bu dosya türü AI analizini desteklemiyor. Lütfen PDF, DOCX, TXT veya CSV yükleyin.", "ℹ️"),
    ]


# ---------------------------------------------------------------------------
# _save_upload_to_temp testleri
# ---------------------------------------------------------------------------

def test_save_upload_to_temp_creates_file(tmp_path, monkeypatch):
    """Yüklenen dosya temp/ altına doğru yazılmalı."""
    monkeypatch.chdir(tmp_path)

    mock_file = MagicMock()
    mock_file.name = "test_document.pdf"
    mock_file.getbuffer.return_value = b"%PDF-1.4 fake content"

    result = Dashboard._save_upload_to_temp(mock_file)

    assert os.path.exists(result)
    assert result == os.path.join("temp", "test_document.pdf")
    with open(result, "rb") as f:
        assert f.read() == b"%PDF-1.4 fake content"


def test_save_upload_to_temp_overwrites_existing(tmp_path, monkeypatch):
    """Aynı isimli dosya varsa üzerine yazmalı."""
    monkeypatch.chdir(tmp_path)
    os.makedirs("temp", exist_ok=True)
    existing = os.path.join("temp", "existing.txt")
    with open(existing, "w") as f:
        f.write("old content")

    mock_file = MagicMock()
    mock_file.name = "existing.txt"
    mock_file.getbuffer.return_value = b"new content"

    result = Dashboard._save_upload_to_temp(mock_file)
    with open(result, "rb") as f:
        assert f.read() == b"new content"


# ---------------------------------------------------------------------------
# _dispatch_conversion testleri
# ---------------------------------------------------------------------------

def test_dispatch_conversion_csv_to_xlsx_success(tmp_path):
    """CSV -> XLSX dönüşümü başarıyla tamamlanmalı."""
    src = tmp_path / "data.csv"
    src.write_text("col_a,col_b\n1,2\n3,4\n", encoding="utf-8")
    dst = tmp_path / "data.xlsx"

    result = Dashboard._dispatch_conversion(
        str(src), ".csv", "xlsx", str(dst)
    )
    assert result is True
    assert dst.exists()


def test_dispatch_conversion_missing_file_returns_false(tmp_path):
    """Var olmayan girdi dosyasında False dönmeli, crash olmamalı."""
    result = Dashboard._dispatch_conversion(
        str(tmp_path / "nonexistent.csv"), ".csv", "xlsx",
        str(tmp_path / "out.xlsx")
    )
    assert result is False


def test_dispatch_conversion_unsupported_pair_returns_false(tmp_path):
    """Desteklenmeyen kaynak-hedef çifti False dönmeli."""
    src = tmp_path / "file.xyz"
    src.write_text("dummy", encoding="utf-8")
    result = Dashboard._dispatch_conversion(
        str(src), ".xyz", "abc", str(tmp_path / "out.abc")
    )
    assert result is False


# ---------------------------------------------------------------------------
# _FORMAT_MAP testleri
# ---------------------------------------------------------------------------

def test_format_map_pdf_has_docx():
    """PDF uzantısı için docx hedef formatı olmalı."""
    assert "docx" in _FORMAT_MAP[".pdf"]


def test_format_map_csv_has_xlsx():
    """CSV uzantısı için xlsx hedef formatı olmalı."""
    assert "xlsx" in _FORMAT_MAP[".csv"]


def test_format_map_image_targets():
    """Görsel uzantıları için en az 2 hedef format olmalı."""
    for ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
        assert len(_FORMAT_MAP[ext]) >= 2, f"{ext} için yetersiz hedef format"


def test_format_map_audio_targets():
    """Ses uzantıları için en az 2 hedef format olmalı."""
    for ext in [".mp3", ".wav", ".ogg", ".flac"]:
        assert len(_FORMAT_MAP[ext]) >= 2, f"{ext} için yetersiz hedef format"
