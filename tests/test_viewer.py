"""
tests/test_viewer.py — FileViewer display_* metotları ve _dispatch_viewer testleri
Issue #13 + Issue #8 — Abdulkadir Sar (Aksar712)

Kapsam:
  - display_image başarılı senaryo (st.image çağrısını doğrular)
  - display_image eksik dosya senaryosu (exception fırlatmaz)
  - display_text_document: .txt, .py (kod), .docx başarı ve hata senaryoları
  - _dispatch_viewer: görsel, ses, metin ve desteklenmeyen uzantı yönlendirmeleri
"""

import sys
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# PyMuPDF (fitz) yoksa modül seviyesinde stub ekle — CI/lokal uyumluluğu için
# ---------------------------------------------------------------------------
if "fitz" not in sys.modules:
    fitz_stub = MagicMock()
    sys.modules["fitz"] = fitz_stub

# ---------------------------------------------------------------------------
# Yardımcı: tek piksellik minimum PNG bayt dizisi
# ---------------------------------------------------------------------------
MINIMAL_PNG = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx"
    b"\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00"
    b"\x00\x00\x00IEND\xaeB`\x82"
)


# ===========================================================================
# display_image testleri
# ===========================================================================

class TestDisplayImage:
    """FileViewer.display_image metodu için testler."""

    def test_display_image_calls_st_image_success(self, tmp_path: Path):
        """Başarılı senaryo: gerçek PNG dosyası ile st.image çağrısını doğrular."""
        from core.viewer import FileViewer

        img_file = tmp_path / "test.png"
        img_file.write_bytes(MINIMAL_PNG)

        fv = FileViewer()
        with patch("core.viewer.st.image") as mock_st_image:
            fv.display_image(str(img_file))
            mock_st_image.assert_called_once_with(str(img_file), use_container_width=True)

    def test_display_image_missing_file_does_not_raise(self, tmp_path: Path):
        """Hata senaryosu: eksik dosya exception fırlatmamalı; st.error çağrılmalı."""
        from core.viewer import FileViewer

        missing = str(tmp_path / "nonexistent.png")
        fv = FileViewer()

        with (
            patch("core.viewer.st.image", side_effect=FileNotFoundError("Dosya yok")),
            patch("core.viewer.st.error") as mock_error,
        ):
            # Exception fırlatmamalı
            fv.display_image(missing)
            assert mock_error.called, "Hata durumunda st.error çağrılmalıydı."


# ===========================================================================
# _dispatch_viewer testleri (Dashboard üzerinde)
# ===========================================================================

