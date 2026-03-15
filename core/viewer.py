import pandas as pd
import fitz 
import os

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
        
        # 1. Validator (Doğrulayıcı): Dosyanın uzantısını alıyoruz
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower() # Büyük/küçük harf sorunu olmasın diye küçültüyoruz
        
        try:
            # 2. Eğer dosya CSV ise pandas'ın read_csv fonksiyonunu kullan
            if uzanti == '.csv':
                return pd.read_csv(file_path)
            
            # 3. Eğer dosya Excel ise pandas'ın read_excel fonksiyonunu kullan
            elif uzanti in ['.xls', '.xlsx']:
                return pd.read_excel(file_path)
            
            # 4. Desteklenmeyen bir dosyaysa hata fırlat (Burası Validator kısmımız)
            else:
                raise ValueError("Desteklenmeyen dosya formatı! Lütfen .csv veya .xlsx yükleyin.")
                
        except Exception as e:
            # Okuma sırasında dosya bozuksa veya başka hata varsa yakalıyoruz
            raise ValueError(f"Dosya okunurken bir hata oluştu: {e}")