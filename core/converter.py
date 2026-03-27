"""
core/converter.py — Dosya Dönüştürme Algoritmaları
Sahibi: Said Hamza Turan (Mantık & Algoritma Mühendisi)
"""
import docx
from docx2pdf import convert as docx2pdf_convert
from PIL import Image
import pandas as pd
import logging
from pdf2docx import Converter

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class FileConverter:
    def convert_pdf_to_docx(self, input_path: str, output_path: str) -> bool:
        try:
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
            logging.info(f"Başarılı: PDF -> DOCX ({output_path})")
            return True
            
        except FileNotFoundError:
            logging.error(f"Hata: Girdi dosyası bulunamadı ({input_path})")
            return False
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (PDF->DOCX): {e}")
            return False

    def convert_csv_to_xlsx(self, input_path: str, output_path: str) -> bool:
        try:
            df = pd.read_csv(input_path)
            df.to_excel(output_path, index=False, engine='openpyxl')
            
            logging.info(f"Başarılı: CSV -> XLSX ({output_path})")
            return True
            
        except pd.errors.EmptyDataError:
            logging.error("Hata: Dönüştürülmeye çalışılan CSV dosyası boş.")
            return False
        except FileNotFoundError:
            logging.error(f"Hata: Girdi dosyası bulunamadı ({input_path})")
            return False
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (CSV->XLSX): {e}")
            return False

    def convert_xlsx_to_csv(self, input_path: str, output_path: str) -> bool:
        try:
            df = pd.read_excel(input_path, engine='openpyxl')
            df.to_csv(output_path, index=False)
            
            logging.info(f"Başarılı: XLSX -> CSV ({output_path})")
            return True
            
        except FileNotFoundError:
            logging.error(f"Hata: Girdi dosyası bulunamadı ({input_path})")
            return False
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (XLSX->CSV): {e}")
            return False
    def convert_image(self, input_path: str, output_path: str, target_format: str, quality: int = 100) -> bool:
     
        try:
            img = Image.open(input_path)
            
            hedef = target_format.upper()
            if hedef == "JPG":
                hedef = "JPEG"

            if hedef == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.save(output_path, format=hedef, quality=quality)
            
            logging.info(f"Başarılı: Görsel Dönüşümü -> {output_path} (Kalite: %{quality})")
            return True

        except FileNotFoundError:
            logging.error(f"Hata: Girdi görseli bulunamadı ({input_path})")
            return False
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (Görsel Dönüşümü): {e}")
            return False        
    def convert_docx_to_txt(self, input_path: str, output_path: str) -> bool:
        try:
            doc = docx.Document(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                for para in doc.paragraphs:
                    if para.text.strip():
                        f.write(para.text + "\n")
                        
            logging.info(f"Başarılı: DOCX -> TXT ({output_path})")
            return True
            
        except FileNotFoundError:
            logging.error(f"Hata: Girdi dosyası bulunamadı ({input_path})")
            return False
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (DOCX->TXT): {e}")
            return False

    def convert_docx_to_pdf(self, input_path: str, output_path: str) -> bool:
        try:
            docx2pdf_convert(input_path, output_path)
            
            logging.info(f"Başarılı: DOCX -> PDF ({output_path})")
            return True
            
        except Exception as e:
            logging.error(f"Hata (DOCX->PDF): Sistemde MS Word eksik olabilir veya dönüştürme başarısız. Detay: {e}")
            return False