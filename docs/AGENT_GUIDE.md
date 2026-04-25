# 🧭 AGENT_GUIDE.md — Modeller İçin Tek Dosyalık Proje Rehberi

> **Amaç:** Bu dosya, projenin kaynak kodunu okumadan tüm mimariyi, sözleşmeleri (contracts), veri akışını, hata tuzaklarını ve kodlama kurallarını bir AI modelinin tam olarak anlayabilmesi için yazılmıştır.
>
> **Hedef Kitle:** Düşük kapasiteli / hızlı kodlama modelleri (örn. küçük yardımcı LLM'ler).
> **Bu dosyayı okuduktan sonra model:** Yeni özellik ekleyebilir, mevcut modülleri çağırabilir, doğru i18n anahtarlarını kullanabilir, hataları önleyebilir.
>
> **Kaynak Doğruluk:** Bu dosya `2026-04-21` itibarıyla `main.py`, `core/*`, `ui/*`, `config/*`, `assets/*` ve `tests/*` ile birebir senkronize edilmiştir.

---

## 0. Hızlı Özet (TL;DR)

- **Proje Adı:** Universal File Workstation (klasör adı: `file-converter`)
- **Tip:** Streamlit tabanlı, yerel-öncelikli (local-first), masaüstü/web hibrit dosya araç çantası.
- **Üç Ana Yetenek:** Dosya Dönüştürme · Dosya Görüntüleme · AI Analizi (Gemini API entegre).
- **Dil:** Python 3.10+
- **UI:** Streamlit + özel CSS enjeksiyonu (karanlık tema).
- **Çoklu Dil:** Türkçe (varsayılan) / İngilizce, runtime'da değiştirilebilir.
- **Giriş Noktası:** `streamlit run main.py`
- **Mimari Kuralı:** `core/` Streamlit import etmez; `ui/` dosya I/O yapmaz; `config/` iş mantığı içermez.

---

## 1. Klasör Haritası (Görsel Zihin Modeli)

```
file-converter/
├── main.py                   ← Streamlit giriş noktası, session_state başlatır, Dashboard'u tetikler
├── config/
│   └── settings.py           ← Config sınıfı (sabitler, API key, desteklenen uzantılar)
├── core/                     ← İŞ MANTIĞI (Streamlit import YASAK)
│   ├── converter.py          ← FileConverter: PDF↔DOCX, CSV↔XLSX, Image, DOCX→PDF/TXT
│   ├── player.py             ← AudioConverter: pydub + FFmpeg ile ses dönüşümü
│   ├── viewer.py             ← FileViewer: PDF→PNG, tablo, ses/video/text gösterimi
│   └── ai_engine.py          ← AIEngine: summarize/answer_question/extract_keywords/simplify (Gemini API)
├── ui/                       ← SUNUM KATMANI (dosya I/O YASAK)
│   ├── dashboard.py          ← Dashboard sınıfı: render_sidebar() + render_main_area()
│   └── styles.py             ← apply_custom_css(): tek fonksiyon, tüm tema CSS'i
├── config/
│   └── settings.py
├── assets/
│   └── languages.json        ← i18n tek kaynak; tr ve en kökleri ZORUNLU
├── tests/                    ← pytest
│   ├── test_languages.py     ← tr/en anahtar paritesi + zorunlu runtime anahtarları
│   └── test_requirements.py  ← ~= operatörü + tekillik kontrolü
├── docs/                     ← TÜM dökümantasyon burada
├── temp/                     ← Runtime geçici dosyalar (git-ignore)
├── .env                      ← GEMINI_API_KEY (git-ignore)
├── requirements.txt          ← Tüm bağımlılıklar `~=` ile pinli
├── test.py                   ← Manuel entegrasyon (image + ffmpeg)
└── test_core.py              ← Manuel entegrasyon (converter)
```

> **Not:** `!prototip/` klasörü eski/deneme kodları içerir; **dokunma**.

---

## 2. Modüllerin API Sözleşmeleri (Kod Okumadan Çağırma Rehberi)

> Aşağıdaki imzalar **birebir doğrudur**; modeller bu sözleşmelere güvenerek import edip çağırabilir.

### 2.1 `config/settings.py`

```python
from config.settings import Config

Config.APP_NAME            # "Universal File Workstation"
Config.VERSION             # "0.1.0-alpha"
Config.DEFAULT_LANGUAGE    # "tr"
Config.GEMINI_API_KEY      # str | None  (.env'den)
Config.SUPPORTED_EXTENSIONS  # list[str], her uzantı '.' ile başlar (örn. ".pdf")
```

`SUPPORTED_EXTENSIONS` içerikleri kategoriler halinde: dokümanlar, tablo, görsel, ses, video, kod.

### 2.2 `core/converter.py` — `FileConverter`

Tüm metotlar `bool` döner (`True`=başarı, `False`=hata). Asla exception fırlatmaz; `logging` kullanır.

```python
from core.converter import FileConverter
fc = FileConverter()

fc.convert_pdf_to_docx(input_path: str, output_path: str) -> bool
fc.convert_csv_to_xlsx(input_path: str, output_path: str) -> bool
fc.convert_xlsx_to_csv(input_path: str, output_path: str) -> bool
fc.convert_image(input_path: str, output_path: str, target_format: str, quality: int = 100) -> bool
    # target_format: "PNG" | "JPG" | "JPEG" | "WEBP" | "BMP" (case-insensitive)
    # JPG -> dahili olarak JPEG'e map edilir; RGBA/P modlar otomatik RGB'ye çevrilir
fc.convert_docx_to_txt(input_path: str, output_path: str) -> bool
fc.convert_docx_to_pdf(input_path: str, output_path: str) -> bool
    # ⚠️ Windows + MS Word kurulu olmalı (docx2pdf bağımlılığı)
```

> **Eksik:** `convert_pdf_to_txt`, `convert_pdf_to_image`, `convert_mp3_to_wav` vb. **YOKTUR**. Kullanmadan önce yazmak gerekir.

### 2.3 `core/player.py` — `AudioConverter`

> ⚠️ **BİLİNEN BUG:** Dosyada iki adet `class AudioConverter` ve iki adet `__init__` tanımı vardır. Python yalnızca sonuncuyu kullanır, dolayısıyla **etkili API aşağıdaki gibidir**. Refactor görevi açıktır.

```python
from core.player import AudioConverter
ac = AudioConverter()

ac.ffmpeg_available      # bool, init'te shutil.which("ffmpeg") ile set edilir
ac.is_ffmpeg_installed() -> bool

ac.convert_audio(input_path: str, output_path: str, target_format: str) -> bool
    # target_format küçük harfle pydub'a verilir: "mp3" | "wav" | "ogg" | "flac" ...
ac.convert_mp3_to_ogg(input_path: str, output_path: str) -> bool
ac.convert_ogg_to_mp3(input_path: str, output_path: str) -> bool
```

FFmpeg yoksa tüm dönüşümler `False` döner ve `logging.error` ile loglanır.

### 2.4 `core/viewer.py` — `FileViewer`

> ⚠️ **Mimari İhlal Notu:** `viewer.py`, `streamlit`'i import eder (`display_*` metotları için). CONTEXT'teki "core/ Streamlit import etmez" kuralının **istisna**sıdır. Yeni `display_*` metotları **eklemek serbest** ama ham veri (`render_pdf`, `read_table`) ile UI metotlarını ayrı tutmaya dikkat.

```python
from core.viewer import FileViewer
fv = FileViewer()

# Saf data (UI bağımsız):
fv.render_pdf(pdf_path: str) -> list[bytes]   # her bir PNG sayfa byte dizisi
fv.read_table(file_path: str) -> pandas.DataFrame
    # .csv, .xls, .xlsx desteklenir; aksi halde ValueError

# Streamlit'e basan helper'lar:
fv.display_pdf(pdf_path: str) -> None         # st.image ile sayfa sayfa
fv.display_table(file_path: str) -> None      # st.dataframe
fv.display_audio(file_path: str, format: str = "audio/mp3") -> None
fv.display_video(file_path: str, format: str = "video/mp4") -> None
fv.display_text_document(file_path: str) -> None  # .txt -> text_area, .docx -> markdown
```

### 2.5 `core/ai_engine.py` — `AIEngine`

> **Güncelleme (2026-04-21, Issue #16):** Stub kaldırıldı, gerçek Gemini API entegrasyonu tamamlandı.

```python
from core.ai_engine import AIEngine
ai = AIEngine()

ai.summarize(text: str, length: str = "medium") -> str
    # length: "short" | "medium" | "long"
    # API key yoksa bilgilendirici fallback string döner
ai.answer_question(context: str, question: str) -> str
    # Context-feeding ile soru yanıtlama (RAG değil)
ai.extract_keywords(text: str, top_k: int = 10) -> list[str]
    # Anahtar kelime listesi; hata durumunda boş liste
ai.simplify(text: str, level: str = "intermediate") -> str
    # level: "basic" | "intermediate" | "advanced"
```

> `Config.GEMINI_API_KEY` eksikse metotlar exception fırlatmaz; bilgilendirici string/boş liste döner.
> Tüm metotlar `_call_gemini(prompt, system)` private helper üzerinden çalışır (DRY).
> 8 adet projeye özel system prompt `_SYSTEM_PROMPTS` dict'inde tanımlıdır.

### 2.6 `ui/dashboard.py` — `Dashboard`

```python
from ui.dashboard import Dashboard

dash = Dashboard(texts: dict)   # texts = languages.json'un seçili dil bloğu
dash.render_sidebar() -> None    # logo, dil seçici, navigasyon, file_uploader, file_history, settings
dash.render_main_area() -> None  # st.tabs ile Dönüştür / Görüntüle / AI sekmeleri
dash._add_to_file_history(filename: str) -> None  # internal
```

### 2.7 `ui/styles.py`

```python
from ui.styles import apply_custom_css
apply_custom_css()   # Tek fonksiyon, çağırınca tüm CSS enjekte olur
```

---

## 3. Session State Sözleşmesi (`st.session_state` Anahtarları)

`main.py → init_state()` aşağıdakileri **garanti eder**. Yeni kod yazarken **var olduklarını** varsayabilirsin.

| Anahtar | Tip | Varsayılan | Açıklama |
|:---|:---|:---|:---|
| `language` | `"tr"` \| `"en"` | `"tr"` | Aktif dil; değişince `st.rerun()` tetiklenir |
| `active_tab` | `str` | `"convert"` | Sekme adı (i18n çevirisinden alınır) |
| `uploaded_file` | `UploadedFile \| None` | `None` | Streamlit'in upload nesnesi |
| `file_history` | `list[dict]` | `[]` | Her item: `{"name": str, "time": "HH:MM:SS", "date": "DD.MM.YYYY"}` |

> **Önemli:** `init_state()` içinde `active_tab` başlangıç değeri `"convert"`'tir, ancak `Dashboard.render_sidebar()` içinde i18n çevirileri ile karşılaştırılır ve uyuşmazsa `nav_options[0]`'a (yine "Dönüştür") düşürülür. Yani pratikte güvenlidir.

---

## 4. i18n Kullanım Rehberi (Asla Hardcoded String Yazma!)

### 4.1 Çalışma Mantığı

```python
texts = load_languages()       # main.py — assets/languages.json[st.session_state.language]
st.write(texts.get("convert_tab", "Dönüştür"))  # her zaman .get() + fallback kullan
```

### 4.2 Şu Anda Mevcut Anahtarlar (her ikisi de tr ve en'de var)

```
__UI_HEADER__, app_title,
__NAV_SECTION__, sidebar_title, home_tab, convert_tab, view_tab, ai_tab,
__FILE_SECTION__, upload_file, file_uploaded,
__STATUS_SECTION__, status_architecture_in_progress,
__MSG_SECTION__, error_unsupported_file, success_conversion
```

> `__SECTION__` formatlı anahtarlar **görsel ayraç**tır, asla koddan çağrılmaz.

### 4.3 Yeni Bir UI Stringi Eklemek

1. `assets/languages.json` içine **hem `tr` hem `en` bloğuna** aynı snake_case anahtar adıyla ekle.
2. Anahtar adı varsa `tests/test_languages.py` paritesini bozmaz.
3. Eğer anahtar runtime için kritikse `tests/test_languages.py::test_required_runtime_keys_exist` içine ekle.
4. Kodda `texts.get("yeni_anahtar", "Fallback Türkçe")` ile çağır.

### 4.4 Bilinen Eksiklik

`ui/dashboard.py` içinde "🌐 Dil / Language", "📊 Navigasyon", "📁 Dosya Yükleme", "⏱️ Dosya Geçmişi", "⚙️ Ayarlar", "Henüz dosya yüklenmedi", "Lütfen önce yan menüden bir dosya yükleyin." gibi stringler **hardcoded Türkçe**'dir. Refactor görevi açıktır.

---

## 5. Veri Akış Diyagramları

### 5.1 Uygulama Açılışı

```
streamlit run main.py
└── main()
    ├── st.set_page_config(page_title=Config.APP_NAME, layout="wide")
    ├── apply_custom_css()                  # ui/styles.py
    ├── init_state()                        # session defaults
    ├── texts = load_languages()            # JSON oku, dile göre dilim al
    ├── Dashboard(texts)
    │   ├── .render_sidebar()               # dil/nav/upload/history
    │   └── .render_main_area()             # st.tabs(Dönüştür, Görüntüle, AI)
    └── (Streamlit her etkileşimde script'i baştan çalıştırır)
```

### 5.2 Dosya Dönüştürme Akışı (Issue #6 + #11 ile Tamamlandı)

```
Kullanıcı sidebar'dan dosya yükler
  → st.session_state.uploaded_file = UploadedFile
  → file_history listesine eklenir
  → Kullanıcı "Dönüştür" sekmesine geçer
  → _FORMAT_MAP ile uzantıya göre hedef formatlar st.selectbox'ta listelenir
  → _save_upload_to_temp() ile temp/'e yazılır
  → _dispatch_conversion() → FileConverter/AudioConverter çağrılır
  → bool sonuca göre st.success / st.error
  → Çıktı dosyası st.download_button ile sunulur
  → Path.unlink() ile geçici dosyalar temizlenir
```

### 5.3 Hata Yönetimi Felsefesi

| Katman | Hata Davranışı |
|:---|:---|
| `core/*` | Try/except ile yakalar, `logging.error` ile kaydeder, `False` veya `None`/sentinel döner. **Asla raise etmez** (tek istisna: `viewer.read_table` `ValueError` raise eder). |
| `ui/*` | `core` dönüşüne göre `st.error` / `st.success` / `st.warning` gösterir. |
| `main.py` | Yalnızca orchestration hatalarını yakalar (örn. `languages.json` yok). |

---

## 6. Bağımlılıklar (requirements.txt — `~=` zorunlu)

| Paket | Sürüm | Kullanan Modül | Açıklama |
|:---|:---|:---|:---|
| `streamlit` | `~=1.44.0` | `main`, `ui/*`, `viewer` | Web UI |
| `pandas` | `~=2.2.3` | `converter`, `viewer` | CSV/XLSX okuma-yazma |
| `openpyxl` | `~=3.1.5` | `converter` | Excel engine |
| `python-docx` | `~=1.1.2` | `converter`, `viewer` | DOCX okuma |
| `PyPDF2` | `~=3.0.1` | (rezerv, henüz aktif değil) | PDF utils |
| `pdf2docx` | `~=0.5.8` | `converter` | PDF→DOCX |
| `PyMuPDF` | `~=1.25.5` | `viewer` | `import fitz` ile PDF render |
| `Pillow` | `~=11.2.1` | `converter` | Görsel dönüşümü |
| `pydub` | `~=0.25.1` | `player` | Ses dönüşümü |
| `audioop-lts` | `~=0.2.1` | (Python 3.13+ pydub uyumu) | |
| `openai` | `~=1.70.0` | ~~`ai_engine`~~ (kullanılmıyor) | LLM client — `google-generativeai~=0.8.3` ile değiştirilmeli (Ali ile koordinasyon) |
| `python-dotenv` | `~=1.0.1` | `config/settings` | `.env` yükleme |
| `pytest` | `~=8.3.5` | `tests/*` | Test runner |

**Sistem Bağımlılıkları:**
- **FFmpeg** (ses dönüşümü için PATH'te olmalı)
- **MS Word** (yalnızca DOCX→PDF için, Windows)
- **docx2pdf** (requirements.txt'de yok ama `core/converter.py` import ediyor — eksiklik, eklenmeli)

> ⚠️ **Tutarsızlık:** `from docx2pdf import convert as docx2pdf_convert` kullanılıyor ama `requirements.txt`'de `docx2pdf` listelenmemiş. Yeni dönüşüm test ederken pip ile kurulmalı.

---

## 7. Kodlama Standartları (Modeller İçin Zorunlu Çek-Liste)

✅ **YAP:**
- `snake_case` fonksiyon/metot, `PascalCase` sınıf, `UPPER_SNAKE` sabit.
- Dönüşüm metodu yazıyorsan **`bool` döndür**, `try/except` ile sar, `logging` kullan.
- Önce spesifik exception (`FileNotFoundError`, `pd.errors.EmptyDataError`, `CouldntDecodeError`) sonra generic `Exception`.
- Yeni modül `core/`'a giriyorsa Streamlit import **etme**.
- Yeni UI string ekliyorsan `languages.json`'a hem `tr` hem `en` ekle.
- Yeni paket ekliyorsan `requirements.txt`'ye `paket~=X.Y.Z` formatında ekle.
- Modül başına Türkçe docstring (mevcut konvansiyona uy).

❌ **YAPMA:**
- Tek satır da olsa hardcoded UI stringi koyma (mevcut hardcoded'ları **artırma**).
- `core/` içinde `st.error`/`st.write` kullanma (viewer'daki istisna hariç, ama yeni metotta kaçın).
- `print()` ile log atma — `logging` kullan.
- `~=` yerine `==` veya pinsiz dependency yazma (test düşer).
- Aynı sınıfı iki kez tanımlama (`player.py` örneği bir bug, kopyalama).
- `!prototip/` klasörüne dokunma.
- Cömert emoji kullanma — sadece i18n string içindekileri koru.

---

## 8. Test Etme

```bash
# Tüm testler
python -m pytest tests -v

# Spesifik
python -m pytest tests/test_languages.py -v
python -m pytest tests/test_requirements.py -v
```

**Mevcut test setleri ne kontrol eder:**
- `test_languages.py`: `tr`/`en` kökleri var mı, anahtar setleri eşit mi, zorunlu runtime anahtarları eksik mi.
- `test_requirements.py`: tüm satırlarda `~=` var mı, duplicate dependency var mı.

**Manuel testler:**
- `python test.py` — image + ffmpeg
- `python test_core.py` — converter

> Yeni özellik için `tests/test_<modül>.py` ekle. Konvansiyon: dosya adı `test_` ile başlamalı, fonksiyon adı `test_` ile başlamalı.

---

## 9. Bilinen Sorunlar / Açık Görevler (Öncelik Sırasıyla)

| # | Konum | Tip | Açıklama | Durum |
|:---|:---|:---|:---|:---|
| 1 | `core/player.py` | 🐛 Bug | Çift `class AudioConverter` ve çift `__init__`. Birinciyi tamamen sil. | Açık (Issue #12) |
| 2 | `core/ai_engine.py` | ~~🔲 Stub~~ | ~~Gerçek Gemini/OpenAI entegrasyonu.~~ Issue #16 ile tamamlandı. | ✅ Tamamlandı |
| 3 | `requirements.txt` | ⚠️ Eksik | `docx2pdf` import ediliyor ama listede yok. `openai` → `google-generativeai` değişimi de gerekli. | Açık (Issue #15 + Ali koordinasyonu) |
| 4 | `ui/dashboard.py` | 🌐 i18n | Sidebar başlıkları (Navigasyon, Ayarlar, vb.) hardcoded; `languages.json`'a taşı. | Açık (Issue #14) |
| 5 | `main.py` tab içerikleri | ~~🔌 Bağlantı~~ | ~~"Dönüştürme modülü yükleniyor..." placeholder'ları~~ Dönüştür sekmesi bağlandı (Issue #6 + #11). | ✅ Tamamlandı |
| 6 | View sekmesi | 🔌 Bağlantı | Yüklenen dosyanın uzantısına göre `FileViewer.display_*` çağrılmalı. | Açık (Issue #13) |
| 7 | AI sekmesi | 🔌 Bağlantı | Text input + `AIEngine.answer_question` veya `summarize` butonu. | Açık (Issue #18) |
| 8 | `core/viewer.py` | 🏗️ Mimari | Streamlit import'u var; saf-data ile UI'yı ayır (opsiyonel refactor). | Açık |

---

## 10. Sık İhtiyaç Duyulan Kod Şablonları (Copy-Paste Hazır)

### 10.1 Yeni bir dönüşüm metodu eklemek (FileConverter)

```python
def convert_pdf_to_txt(self, input_path: str, output_path: str) -> bool:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(input_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for page in reader.pages:
                f.write(page.extract_text() or "")
                f.write("\n")
        logging.info(f"Başarılı: PDF -> TXT ({output_path})")
        return True
    except FileNotFoundError:
        logging.error(f"Hata: Girdi dosyası bulunamadı ({input_path})")
        return False
    except Exception as e:
        logging.error(f"Beklenmeyen Hata (PDF->TXT): {e}")
        return False
```

### 10.2 Sekme içinde converter çağırmak

```python
# ui/dashboard.py içinde tabs[0] altında
if st.session_state.uploaded_file and st.button("Dönüştür"):
    import tempfile, os
    from core.converter import FileConverter
    fc = FileConverter()
    src = st.session_state.uploaded_file
    in_path = os.path.join("temp", src.name)
    with open(in_path, "wb") as f:
        f.write(src.getbuffer())
    out_path = os.path.splitext(in_path)[0] + ".docx"
    if fc.convert_pdf_to_docx(in_path, out_path):
        st.success(self.texts.get("success_conversion", "Başarılı!"))
        with open(out_path, "rb") as f:
            st.download_button("İndir", f, file_name=os.path.basename(out_path))
    else:
        st.error(self.texts.get("error_unsupported_file", "Hata"))
```

### 10.3 Yeni bir i18n anahtarı eklemek

```jsonc
// assets/languages.json
"tr": {
    ...
    "btn_convert": "Dönüştür",
    "btn_download": "İndir",
    ...
},
"en": {
    ...
    "btn_convert": "Convert",
    "btn_download": "Download",
    ...
}
```

### 10.4 Yeni pytest

```python
# tests/test_converter.py
from pathlib import Path
from core.converter import FileConverter

def test_convert_csv_to_xlsx_success(tmp_path: Path):
    src = tmp_path / "in.csv"
    src.write_text("a,b\n1,2\n", encoding="utf-8")
    dst = tmp_path / "out.xlsx"
    assert FileConverter().convert_csv_to_xlsx(str(src), str(dst)) is True
    assert dst.exists()

def test_convert_csv_to_xlsx_missing_file(tmp_path: Path):
    assert FileConverter().convert_csv_to_xlsx(str(tmp_path/"nope.csv"), str(tmp_path/"x.xlsx")) is False
```

---

## 11. Ekip ve Modül Sahipliği

| Üye | Rol | Sahip Olduğu Dosyalar |
|:---|:---|:---|
| **Galip Efe Öncü** | Proje Mimarı | `main.py`, `config/settings.py`, `core/ai_engine.py` |
| **Said Hamza Turan** | Mantık & Algoritma | `core/converter.py`, `core/player.py` |
| **Abdulkadir Sar** | Görüntüleme Uzmanı | `core/viewer.py` |
| **Samet Demir** | UI/UX Tasarımcı | `ui/dashboard.py`, `ui/styles.py` |
| **Muhammed Ali Avcı** | QA & Test | `assets/languages.json`, `requirements.txt`, `tests/` |

> Başka birinin dosyasını değiştiriyorsan PR açıklamasında **modül sahibini etiketle**.

---

## 12. Sık Sorulanlar (Modeller İçin)

**S: Yeni bir dosya formatı dönüşümü ekleyeceğim. Nereden başlamalıyım?**
C: `core/converter.py` (belge/görsel) veya `core/player.py` (ses) içine `bool` dönen yeni metot ekle. Sonra UI bağlantısı için `ui/dashboard.py` `tabs[0]` altında bir buton + i18n stringi ekle.

**S: Streamlit'i `core/`'a import edebilir miyim?**
C: HAYIR. Tek istisna `core/viewer.py`'de `display_*` metotları (legacy). Yeni `core/` modülünde import etme.

**S: `assets/languages.json`'da yalnızca `tr`'ye yeni anahtar eklersem ne olur?**
C: `pytest` düşer (`test_language_keys_are_symmetric_between_tr_and_en`). Her zaman ikisine birden ekle.

**S: `Config.GEMINI_API_KEY` `None` ise ne yapmalıyım?**
C: AI çağrısı öncesi kontrol et: `if not Config.GEMINI_API_KEY: return "API key missing"` gibi graceful fallback.

**S: Geçici dosyaları nereye yazmalıyım?**
C: `temp/` klasörüne. Git tarafından ignore edilir.

**S: `docx2pdf` çalışmıyor, ne olmuş?**
C: Yalnızca Windows + MS Word kurulu sistemlerde çalışır. Diğer platformlarda `convert_docx_to_pdf` her zaman `False` döner — beklenen davranış.

**S: `st.rerun()` ne zaman çağırılır?**
C: Yalnızca `language` değişiminde (`render_sidebar` içinde otomatik). Başka yerlerde çağırma — gereksiz reload yapar.

---

## 13. Diğer Dökümanlara Yönlendirme

Bu dosya tek başına yetersiz kaldığında:

- **`docs/CONTEXT.md`** — Daha derin teknik detay (EN).
- **`docs/PRD.md`** — Ürün gereksinimleri ve kabul kriterleri (EN).
- **`docs/PROJECT_DETAILS.md`** — Üst düzey ürün vizyonu (TR).
- **`docs/ROADMAP.md`** — 6 haftalık sprint planı + issue listesi (TR).
- **`docs/TASK_DISTRIBUTION.md`** — Modül sahipliği ve sorumluluklar (TR).
- **`docs/WEEKLY_PROGRESS_ALI.md`** — QA haftalık raporu (EN).
- **`README.md`** — Kurulum + kullanıcı belgesi (EN).

---

> **Bu dosya bir kod-okuma-bypass'ıdır.** Burada listelenen sözleşmeler güncel olduğu sürece, model `core/`, `ui/`, `config/` içindeki herhangi bir `.py` dosyasını açmadan doğru çalışan kod yazabilir.
> Kodda anlam veremediğin bir davranış varsa **önce bu dosyayı kontrol et, ardından ilgili kaynak dosyayı oku.**
