import pandas as pd
import fitz 
import os
import streamlit as st  # Arayüz bileşenleri için eklendi
import docx             # Word dosyalarını okumak için eklendi

class FileViewer:
    """Dosyaları önizleme için uygun formata dönüştürür ve arayüzde gösterir."""

    # --- SENİN MEVCUT KODLARIN (ARKA PLAN) ---

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
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()
        
        try:
            if uzanti == '.csv':
                return pd.read_csv(file_path)
            elif uzanti in ['.xls', '.xlsx']:
                return pd.read_excel(file_path)
            else:
                raise ValueError("Desteklenmeyen dosya formatı! Lütfen .csv veya .xlsx yükleyin.")
                
        except Exception as e:
            raise ValueError(f"Dosya okunurken bir hata oluştu: {e}")

    # --- YENİ EKLENEN KISIM (UI / ARAYÜZ GÖREVLERİN) ---

    def display_pdf(self, pdf_path: str):
        """PDF sayfalarını Streamlit arayüzünde alt alta gösterir."""
        resim_listesi = self.render_pdf(pdf_path)
        for i, resim in enumerate(resim_listesi):
            st.image(resim, caption=f"Sayfa {i+1}", use_container_width=True)

    def display_table(self, file_path: str):
        """Tablo verilerini Streamlit arayüzünde gösterir."""
        try:
            df = self.read_table(file_path)
            st.dataframe(df, use_container_width=True)
        except ValueError as e:
            st.error(str(e))

    def display_audio(self, file_path: str, format="audio/mp3"):
        """Ses dosyalarını arayüzde oynatır."""
        with open(file_path, "rb") as f:
            st.audio(f.read(), format=format)

    def display_video(self, file_path: str, format="video/mp4"):
        """Video dosyalarını arayüzde oynatır."""
        with open(file_path, "rb") as f:
            st.video(f.read(), format=format)

    def display_text_document(self, file_path: str):
        """TXT ve DOCX içeriklerini okuyup arayüzde metin olarak basar."""
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()

        if uzanti == '.txt':
            with open(file_path, "r", encoding="utf-8") as f:
                icerik = f.read()
            st.text_area("Belge İçeriği", icerik, height=400)
            
        elif uzanti in ['.docx', '.doc']:
            try:
                doc = docx.Document(file_path)
                # Word'deki tüm paragrafları alt alta birleştirir
                tam_metin = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                st.markdown(tam_metin)
            except Exception as e:
                st.error(f"Word dosyası okunurken hata oluştu: {e}")
        else:
            st.warning("Bu metin formatı desteklenmiyor.")

