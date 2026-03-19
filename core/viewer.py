import pandas as pd
import fitz 

class FileViewer:
    """Dosyaları önizleme için uygun formata dönüştürür."""

    def render_pdf(self, pdf_path: str):
        """PDF sayfalarını görsel olarak render eder."""
        doc = fitz.open(pdf_path) 
        resim_listesi = []
        
        for sayfa_numarasi in range(len(doc)):
            sayfa = doc.load_page(sayfa_numarasi)
            resim_verisi = sayfa.get_pixmap() 
            png_formati = resim_verisi.tobytes("png") 
            resim_listesi.append(png_formati)
            
        return resim_listesi

    def read_table(self, file_path: str) -> pd.DataFrame:
        """CSV veya Excel dosyalarını DataFrame olarak okur."""
        return pd.DataFrame()