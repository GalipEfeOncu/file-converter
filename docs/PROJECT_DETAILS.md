# 📄 Project Details — File Converter & Analyzer

> Çok amaçlı bir masaüstü/web uygulaması: dosya dönüştürme, dahili görüntüleme ve yapay zekâ destekli içerik analizi.
>
> 💡 **Modeller / yeni geliştiriciler için:** Önce `docs/AGENT_GUIDE.md` dosyasını okuyun — kod açmadan tüm mimariyi ve sözleşmeleri tek dosyada özetler. Bu döküman ise yüksek seviyeli ürün vizyonunu açıklar.
>
> **Son Güncelleme:** 2026-04-19

---

## 🔍 Proje Tanımı

Bu proje; farklı dosya türlerini **dönüştürebilen**, uygulama içinde **görüntüleyebilen/çalıştırabilen** ve **yapay zekâ destekli içerik analizi** yapabilen çok amaçlı bir masaüstü veya web uygulamasıdır.

**UI Kütüphanesi:** [Streamlit](https://streamlit.io)

---

## 🧩 Modüller

### 1. Dosya Dönüştürme Modülü

Uygulama aşağıdaki kategorilerde dosya dönüştürme işlemleri gerçekleştirir:

#### 1.1 Metin ve Belge Dosyaları

| Kaynak Format | Hedef Format | Durum |
|---|---|---|
| PDF | DOCX | ✅ `FileConverter.convert_pdf_to_docx` |
| PDF | TXT, PNG, JPG | 🔲 Planlı (henüz kod yok) |
| DOCX | PDF | ✅ `convert_docx_to_pdf` (Windows + MS Word gerekir) |
| DOCX | TXT | ✅ `convert_docx_to_txt` |
| CSV | XLSX | ✅ `convert_csv_to_xlsx` |
| XLSX | CSV | ✅ `convert_xlsx_to_csv` |

> **Amaç:** Metin ve tablo içeren dosyaları kendi aralarında dönüştürebilmek.

#### 1.2 Görsel Dosyaları

Tek metot (`FileConverter.convert_image(input, output, target_format, quality=100)`) tüm dönüşümleri yapar.

| Dönüşüm | Durum |
|---|---|
| PNG ↔ JPG | ✅ |
| PNG / JPG ↔ WEBP | ✅ |
| BMP → diğer formatlar | ✅ |
| Görsel formatları arası kalite ayarlı dönüşüm (`quality: int`) | ✅ |

> Not: JPEG çıktısı için RGBA/P mod görseller otomatik olarak RGB'ye çevrilir.

#### 1.3 Ses Dosyaları

`AudioConverter.convert_audio(input, output, target_format)` jenerik metot herhangi-iki ses formatını dönüştürür (FFmpeg PATH'te olmalı).

| Dönüşüm | Durum |
|---|---|
| MP3 ↔ OGG | ✅ Kısayol metotlar (`convert_mp3_to_ogg`, `convert_ogg_to_mp3`) |
| MP3 ↔ WAV | ✅ `convert_audio` ile (`target_format="wav"`/`"mp3"`) |
| Diğer pydub destekli formatlar | ✅ `convert_audio` ile |

---

### 2. Dosya Görüntüleme ve Çalıştırma Modülü

Kullanıcı, uygulama içinde dosyaları açıp görüntüleyebilecektir:

| Dosya Türü | Görüntüleyici | Metot | Durum |
|---|---|---|---|
| PDF | Dahili PDF görüntüleyici (PyMuPDF + `st.image`) | `FileViewer.display_pdf` / `render_pdf` | ✅ |
| DOCX / TXT | Metin görüntüleyici (`st.markdown` / `st.text_area`) | `FileViewer.display_text_document` | ✅ |
| PNG / JPG / WEBP | Görsel görüntüleyici (`st.image`) | 🔲 Planlı (henüz `display_image` metodu yok) | 🔲 |
| MP3 / WAV / OGG | Dahili ses oynatıcı (`st.audio`) | `FileViewer.display_audio` | ✅ |
| MP4 / MOV / WEBM | Dahili video oynatıcı (`st.video`) | `FileViewer.display_video` | ✅ |
| CSV / XLSX | Tablo görüntüleyici (`st.dataframe`) | `FileViewer.display_table` / `read_table` | ✅ |

> ⚠️ Bu metotlar `core/viewer.py` içinde mevcuttur ancak `Dashboard.render_main_area()` "Görüntüle" sekmesi henüz bu metotları çağırmaz; placeholder metin gösterir.

> **Amaç:** Kullanıcı, başka bir programa ihtiyaç duymadan dosyayı doğrudan uygulama içinde inceleyebilmeli.

---

### 3. Yapay Zekâ Destekli Analiz Modülü

> ⚠️ **Mevcut Durum:** `core/ai_engine.py` STUB seviyededir. `summarize()` ve `answer_question()` placeholder string döner. Groq/OpenAI entegrasyonu beklemededir (`Config.GROQ_API_KEY` `.env`'den okunur).

Uygulama içinde dosya içeriğini okuyabilen ve analiz edebilen bir AI sistemi bulunacaktır.

**AI Özellikleri:**

- 📝 Metin dosyasını özetleme
- ❓ İçerikten soru üretme
- 🔑 Anahtar kelime çıkarma
- 🏷️ Konu başlığı üretme
- 🔤 Metni farklı seviyelerde sadeleştirme

**Desteklenen Dosya Türleri:**

| Format | Not |
|---|---|
| PDF | ✅ Tam destek |
| DOCX | ✅ Tam destek |
| TXT | ✅ Tam destek |
| CSV | ⚠️ Yalnızca metinsel veri için |

> **Amaç:** Dosyayı sadece açmak değil, içerikten anlam üretmek.

---

### 4. Kullanıcı Deneyimi ve Ek Özellikler

| Özellik | Durum | Açıklama |
|---|---|---|
| 🌗 Tema | ⚠️ Kısmen | Karanlık tema aktif (`ui/styles.py`); açık tema seçici sidebar'da var ama `disabled` |
| 🌍 Çoklu Dil | ✅ | Türkçe / İngilizce, runtime'da `st.selectbox` ile değişir, `st.rerun()` tetikler |
| 🕓 Dosya Geçmişi | ✅ | Son 5 dosya sidebar'da gösterilir (`st.session_state.file_history`) |
| 🖱️ Sürükle-Bırak | ✅ | Streamlit varsayılan + özel CSS (gradient + dashed border) |
| ⚙️ Ayarlar | 🔲 | Sidebar'da expander mevcut ama içerik placeholder (tema seçici disabled) |

---

## 📌 Notlar

- Proje **Streamlit** kullanılarak geliştirilecektir.
- Dosya yapısı modüler ve genişletilebilir biçimde tasarlanacaktır.