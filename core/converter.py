"""
core/converter.py — Dosya Dönüştürme Algoritmaları
Sahibi: Said Hamza Turan (Mantık & Algoritma Mühendisi)
"""
"""Dosya format dönüşümlerini (Görsel, PDF, Belge, Tablo) yöneten ana modül."""
"""Dosya format dönüşümlerini (Toplu işlem, PDF, Görsel, Tablo) yöneten modül."""
import os
import logging
import fitz  # PyMuPDF
import pandas as pd
from PIL import Image
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class FileConverter:
    def batch_convert(self, input_paths, output_dir, target_format, **kwargs):
        """Birden fazla dosyayı toplu halde dönüştürür."""
        results = {}
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for path in input_paths:
            filename = os.path.basename(path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}.{target_format.lower()}")
            
            # Basit dispatch mantığı
            success = False
            if ext.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                success = self.convert_image(path, output_path, target_format, **kwargs)
            elif ext.lower() == '.csv' and target_format.lower() == 'xlsx':
                success = self.convert_csv_to_xlsx(path, output_path)
            
            results[path] = success
        return results

    def pdf_to_images(self, input_path, output_dir, image_format="png", dpi=150):
        """PDF'in her sayfasını bir görsel dosyası olarak dışa aktarır."""
        saved_paths = []
        try:
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            doc = fitz.open(input_path)
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                output_path = os.path.join(output_dir, f"page_{i+1}.{image_format}")
                pix.save(output_path)
                saved_paths.append(output_path)
            doc.close()
            logging.info(f"Başarılı: PDF -> {len(saved_paths)} görsel ({output_dir})")
            return saved_paths
        except Exception as e:
            logging.error(f"PDF'ten görsele dönüşüm hatası: {e}")
            return []

    def merge_pdfs(self, input_paths, output_path):
        """Birden fazla PDF dosyasını tek bir PDF'te birleştirir."""
        try:
            result_doc = fitz.open()
            for path in input_paths:
                with fitz.open(path) as m_doc:
                    result_doc.insert_pdf(m_doc)
            result_doc.save(output_path)
            result_doc.close()
            logging.info(f"Başarılı: PDF Birleştirme -> {output_path}")
            return True
        except Exception as e:
            logging.error(f"PDF birleştirme hatası: {e}")
            return False

    # --- Mevcut Metotların (CSV, Image vb.) Buraya Gelecek ---
    def convert_image(self, input_path, output_path, target_format, quality=85):
        try:
            img = Image.open(input_path)
            hedef = target_format.upper()
            if hedef == "JPG": hedef = "JPEG"
            if hedef == "JPEG" and img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.save(output_path, format=hedef, quality=quality)
            return True
        except Exception as e:
            logging.error(f"Görsel hatası: {e}"); return False

    def convert_csv_to_xlsx(self, input_path, output_path):
        try:
            pd.read_csv(input_path).to_excel(output_path, index=False); return True
        except Exception as e:
            logging.error(f"CSV hatası: {e}"); return False