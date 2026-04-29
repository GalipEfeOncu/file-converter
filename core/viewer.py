import logging
import pandas as pd
import fitz
import os
import streamlit as st  # Arayüz bileşenleri için eklendi
import docx             # Word dosyalarını okumak için eklendi

class FileViewer:
    """Dosyaları önizleme için uygun formata dönüştürür ve arayüzde gösterir."""

    # --- SENİN MEVCUT KODLARIN (ARKA PLAN) ---

    def render_pdf(self, pdf_path: str, start: int = 0, end: int | None = None) -> list[bytes]:
        """PDF sayfalarini gorsel olarak render eder.

        Args:
            pdf_path: Render edilecek PDF dosyasinin yolu.
            start: Baslangic sayfa indeksi (dahil, 0-tabanli). Varsayilan: 0.
            end: Bitis sayfa indeksi (haric, None ise son sayfa). Varsayilan: None.

        Returns:
            Her sayfa icin PNG byte dizisi iceren liste.
        """
        doc = fitz.open(pdf_path)
        toplam_sayfa = len(doc)
        bitis = end if end is not None else toplam_sayfa
        # Sinir kontrolu
        bitis = min(bitis, toplam_sayfa)
        baslangic = max(0, start)

        resim_listesi = []
        for sayfa_numarasi in range(baslangic, bitis):
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

    def display_pdf(self, pdf_path: str, texts: dict | None = None) -> None:
        """PDF sayfalarini Streamlit arayuzunde sayfa sayfa (lazy) gosterir.

        Pagination: st.session_state['pdf_current_page'] ile sayfa takibi yapilir.
        Her seferinde yalnizca tek bir sayfa render edilir — buyuk PDF'lerde performans icin.

        Args:
            pdf_path: Gosterilecek PDF dosyasinin yolu.
            texts: i18n sozlugu (opsiyonel). Fallback Turkce string'ler mevcuttur.
        """
        if texts is None:
            texts = {}

        try:
            doc = fitz.open(pdf_path)
            toplam_sayfa = len(doc)
        except Exception as e:
            logging.error(f"Hata: PDF acilamadi ({pdf_path}): {e}")
            st.error(f"PDF acilamadi: {e}")
            return

        if toplam_sayfa == 0:
            st.warning("PDF bos gorunuyor.")
            return

        # --- Session state ile sayfa indeksini yonet ---
        if "pdf_current_page" not in st.session_state:
            st.session_state["pdf_current_page"] = 0

        # Dosya degistiginde sayfayi sifirla
        pdf_key = f"pdf_key_{pdf_path}"
        if st.session_state.get("_pdf_last_path") != pdf_path:
            st.session_state["pdf_current_page"] = 0
            st.session_state["_pdf_last_path"] = pdf_path

        current = st.session_state["pdf_current_page"]
        pdf_page_of = texts.get("pdf_page_of", "/ toplam sayfa")

        # --- Sayfa numarasi input + bilgi satiri ---
        col_info, col_nav = st.columns([3, 2])
        with col_info:
            sayfa_no = st.number_input(
                f"Sayfa ({pdf_page_of} {toplam_sayfa})",
                min_value=1,
                max_value=toplam_sayfa,
                value=current + 1,
                step=1,
                key="pdf_page_input",
            )
            current = sayfa_no - 1
            st.session_state["pdf_current_page"] = current

        with col_nav:
            st.write("")
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("◀ Onceki", key="pdf_prev", disabled=(current == 0)):
                    st.session_state["pdf_current_page"] = max(0, current - 1)
                    st.rerun()
            with nav_col2:
                if st.button("Sonraki ▶", key="pdf_next", disabled=(current >= toplam_sayfa - 1)):
                    st.session_state["pdf_current_page"] = min(toplam_sayfa - 1, current + 1)
                    st.rerun()

        # --- Yalnizca aktif sayfayi render et (lazy) ---
        resimler = self.render_pdf(pdf_path, start=current, end=current + 1)
        if resimler:
            st.image(resimler[0], caption=f"Sayfa {current + 1} / {toplam_sayfa}", use_container_width=True)
            logging.info(f"Basarili: PDF sayfa {current + 1}/{toplam_sayfa} gosterildi ({pdf_path})")

    def display_table(self, file_path: str, texts: dict | None = None) -> None:
        """Tablo verilerini arama/filtreleme destegi ile Streamlit arayuzunde gosterir.

        Args:
            file_path: Gosterilecek CSV veya Excel dosyasinin yolu.
            texts: i18n sozlugu (opsiyonel). Fallback Turkce string'ler mevcuttur.
        """
        if texts is None:
            texts = {}

        try:
            df = self.read_table(file_path)
        except ValueError as e:
            st.error(str(e))
            return

        # --- Arama inputu ---
        search_label = texts.get("pdf_search_label", "Tabloda ara...")
        query = st.text_input(search_label, key="table_search_query")

        if query:
            try:
                filtered = df[df.apply(
                    lambda row: row.astype(str).str.contains(query, case=False, na=False).any(),
                    axis=1
                )]
            except Exception as e:
                logging.error(f"Hata: Tablo filtresi uygulanamadi: {e}")
                filtered = df

            if filtered.empty:
                no_match_msg = texts.get("table_no_match", "Aramanizla eslesen satir bulunamadi.")
                st.info(no_match_msg)
                logging.info(f"Tablo aramasinda sonuc bulunamadi. Sorgu: '{query}'")
            else:
                st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

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

