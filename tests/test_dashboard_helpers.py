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

# docx2pdf modülü yüklü olmayabilir (bilinen eksik bağımlılık).
# converter.py import'unu kırmamak için test başlamadan önce mock enjekte ediyoruz.
if "docx2pdf" not in sys.modules:
    sys.modules["docx2pdf"] = MagicMock()

from ui.dashboard import Dashboard, _FORMAT_MAP


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
