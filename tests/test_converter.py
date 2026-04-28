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


def test_convert_csv_to_xlsx_success(tmp_path: Path):
    """CSV girdisi XLSX cikisina basariyla donusmeli."""
    source = tmp_path / "input.csv"
    output = tmp_path / "output.xlsx"
    source.write_text("name,value\nalpha,1\nbeta,2\n", encoding="utf-8")

    result = FileConverter().convert_csv_to_xlsx(str(source), str(output))

    assert result is True
    assert output.exists()


def test_convert_csv_to_xlsx_empty_file_returns_false(tmp_path: Path):
    """Bos CSV dosyasi EmptyDataError uzerinden False donmeli."""
    source = tmp_path / "empty.csv"
    output = tmp_path / "output.xlsx"
    source.write_text("", encoding="utf-8")

    result = FileConverter().convert_csv_to_xlsx(str(source), str(output))

    assert result is False
    assert not output.exists()


def test_convert_xlsx_to_csv_success(tmp_path: Path):
    """XLSX girdisi CSV cikisina basariyla donusmeli."""
    source = tmp_path / "input.xlsx"
    output = tmp_path / "output.csv"
    import pandas as pd
    pd.DataFrame([{"col_a": 1, "col_b": 2}]).to_excel(source, index=False, engine="openpyxl")

    result = FileConverter().convert_xlsx_to_csv(str(source), str(output))

    assert result is True
    assert output.exists()
    assert "col_a,col_b" in output.read_text(encoding="utf-8")


def test_convert_xlsx_to_csv_missing_file_returns_false(tmp_path: Path):
    """Olmayan XLSX girdisi icin False donmeli."""
    result = FileConverter().convert_xlsx_to_csv(
        str(tmp_path / "missing.xlsx"),
        str(tmp_path / "output.csv"),
    )

    assert result is False


def test_convert_pdf_to_docx_success(tmp_path: Path, monkeypatch):
    """pdf2docx donusumu basariliysa True donmeli."""
    source = tmp_path / "input.pdf"
    output = tmp_path / "output.docx"
    source.write_bytes(b"%PDF-1.4 fake pdf")
    call_log = {"closed": False}

    class FakeConverter:
        def __init__(self, input_path: str):
            assert input_path == str(source)

        def convert(self, output_path: str, start: int = 0, end=None) -> None:
            assert output_path == str(output)
            assert start == 0
            assert end is None
            Path(output_path).write_bytes(b"fake docx bytes")

        def close(self) -> None:
            call_log["closed"] = True

    monkeypatch.setattr(converter_module, "Converter", FakeConverter)

    result = FileConverter().convert_pdf_to_docx(str(source), str(output))

    assert result is True
    assert output.exists()
    assert call_log["closed"] is True


def test_convert_pdf_to_docx_failure_returns_false(tmp_path: Path, monkeypatch):
    """pdf2docx tarafindaki hata exception yaymadan False donmeli."""
    source = tmp_path / "input.pdf"
    output = tmp_path / "output.docx"
    source.write_bytes(b"%PDF-1.4 fake pdf")

    class FakeConverter:
        def __init__(self, _input_path: str):
            pass

        def convert(self, _output_path: str, start: int = 0, end=None) -> None:
            raise RuntimeError("pdf2docx failure")

        def close(self) -> None:
            return None

    monkeypatch.setattr(converter_module, "Converter", FakeConverter)

    result = FileConverter().convert_pdf_to_docx(str(source), str(output))

    assert result is False
    assert not output.exists()


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


def test_convert_docx_to_txt_success(tmp_path: Path):
    """DOCX icerigi UTF-8 TXT cikisina yazilmali."""
    source = tmp_path / "input.docx"
    output = tmp_path / "output.txt"

    document = Document()
    document.add_paragraph("Ilk satir")
    document.add_paragraph("")
    document.add_paragraph("Ikinci satir")
    document.save(source)

    result = FileConverter().convert_docx_to_txt(str(source), str(output))

    assert result is True
    assert output.exists()
    assert output.read_text(encoding="utf-8") == "Ilk satir\nIkinci satir\n"


def test_convert_docx_to_txt_missing_file_returns_false(tmp_path: Path):
    """Olmayan DOCX girdisi icin False donmeli."""
    result = FileConverter().convert_docx_to_txt(
        str(tmp_path / "missing.docx"),
        str(tmp_path / "output.txt"),
    )

    assert result is False