class TestDispatchViewer:
    """Dashboard._dispatch_viewer için testler."""

    def _make_uploaded_file(self, name: str, content: bytes = b"dummy"):
        """Sahte bir Streamlit UploadedFile nesnesi üretir."""
        mock_file = MagicMock()
        mock_file.name = name
        mock_file.getbuffer.return_value = content
        return mock_file

    def test_dispatch_viewer_routes_image_to_display_image(self, tmp_path: Path):
        """Başarılı senaryo: .png uzantısı display_image'e yönlendirilmeli."""
        from ui.dashboard import Dashboard

        texts = {}
        dash = Dashboard(texts)

        uploaded = self._make_uploaded_file("photo.png", MINIMAL_PNG)
        fake_path = str(tmp_path / "photo.png")

        mock_fv = MagicMock()
        mock_fv_class = MagicMock(return_value=mock_fv)

        # FileViewer modül seviyesinde import edildiği için ui.dashboard.FileViewer
        # ile patch edilebilir
        with (
            patch.object(Dashboard, "_save_upload_to_temp", return_value=fake_path),
            patch("ui.dashboard.FileViewer", mock_fv_class),
            patch("pathlib.Path.unlink"),
        ):
            dash._dispatch_viewer(uploaded)

        mock_fv.display_image.assert_called_once_with(fake_path)


    def test_dispatch_viewer_unsupported_ext_shows_warning(self, tmp_path: Path):
        """Hata senaryosu: desteklenmeyen uzantı için st.warning çağrılmalı."""
        from ui.dashboard import Dashboard

        texts = {"error_unsupported_file": "Desteklenmeyen dosya türü."}
        dash = Dashboard(texts)

        uploaded = self._make_uploaded_file("archive.zip", b"PK")
        fake_path = str(tmp_path / "archive.zip")

        mock_fv = MagicMock()
        mock_fv_class = MagicMock(return_value=mock_fv)

        with (
            patch.object(Dashboard, "_save_upload_to_temp", return_value=fake_path),
            patch("ui.dashboard.FileViewer", mock_fv_class),
            patch("streamlit.warning") as mock_warning,
            patch("pathlib.Path.unlink"),
        ):
            dash._dispatch_viewer(uploaded)

        mock_warning.assert_called_once()
        # Uyarı mesajı i18n'den gelmeli
        assert "Desteklenmeyen" in mock_warning.call_args[0][0]

    def test_dispatch_viewer_routes_audio_to_display_audio(self, tmp_path: Path):
        """Başarılı senaryo: .mp3 uzantısı display_audio'ya yönlendirilmeli."""
        from ui.dashboard import Dashboard

        texts = {}
        dash = Dashboard(texts)
        uploaded = self._make_uploaded_file("song.mp3", b"\xff\xfb")
        fake_path = str(tmp_path / "song.mp3")

        mock_fv = MagicMock()
        mock_fv_class = MagicMock(return_value=mock_fv)

        with (
            patch.object(Dashboard, "_save_upload_to_temp", return_value=fake_path),
            patch("ui.dashboard.FileViewer", mock_fv_class),
            patch("pathlib.Path.unlink"),
        ):
            dash._dispatch_viewer(uploaded)

        assert mock_fv.display_audio.called, "display_audio çağrılmalıydı."

    def test_dispatch_viewer_routes_docx_to_display_text(self, tmp_path: Path):
        """Başarılı senaryo: .docx uzantısı display_text_document'a yönlendirilmeli."""
        from ui.dashboard import Dashboard

        texts = {}
        dash = Dashboard(texts)
        uploaded = self._make_uploaded_file("report.docx", b"PK")
        fake_path = str(tmp_path / "report.docx")

        mock_fv = MagicMock()
        mock_fv_class = MagicMock(return_value=mock_fv)

        with (
            patch.object(Dashboard, "_save_upload_to_temp", return_value=fake_path),
            patch("ui.dashboard.FileViewer", mock_fv_class),
            patch("pathlib.Path.unlink"),
            patch("streamlit.spinner", return_value=MagicMock(__enter__=lambda s: s, __exit__=MagicMock(return_value=False))),
        ):
            dash._dispatch_viewer(uploaded)

        assert mock_fv.display_text_document.called, "display_text_document çağrılmalıydı."


# ===========================================================================
# display_text_document testleri (Issue #8)
# ===========================================================================

class TestDisplayTextDocument:
    """FileViewer.display_text_document genişletilmiş davranışı için testler."""

    def test_display_txt_file_success(self, tmp_path: Path):
        """Başarılı senaryo: .txt dosyası st.text_area ile gösterilmeli."""
        from core.viewer import FileViewer

        txt_file = tmp_path / "notes.txt"
        txt_file.write_text("Merhaba Dünya", encoding="utf-8")

        fv = FileViewer()
        with patch("core.viewer.st.text_area") as mock_area:
            fv.display_text_document(str(txt_file))
            assert mock_area.called, "st.text_area çağrılmalıydı."
            # İçerik doğru geçirilmeli
            assert "Merhaba Dünya" in mock_area.call_args[0][1]

    def test_display_python_file_uses_st_code(self, tmp_path: Path):
        """Başarılı senaryo: .py dosyası st.code(language='python') ile gösterilmeli."""
        from core.viewer import FileViewer

        py_file = tmp_path / "script.py"
        py_file.write_text("print('hello')", encoding="utf-8")

        fv = FileViewer()
        with patch("core.viewer.st.code") as mock_code:
            fv.display_text_document(str(py_file))
            mock_code.assert_called_once_with("print('hello')", language="python")

    def test_display_text_document_read_error_does_not_raise(self, tmp_path: Path):
        """Hata senaryosu: okuma hatası exception fırlatmamalı; st.error çağrılmalı."""
        from core.viewer import FileViewer

        py_file = tmp_path / "broken.py"
        py_file.write_text("x = 1", encoding="utf-8")

        fv = FileViewer()
        with (
            patch("builtins.open", side_effect=PermissionError("Erişim reddedildi")),
            patch("core.viewer.st.error") as mock_error,
        ):
            fv.display_text_document(str(py_file))
            assert mock_error.called, "Hata durumunda st.error çağrılmalıydı."
