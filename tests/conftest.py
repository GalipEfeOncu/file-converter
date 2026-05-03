import pytest
import fitz
import os

@pytest.fixture
def sample_pdf_path(tmp_path):
    """Her test için temiz bir 1 sayfalık PDF fixture'ı oluşturur."""
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((100, 100), "Test PDF Content")
    doc.save(str(pdf_path))
    doc.close()
    return str(pdf_path)
