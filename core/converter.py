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
import pypandoc
import inspect

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class FileConverter:
    QUALITY_PRESETS = {"low": 50, "medium": 75, "high": 90, "lossless": 100}
    def convert_pdf_to_docx(self, input_path: str, output_path: str, start: int = 0, end: int | None = None) -> bool:
        try:
            cv = Converter(input_path)
            cv.convert(output_path, start=start, end=end)
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

    def convert_image(self, input_path: str, output_path: str, target_format: str, quality: int | str = 100) -> bool:
        try:
            img = Image.open(input_path)
            target = target_format.upper().replace("JPG", "JPEG")
            if isinstance(quality, str):
                quality_key = quality.lower()
                if quality_key not in self.QUALITY_PRESETS:
                    raise ValueError(f"Bilinmeyen kalite preset'i: {quality}")
                quality = self.QUALITY_PRESETS[quality_key]
            if target == "JPEG" and img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.save(output_path, format=target, quality=quality); return True
        except Exception as e:
            logging.error(f"Görsel Hatası: {e}"); return False

    def convert_rtf_to_docx(self, input_path: str, output_path: str) -> bool:
        try:
            pypandoc.convert_file(input_path, "docx", format="rtf", outputfile=output_path)
            return True
        except Exception as e:
            logging.error(f"RTF->DOCX Hatası: {e}"); return False

    def convert_odt_to_docx(self, input_path: str, output_path: str) -> bool:
        try:
            pypandoc.convert_file(input_path, "docx", format="odt", outputfile=output_path)
            return True
        except Exception as e:
            logging.error(f"ODT->DOCX Hatası: {e}"); return False

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

    _CONVERSION_REGISTRY = {
        # format: (method_name, extra_kwargs)
        (".pdf", "docx"): "convert_pdf_to_docx",
        (".docx", "pdf"): "convert_docx_to_pdf",
        (".docx", "txt"): "convert_docx_to_txt",
        (".csv", "xlsx"): "convert_csv_to_xlsx",
        (".xlsx", "csv"): "convert_xlsx_to_csv",
        (".rtf", "docx"): "convert_rtf_to_docx",
        (".odt", "docx"): "convert_odt_to_docx",
        # Image extensions (dynamically handled in batch_convert or explicitly listed)
    }

    def batch_convert(self, input_paths, output_dir, target_format, **kwargs):
        """Toplu dosya dönüştürme işlemi. Registry üzerinden uygun metodu bulur."""
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        results = {}
        target = target_format.lower()
        
        image_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
        
        for path in input_paths:
            ext = os.path.splitext(path)[1].lower()
            out_name = f"converted_{os.path.basename(path).split('.')[0]}.{target}"
            out_path = os.path.join(output_dir, out_name)
            
            # 1. Registry kontrolü
            method_name = self._CONVERSION_REGISTRY.get((ext, target))
            if method_name:
                method = getattr(self, method_name)
                sig = inspect.signature(method)
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
                results[path] = method(path, out_path, **filtered_kwargs)
            
            # 2. Görsel dönüşüm (Generic handling)
            elif ext in image_exts and target in {"jpg", "jpeg", "png", "webp", "bmp"}:
                sig = inspect.signature(self.convert_image)
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
                results[path] = self.convert_image(path, out_path, target, **filtered_kwargs)
            
            else:
                logging.warning(f"Batch: {ext} -> {target} için uygun dönüştürücü bulunamadı.")
                results[path] = False
                
        return results

    def pdf_to_images(self, input_path, output_dir, image_format="png", dpi=150):
        """PDF sayfalarını tekil görsellere dönüştürür."""
        try:
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            doc = fitz.open(input_path); saved = []
            for i, page in enumerate(doc):
                # Matrix ile DPI ayarı (default 72'dir)
                zoom = dpi / 72
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                out = os.path.join(output_dir, f"p_{i+1}.{image_format}")
                pix.save(out); saved.append(out)
            doc.close(); return saved
        except Exception as e:
            logging.error(f"PDF->IMG Hatası: {e}"); return []

    def merge_pdfs(self, input_paths, output_path):
        """Birden fazla PDF dosyasını tek bir dosyada birleştirir."""
        try:
            res = fitz.open()
            for p in input_paths:
                with fitz.open(p) as m: res.insert_pdf(m)
            res.save(output_path); res.close(); return True
        except Exception as e:
            logging.error(f"Merge Hatası: {e}"); return False