"""
core/converter.py — Dosya Dönüştürme Algoritmaları
Sahibi: Said Hamza Turan (Mantık & Algoritma Mühendisi)
"""
"""Dosya format dönüşümlerini (Görsel, PDF, Belge, Tablo) yöneten ana modül."""
"""Dosya format dönüşümlerini (Toplu işlem, PDF, Görsel, Tablo) yöneten modül."""
import os
import logging
import docx
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class FileConverter:
    def convert_pdf_to_docx(self, input_path: str, output_path: str) -> bool:
        try:
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            return True
        except Exception as e:
            logging.error(f"PDF->DOCX Hatası: {e}"); return False

    def convert_csv_to_xlsx(self, input_path: str, output_path: str) -> bool:
        try:
            pd.read_csv(input_path).to_excel(output_path, index=False); return True
        except Exception as e:
            logging.error(f"CSV->XLSX Hatası: {e}"); return False

    def convert_xlsx_to_csv(self, input_path: str, output_path: str) -> bool:
        try:
            pd.read_excel(input_path).to_csv(output_path, index=False); return True
        except Exception as e:
            logging.error(f"XLSX->CSV Hatası: {e}"); return False

    def convert_image(self, input_path: str, output_path: str, target_format: str, quality: int = 85) -> bool:
        try:
            img = Image.open(input_path)
            target = target_format.upper().replace("JPG", "JPEG")
            if target == "JPEG" and img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.save(output_path, format=target, quality=quality); return True
        except Exception as e:
            logging.error(f"Görsel Hatası: {e}"); return False

    def convert_docx_to_txt(self, input_path: str, output_path: str) -> bool:
        try:
            doc = docx.Document(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                for p in doc.paragraphs:
                    if p.text.strip(): 
                        f.write(p.text + "\n")
            return True
        except Exception as e:
            logging.error(f"DOCX->TXT Hatası: {e}"); return False

    def convert_docx_to_pdf(self, input_path: str, output_path: str) -> bool:
        try:
            docx2pdf_convert(input_path, output_path); return True
        except Exception as e:
            logging.error(f"DOCX->PDF Hatası: {e}"); return False

    def batch_convert(self, input_paths, output_dir, target_format, **kwargs):
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        results = {}
        for path in input_paths:
            ext = os.path.splitext(path)[1].lower()
            out = os.path.join(output_dir, f"converted_{os.path.basename(path)}.{target_format.lower()}")
            results[path] = self.convert_image(path, out, target_format, **kwargs)
        return results

    def pdf_to_images(self, input_path, output_dir, image_format="png", dpi=150):
        try:
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            doc = fitz.open(input_path); saved = []
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                out = os.path.join(output_dir, f"p_{i+1}.{image_format}")
                pix.save(out); saved.append(out)
            doc.close(); return saved
        except Exception as e:
            logging.error(f"PDF->IMG Hatası: {e}"); return []

    def merge_pdfs(self, input_paths, output_path):
        try:
            res = fitz.open()
            for p in input_paths:
                with fitz.open(p) as m: res.insert_pdf(m)
            res.save(output_path); res.close(); return True
        except Exception as e:
            logging.error(f"Merge Hatası: {e}"); return False