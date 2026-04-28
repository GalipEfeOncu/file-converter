"""
tests/test_viewer.py - FileViewer birim testleri

Okuma ve Streamlit entegrasyon yardimcilarini mock ile dogrular.
"""

from pathlib import Path

import pandas as pd
from docx import Document

from core.viewer import FileViewer
from core import viewer as viewer_module


def test_render_pdf_returns_png_bytes_for_each_page(monkeypatch, tmp_path: Path):
    """PDF render helper her sayfa icin PNG byte listesi donmeli."""
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake pdf")

    class FakePixmap:
        def __init__(self, payload: bytes):
            self.payload = payload

        def tobytes(self, image_format: str) -> bytes:
            assert image_format == "png"
            return self.payload

    class FakePage:
        def __init__(self, payload: bytes):
            self.payload = payload

        def get_pixmap(self):
            return FakePixmap(self.payload)

    class FakeDocument:
        def __len__(self):
            return 2

        def load_page(self, index: int):
            return FakePage(f"page-{index}".encode("utf-8"))

    monkeypatch.setattr(viewer_module.fitz, "open", lambda path: FakeDocument())

    result = FileViewer().render_pdf(str(pdf_path))

    assert result == [b"page-0", b"page-1"]


def test_read_table_supports_csv_and_xlsx(tmp_path: Path):
    """CSV ve XLSX okuma yolları DataFrame donmeli."""
    csv_path = tmp_path / "table.csv"
    xlsx_path = tmp_path / "table.xlsx"
    pd.DataFrame([{"name": "alpha", "value": 1}]).to_csv(csv_path, index=False)
    pd.DataFrame([{"name": "beta", "value": 2}]).to_excel(xlsx_path, index=False)

    viewer = FileViewer()
    csv_df = viewer.read_table(str(csv_path))
    xlsx_df = viewer.read_table(str(xlsx_path))

    assert list(csv_df.columns) == ["name", "value"]
    assert csv_df.iloc[0].to_dict() == {"name": "alpha", "value": 1}
    assert xlsx_df.iloc[0].to_dict() == {"name": "beta", "value": 2}


def test_read_table_invalid_extension_raises_value_error(tmp_path: Path):
    """Desteklenmeyen uzanti ValueError ile raporlanmali."""
    file_path = tmp_path / "data.json"
    file_path.write_text("{}", encoding="utf-8")

    try:
        FileViewer().read_table(str(file_path))
    except ValueError as exc:
        assert "Desteklenmeyen dosya formatı" in str(exc)
    else:
        raise AssertionError("ValueError bekleniyordu")


def test_display_table_shows_dataframe(monkeypatch, tmp_path: Path):
    """display_table basarili okumada dataframe gostermeli."""
    file_path = tmp_path / "table.csv"
    file_path.write_text("name,value\nalpha,1\n", encoding="utf-8")
    calls = {}

    def fake_dataframe(df, use_container_width: bool):
        calls["df"] = df
        calls["use_container_width"] = use_container_width

    monkeypatch.setattr(viewer_module.st, "dataframe", fake_dataframe)

    FileViewer().display_table(str(file_path))

    assert calls["use_container_width"] is True
    assert list(calls["df"]["name"]) == ["alpha"]


def test_display_table_reports_value_error(monkeypatch, tmp_path: Path):
    """display_table ic hata durumunu st.error ile gostermeli."""
    file_path = tmp_path / "bad.json"
    file_path.write_text("{}", encoding="utf-8")
    errors = []
    monkeypatch.setattr(viewer_module.st, "error", errors.append)

    FileViewer().display_table(str(file_path))

    assert errors
    assert "Desteklenmeyen dosya formatı" in errors[0]


def test_display_audio_and_video_read_binary(monkeypatch, tmp_path: Path):
    """Medya helper'lari binary icerigi ilgili Streamlit API'sine aktarmali."""
    audio_path = tmp_path / "sample.mp3"
    video_path = tmp_path / "sample.mp4"
    audio_path.write_bytes(b"audio-bytes")
    video_path.write_bytes(b"video-bytes")
    calls = {"audio": None, "video": None}

    monkeypatch.setattr(viewer_module.st, "audio", lambda data, format=None: calls.__setitem__("audio", (data, format)))
    monkeypatch.setattr(viewer_module.st, "video", lambda data, format=None: calls.__setitem__("video", (data, format)))

    viewer = FileViewer()
    viewer.display_audio(str(audio_path), format="audio/mpeg")
    viewer.display_video(str(video_path), format="video/mp4")

    assert calls["audio"] == (b"audio-bytes", "audio/mpeg")
    assert calls["video"] == (b"video-bytes", "video/mp4")


def test_display_text_document_supports_txt_docx_and_warning(monkeypatch, tmp_path: Path):
    """Metin helper'i TXT, DOCX ve unsupported akislari dogru API'lere yonlendirmeli."""
    txt_path = tmp_path / "sample.txt"
    txt_path.write_text("Merhaba dunya", encoding="utf-8")
    docx_path = tmp_path / "sample.docx"
    doc = Document()
    doc.add_paragraph("Ilk paragraf")
    doc.add_paragraph("Ikinci paragraf")
    doc.save(docx_path)
    unsupported_path = tmp_path / "sample.md"
    unsupported_path.write_text("# baslik", encoding="utf-8")

    calls = {"text_area": [], "markdown": [], "warning": []}
    monkeypatch.setattr(viewer_module.st, "text_area", lambda label, value, height=400: calls["text_area"].append((label, value, height)))
    monkeypatch.setattr(viewer_module.st, "markdown", calls["markdown"].append)
    monkeypatch.setattr(viewer_module.st, "warning", calls["warning"].append)

    viewer = FileViewer()
    viewer.display_text_document(str(txt_path))
    viewer.display_text_document(str(docx_path))
    viewer.display_text_document(str(unsupported_path))

    assert calls["text_area"] == [("Belge İçeriği", "Merhaba dunya", 400)]
    assert calls["markdown"] == ["Ilk paragraf\n\nIkinci paragraf"]
    assert calls["warning"] == ["Bu metin formatı desteklenmiyor."]
