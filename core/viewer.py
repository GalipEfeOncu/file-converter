import logging
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
        """TXT, DOCX ve kod/veri metin dosyalarını okuyup arayüzde gösterir.

        Desteklenen uzantılar:
            .txt, .py, .js, .html, .css, .java, .cpp, .sql,
            .yaml, .json, .xml  → UTF-8 düz metin, st.code ile gösterilir
            .docx, .doc         → python-docx ile st.markdown
            .rtf, .odt          → düz metin olarak okunmaya çalışılır
        """
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()

        # --- DOCX / DOC: python-docx ile paragraf çıkar ---
        if uzanti in ['.docx', '.doc']:
            try:
                doc = docx.Document(file_path)
                tam_metin = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                st.markdown(tam_metin)
            except Exception as e:
                logging.error(f"Hata: Word dosyası okunurken hata oluştu ({file_path}): {e}")
                st.error(f"Word dosyası okunurken hata oluştu: {e}")

        # --- TXT: basit metin alanı ---
        elif uzanti == '.txt':
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                icerik = f.read()
            # TODO(i18n): "Belge İçeriği" → document_content anahtarına taşınacak (Ali koordinasyonu)
            st.text_area("Belge İçeriği", icerik, height=400)

        # --- Kod ve veri dosyaları: syntax highlighting ile st.code ---
        else:
            # Uzantıya göre dil adını belirle (Streamlit st.code için)
            _lang_map = {
                ".py": "python", ".js": "javascript", ".html": "html",
                ".css": "css", ".java": "java", ".cpp": "cpp",
                ".sql": "sql", ".yaml": "yaml", ".json": "json",
                ".xml": "xml", ".rtf": "text", ".odt": "text",
            }
            lang = _lang_map.get(uzanti, "text")
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    icerik = f.read()
                logging.info(f"Başarılı: Metin dosyası gösterildi ({file_path})")
                st.code(icerik, language=lang)
            except Exception as e:
                logging.error(f"Hata: Metin dosyası okunurken hata oluştu ({file_path}): {e}")
                st.error(f"Dosya okunurken hata oluştu: {e}")



    def display_image(self, file_path: str) -> None:
        """Görsel dosyaları Streamlit arayüzünde tam genişlikte gösterir.

        Args:
            file_path: Gösterilecek görsel dosyasının yolu (.png, .jpg, .jpeg, .webp, .bmp).
        """
        try:
            st.image(file_path, use_container_width=True)
            logging.info(f"Başarılı: Görsel gösterildi ({file_path})")
        except FileNotFoundError:
            logging.error(f"Hata: Görsel dosyası bulunamadı ({file_path})")
            st.error(f"Dosya bulunamadı: {file_path}")
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (display_image): {e}")
            st.error(f"Görsel gösterilirken hata oluştu: {e}")

    def extract_text(self, file_path: str) -> str:
        """PDF, DOCX, TXT ve CSV dosyalarından AI analizi için saf metin çıkarır."""
        dosya_adi, uzanti = os.path.splitext(file_path)
        uzanti = uzanti.lower()
        metin = ""

        try:
            if uzanti == '.pdf':
                doc = fitz.open(file_path)
                for page in doc:
                    metin += page.get_text() + "\n"
            elif uzanti in ['.docx', '.doc']:
                doc = docx.Document(file_path)
                metin = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            elif uzanti in ['.txt', '.csv']:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    metin = f.read()
            else:
                logging.warning(f"Desteklenmeyen dosya türü, metin çıkarılamadı: {uzanti}")
        except Exception as e:
            logging.error(f"Metin çıkarılırken hata oluştu ({file_path}): {e}")

        return metin.strip()

