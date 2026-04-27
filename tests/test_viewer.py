"""
tests/test_viewer.py — FileViewer.display_image ve _dispatch_viewer testleri
Issue #13 — Abdulkadir Sar (Aksar712)

Kapsam:
  - display_image başarılı senaryo (st.image çağrısını doğrular)
  - display_image eksik dosya senaryosu (exception fırlatmaz)
  - _dispatch_viewer görsel uzantısını doğru metoda yönlendirir
  - _dispatch_viewer desteklenmeyen uzantı için st.warning çağrısı
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
