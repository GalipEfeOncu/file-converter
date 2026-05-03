import pytest
import os
from core.converter import FileConverter

def test_pdf_to_images_success(sample_pdf_path, tmp_path):
    """[R-1] PDF sayfalarini gorsellere donusturme basarili olmali."""
    fc = FileConverter()
    output_dir = tmp_path / "images"
    
    result = fc.pdf_to_images(sample_pdf_path, str(output_dir))
    
    assert len(result) > 0
    assert os.path.exists(result[0])
    assert result[0].endswith(".png")

def test_merge_pdfs_success(sample_pdf_path, tmp_path):
    """[R-1] PDF birlestirme basarili olmali ve sayfa sayisi artmali."""
    fc = FileConverter()
    output_path = tmp_path / "merged.pdf"
    
    # Kendisiyle birlestir -> 2 sayfa olmali
    success = fc.merge_pdfs([sample_pdf_path, sample_pdf_path], str(output_path))
    
    assert success is True
    assert os.path.exists(output_path)
    
    # Sayfa sayisini kontrol et
    import fitz
    doc = fitz.open(str(output_path))
    assert len(doc) == 2
    doc.close()

def test_merge_pdfs_invalid_input(tmp_path):
    """[R-1] Gecersiz girdi durumunda hata firlatmadan False donmeli."""
    fc = FileConverter()
    output_path = tmp_path / "merged_fail.pdf"
    
    # Olmayan dosyalar
    res = fc.merge_pdfs(["non_existent1.pdf", "non_existent2.pdf"], str(output_path))
    assert res is False
    assert not os.path.exists(output_path)
