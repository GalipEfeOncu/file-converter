"""
tests/test_converter.py — FileConverter birim testleri

Issue #10 kapsaminda DOCX -> PDF ve gorsel donusum akislari icin
basari ve hata senaryolarini dogrular.
"""

from pathlib import Path
import sys
from unittest.mock import MagicMock

from docx import Document
from PIL import Image


if "docx2pdf" not in sys.modules:
    mock_docx2pdf = MagicMock()
    mock_docx2pdf.convert = MagicMock()
    sys.modules["docx2pdf"] = mock_docx2pdf

from core import converter as converter_module

FileConverter = converter_module.FileConverter


def test_convert_image_rgba_png_to_jpg_success(tmp_path: Path):
    """RGBA PNG girdisi JPG cikisina basariyla donusmeli."""
    source = tmp_path / "input.png"
    output = tmp_path / "output.jpg"

    Image.new("RGBA", (32, 32), color=(255, 0, 0, 128)).save(source, format="PNG")

    result = FileConverter().convert_image(str(source), str(output), "jpg", quality=85)

    assert result is True
    assert output.exists()

    with Image.open(output) as converted:
        assert converted.format == "JPEG"
        assert converted.mode == "RGB"


def test_convert_image_missing_file_returns_false(tmp_path: Path):
    """Olmayan girdi gorseli icin False donmeli."""
    result = FileConverter().convert_image(
        str(tmp_path / "missing.png"),
        str(tmp_path / "output.webp"),
        "webp",
    )

    assert result is False


def test_convert_docx_to_pdf_success(tmp_path: Path, monkeypatch):
    """docx2pdf cagrisi basariliysa True donmeli ve cikti dosyasi olusmali."""
    source = tmp_path / "input.docx"
    output = tmp_path / "output.pdf"

    document = Document()
    document.add_paragraph("Donusturme testi")
    document.save(source)

    def fake_convert(input_path: str, output_path: str) -> None:
        assert input_path == str(source)
        Path(output_path).write_bytes(b"%PDF-1.4 fake pdf")

    monkeypatch.setattr(converter_module, "docx2pdf_convert", fake_convert)

    result = FileConverter().convert_docx_to_pdf(str(source), str(output))

    assert result is True
    assert output.exists()
    assert output.read_bytes().startswith(b"%PDF")


def test_convert_docx_to_pdf_failure_returns_false(tmp_path: Path, monkeypatch):
    """docx2pdf hata verirse metot exception yaymadan False donmeli."""
    source = tmp_path / "input.docx"
    output = tmp_path / "output.pdf"

    document = Document()
    document.add_paragraph("Basarisiz donusum testi")
    document.save(source)

    def fake_convert(_input_path: str, _output_path: str) -> None:
        raise RuntimeError("MS Word bulunamadi")

    monkeypatch.setattr(converter_module, "docx2pdf_convert", fake_convert)

    result = FileConverter().convert_docx_to_pdf(str(source), str(output))

    assert result is False
    assert not output.exists()
