# 🗺 Universal File Workstation: 6 Haftalık Geliştirme Yol Haritası

> **Son Güncelleme:** 2026-04-21
> 💡 Hızlı oryantasyon için `docs/AGENT_GUIDE.md` (modeller/yeni gelen geliştiriciler için tek dosyalık özet) öncelikli okumadır.

---

## 📅 Proje Planı Tanıtımı
Bu döküman, projenin 6 haftalık hızlandırılmış geliştirme planını ve üyelerin haftalık odak noktalarını içerir.

| Hafta | Odak Noktası | Ana Hedef | Durum |
| :--- | :--- | :--- | :--- |
| **Hafta 1** | **Temel Altyapı** | Altyapı, Arayüz İskeleti ve Temel Fonksiyonların kurulması. | ✅ Tamamlandı |
| **Hafta 2** | **Dosya İşleme** | Dosya İşleme Motorları (PDF, DOCX, CSV vb.) geliştirilmesi. | ✅ Tamamlandı |
| **Hafta 3** | **Entegrasyon & Bug-Fix** | UI ↔ Core bağlantısı, `player.py` refaktörü, eksik dependency'ler, Görüntüle sekmesi dispatcher. | 🔜 Aktif Sprint |
| **Hafta 4** | **Yapay Zeka** | Gemini API entegrasyonu, özet/Q&A/anahtar kelime, AI sekmesi UI. | ⏳ Planlı |
| **Hafta 5** | **UI/UX Cilalama & Test Genişletme** | i18n tamamlanması, açık tema, loading state'ler, unit & smoke test'ler. | ⏳ Planlı |
| **Hafta 6** | **Paketleme & Yayın** | PyInstaller `.exe`, kullanıcı dokümantasyonu, regresyon testi, v0.1.0 release. | ⏳ Planlı |

---

# 🛠 1. Hafta (Sprint 1) Görev Listesi (Issues)

### 🔴 Issue #1: Proje Mimarisinin Kurulması ve Session State
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** Proje iskeletinin, session state kontrolünün ve yapılandırma sisteminin entegrasyonu.
*   **Görevler:**
    - [x] `main.py` dosyasının temel Streamlit yapısını oluştur.
    - [x] Uygulama genelinde kullanılacak `session_state` kontrol mekanizmasını (yüklenen dosya takibi, aktif sayfa/mod bilgisi) kurgula.
    - [x] `config/settings.py` dosyasını tamamla.
    - [x] `.env` dosyasından API anahtarlarını güvenli çekecek `python-dotenv` entegrasyonunu yap.
    - [x] QA ile koordineli olarak i18n dil desteği altyapısını devreye al.

### 🟠 Issue #2: Dönüştürme Algoritmaları ve Ses İşleme
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** Temel dönüştürme fonksiyonlarının altyapısı ve medya dosyaları için çevresel bağımlılıkların (FFmpeg) kontrolü.
*   **Görevler:**
    - [x] `core/converter.py` içinde PDF-to-Text ve CSV-to-XLSX dönüşümleri için kütüphane seçimlerini yap.
    - [x] Dönüştürme fonksiyonlarının girdi-çıktı imzalarını ve hata yakalama (try-except) yapısını kur.
    - [x] `core/player.py` içinde sistemde `ffmpeg` yüklü olup olmadığını denetleyen doğrulama fonksiyonunu yaz.
    - [x] Temel ses dönüşüm (MP3/WAV) iskeletini oluştur.

### 🟡 Issue #3: PDF Rendering ve Tablo Veri Görüntüleme
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** Belge ve elektronik tablo dosyalarının Streamlit arayüzünde temiz ve görsel bir şekilde sunulması.
*   **Görevler:**
    - [x] `core/viewer.py` içinde `PyMuPDF` (fitz) kullanarak PDF dosyalarını imaja çevirme fonksiyonunu yaz.
    - [x] PDF sayfalarının Streamlit üzerinde `st.image` ile gösterilmesi için PoC oluştur (`FileViewer.display_pdf`).
    - [x] Pandas kullanarak CSV ve Excel dosyalarının okunup `st.dataframe` üzerinden temiz sunulmasını sağla (`FileViewer.display_table`).
    - [x] Veri tipi uyumsuzluklarını önlemek için temel bir validator yaz (`read_table` -> `ValueError`).

### 🔵 Issue #4: Ana Dashboard ve Görsel Tasarım Sistemi
*   **Sorumlu:** **Samet Demir**
*   **Özet:** Uygulamanın navigasyon düzenini kurmak ve görsel bütünlüğü sağlamak için CSS enjeksiyonlarını başlatmak.
*   **Görevler:**
    - [x] `ui/dashboard.py` içinde `st.sidebar` ve ana içerik alanının yerleşimini yap (`Dashboard.render_sidebar` + `render_main_area`).
    - [x] Üç ana sekmeyi (Dönüştür, Görüntüle, AI) `st.tabs` kullanarak oluştur.
    - [x] `ui/styles.py` içinde projenin kurumsal renk paleti ve tipografi standartlarını CSS olarak tanımla.
    - [x] Streamlit'in standart dışı alanlarını özelleştirecek CSS enjeksiyonlarını başlat.

### 🟢 Issue #5: Kalite Güvence ve Test Otomasyonu
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** Çoklu dil desteğinin testleri ve uygulamanın sistem test otomasyonunu (pytest) yapılandırmak.
*   **Görevler:**
    - [x] `assets/languages.json` dosyasını hem Türkçe hem İngilizce olacak şekilde tanımla.
    - [x] Uygulama içindeki metinlerin dinamik olarak bu dosyadan çekilmesi süreçlerini test et.
    - [x] `pytest` çalışma ortamını yapılandır.
    - [ ] Temel modüllerin import testlerini ve `main.py` çalışabilirliğini doğrulayan Smoke Test senaryolarını yaz. (TODO)

---

# 🚀 2. Hafta (Sprint 2) Görev Listesi (Issues)

### 🔴 Issue #6: Arayüz ve Dönüştürücü Modüllerinin Entegrasyonu
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** `ui/dashboard.py` içerisindeki dönüştürme (Convert) ve görüntüleme (View) sekmelerinin altyapısını Said ve Abdulkadir'in modülleriyle bağlamak.
*   **Görevler:**
    - [x] `main.py` "Dönüştür" sekmesine `core/converter.py` modülünü import edip bağla.
    - [x] Streamlit arayüzünden seçilen dosya hedefine göre `converter.py` fonksiyonlarını tetikleyen buton ve durum yönetimini ekle.
    - [x] `ai_engine.py` için temel Gemini API bağlantı taslağını yaz ve System Prompt oluşturarak test altyapısını kur.

### 🟠 Issue #7: Gelişmiş Dönüştürme Motorları (Resim & Belge)
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** Proje detaylarındaki eksik görsel ve diğer metin formatı dönüşümlerini (PNG/JPG/WEBP, DOCX->PDF) kodlamak.
*   **Görevler:**
    - [x] `core/converter.py` içine Pillow (PIL) kullanarak PNG <-> JPG <-> WEBP dönüşüm imkanlarını ekle.
    - [x] DOCX dosyalarından PDF ve TXT formatına dönüştürme fonksiyonlarını yaz.
    - [x] Arayüzde kalite seçeneği (görseller için %50, %80 vb.) alınabilecek şekilde fonksiyon imzalarına argüman (`quality: int`) ekle.
    - [x] `player.py` dosyasındaki eksik kalan MP3 <-> OGG eklentilerini tamamla.

### 🟡 Issue #8: Arayüz Görüntüleme Bileşenlerinin (UI) Bağlanması
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** `viewer.py` arka planında oluşturulan render çıktılarının Streamlit arayüzünde kullanıcıya sunulması.
*   **Görevler:**
    - [x] Dönüştürülen veya yüklenen PDF sayfalarını `st.image` ile art arda gösterecek bir loop kur (`display_pdf`).
    - [x] Excel/CSV verilerini `pd.DataFrame` üzerinden okuduktan sonra `st.dataframe` ile arayüze bas (`display_table`).
    - [x] `st.audio` ve `st.video` kullanarak medya oynatma araçlarının arayüzdeki entegrasyonu için kod taslaklarını hazırla (`display_audio`, `display_video`).
    - [x] DOCX veya TXT içeriğini okuyup UTF-8 olarak decodelayan ve `st.markdown` veya `st.text_area` ile gösteren fonksiyonu yaz (`display_text_document`).
    - [ ] Bu metotları `Dashboard.render_main_area()` "Görüntüle" sekmesinde dosya uzantısına göre dispatcher ile bağla. (TODO)

### 🔵 Issue #9: Gelişmiş Dashboard ve Dosya Yükleme Paneli
*   **Sorumlu:** **Samet Demir**
*   **Özet:** Geçiçi `st.radio` navigasyonunu kaldırıp modern bir dashboard sidebar kalıbına geçmek.
*   **Görevler:**
    - [x] `ui/dashboard.py` içindeki `render_sidebar()` fonksiyonunu yaz, "Dosya Geçmişi" + dil seçimi + ayarlar oraya eklendi.
    - [x] `ui/dashboard.py` içindeki `render_main_area()` kısmında `st.tabs` kullanarak (Dönüştür, Görüntüle, AI) sekmelerini asıl yerine oturt.
    - [x] Ana ekrandaki dosya yükleyici (`st.file_uploader`) kısmına CSS ekleyerek daha estetik bir sürükle-bırak kutusu görünümü ver (`ui/styles.py` `[data-testid="stFileUploadDropzone"]`).
    - [x] Galip Efe ile eş zamanlı çalışarak tasarımlarının `main.py` içerisine import edilmesini sağla (`from ui.dashboard import Dashboard`).
    - [ ] Sidebar'daki hardcoded Türkçe etiketleri (`🌐 Dil / Language`, `📊 Navigasyon`, `📁 Dosya Yükleme`, `⏱️ Dosya Geçmişi`, `⚙️ Ayarlar`) `assets/languages.json`'a taşı. (TODO)

### 🟢 Issue #10: Modül Entegrasyon Testleri ve Kalite Güvencesi
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** Yeni dönüştürücüler için gelişmiş testler ve projenin resmi sistem testinin başlatılması.
*   **Görevler:**
    - [x] `pytest.ini` ve test konfigürasyonlarını kurarak resmi test altyapısına geçiş yap.
    - [ ] DOCX -> PDF ve Görsel (JPG/PNG/WEBP) dönüştürme modülleri için birim (unit) testleri yaz.
    - [x] İngilizce/Türkçe string hatalarını veya çevirisi unutulan kelimeleri `languages.json` dosyasına ekle.
    - [x] Uygulamanın büyük dosyalarda (>50MB) çöküp çökmediğini görmek için manuel duman testleri (smoke test) yürüt.

---

# 🔧 3. Hafta (Sprint 3) Görev Listesi (Issues)

> **Sprint Hedefi:** Tamamlanmış backend modüllerini Streamlit UI ile **uçtan uca bağlamak**, `player.py` çift sınıf bug'ını gidermek, eksik bağımlılığı (`docx2pdf`) eklemek ve Görüntüle sekmesinin dosya uzantısına göre doğru `FileViewer.display_*` metodunu çağırmasını sağlamak.
> **Definition of Done:** Bir kullanıcı `streamlit run main.py` ile uygulamayı açabilmeli; PDF / DOCX / CSV / XLSX / Image / Audio / Video yükleyip Dönüştür sekmesinde dönüştürme yapabilmeli, Görüntüle sekmesinde önizleyebilmeli. Tüm pytest'ler yeşil.

### 🔴 Issue #11: Dönüştür Sekmesinin `core/converter.py` ile Tam Entegrasyonu
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** "Dönüştür" sekmesindeki placeholder metni kaldırıp, yüklenen dosyanın türüne göre hedef format seçtiren, butonla `FileConverter` metodlarını tetikleyen ve sonucu `st.download_button` ile kullanıcıya sunan tam akışı kurmak.
*   **User Story:** _"Bir kullanıcı olarak, yüklediğim PDF/DOCX/CSV/XLSX/Image/Audio dosyamın hangi formatlara dönüştürülebileceğini görmek; tek bir butonla dönüşümü tetiklemek ve sonuç dosyasını aynı sayfadan indirmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [x] Dönüştür sekmesi, `st.session_state.uploaded_file` boşsa kullanıcıyı i18n stringi ile dosya yüklemeye yönlendirir.
    - [x] Yüklü dosyanın uzantısına göre **geçerli hedef formatlar** dinamik olarak `st.selectbox` içinde listelenir (örn. `.pdf` → `["docx"]`, `.csv` → `["xlsx"]`, image → `["png", "jpg", "webp"]`).
    - [x] "Dönüştür" butonuna basıldığında dosya `temp/` altına yazılır, ilgili `FileConverter.*` metodu çağrılır.
    - [x] Başarı durumunda `i18n["success_conversion"]` ile `st.success` ve `st.download_button` gösterilir.
    - [x] Başarısızlıkta `i18n["error_unsupported_file"]` veya benzeri ile `st.error` gösterilir; uygulama crash etmez.
    - [x] Dönüşüm sırasında `st.spinner` ile kullanıcıya geri bildirim verilir.
*   **Görevler:**
    - [x] `ui/dashboard.py` `render_main_area()` `tabs[0]` bloğuna dispatcher mantığını yaz (uzantı → hedef format listesi).
    - [x] `temp/` klasörüne güvenli yazma yardımcı fonksiyonu ekle (`_save_upload_to_temp(uploaded_file) -> str`).
    - [x] Her dönüşüm tipi için `FileConverter` çağrısını wrap eden ince bir router metot ekle (`_dispatch_conversion(input_path, target_format) -> bool`).
    - [x] `assets/languages.json`'a yeni anahtarlar: `btn_convert`, `btn_download`, `select_target_format`, `converting_in_progress` (hem TR hem EN).
    - [x] Geçici dosyaların temizlenmesi için `Path.unlink(missing_ok=True)` cleanup stratejisi.

### 🟠 Issue #12: `core/player.py` Refaktörü ve Eksik Audio Dönüşümleri
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** `player.py` içindeki çift `class AudioConverter` ve çift `__init__` bug'ını temizlemek; MP3 ↔ WAV kısayol metotlarını eklemek ve eksik `docx2pdf` bağımlılığı için Said'in kullandığı paket sürümünü Ali ile koordineli `requirements.txt`'ye eklenmesi için raporlamak.
*   **User Story:** _"Bir geliştirici olarak, `core/player.py` dosyasını okuduğumda yalnızca tek bir net `AudioConverter` sınıfı görmek; MP3-WAV ve diğer yaygın ses dönüşümlerini kısayol metotlarla çağırabilmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `core/player.py` içinde **yalnızca bir** `class AudioConverter` ve **bir** `__init__` bulunur.
    - [ ] Modül başındaki gereksiz `import shutil/logging` tekrarları temizlenir.
    - [ ] `convert_mp3_to_wav` ve `convert_wav_to_mp3` kısayol metotları eklenir (`convert_audio` üzerinden).
    - [ ] FFmpeg yokken tüm metotlar `False` döner ve `logging.error` ile loglar — davranış değişmez.
    - [ ] `pytest tests -v` yeşil; manuel `python test.py` çalışır.
    - [ ] PR açıklamasında `docx2pdf` paketinin gerçek kullanım sürümü Ali'ye iletilir.
*   **Görevler:**
    - [ ] `player.py` çift sınıf tanımını sil; tek `AudioConverter` bırak.
    - [ ] `is_ffmpeg_installed()` ve `__init__` mantığını birleştir.
    - [ ] `convert_mp3_to_wav` + `convert_wav_to_mp3` kısayol metotlarını ekle.
    - [ ] `tests/test_player.py` taslağı: `is_ffmpeg_installed()` mock'u ile FFmpeg yok senaryosu (`False` dönmeli).
    - [ ] `core/converter.py` üstüne kısa modül docstring'i + import düzeni iyileştirmesi (opsiyonel, küçük temizlik).

### 🟡 Issue #13: Görüntüle Sekmesi — Dosya Tipi Dispatcher ve `display_image` Metodu
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** `Dashboard.render_main_area()` "Görüntüle" sekmesinde, yüklenen dosyanın uzantısına göre doğru `FileViewer.display_*` metodunu otomatik çağıran dispatcher mantığını yazmak; eksik olan `display_image` metodunu `core/viewer.py`'ye eklemek.
*   **User Story:** _"Bir kullanıcı olarak, hangi dosyayı yüklersem yükleyeyim Görüntüle sekmesine geçtiğimde dosyanın uygun önizleyicide (PDF→sayfa görselleri, CSV→tablo, MP3→oynatıcı, PNG→görsel, DOCX→metin) gösterilmesini istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `core/viewer.py`'ye `display_image(file_path: str)` metodu eklenir; `st.image` ile görseli `use_container_width=True` gösterir.
    - [ ] "Görüntüle" sekmesi yüklü dosya uzantısına göre uygun `display_*` metodunu çağırır (mapping: `.pdf→display_pdf`, `.csv/.xls/.xlsx→display_table`, `.mp3/.wav/.ogg→display_audio`, `.mp4/.mov/.webm→display_video`, `.png/.jpg/.jpeg/.webp/.bmp→display_image`, `.txt/.docx→display_text_document`).
    - [ ] Desteklenmeyen uzantı için `i18n["error_unsupported_file"]` ile `st.warning`.
    - [ ] Yüklenen dosya `temp/` altına yazılır (Galip Efe'nin yardımcı fonksiyonu kullanılır).
    - [ ] Büyük PDF (>20 sayfa) için `st.spinner` veya progress bar gösterilir.
*   **Görevler:**
    - [ ] `core/viewer.py` → `display_image(file_path)` metodunu ekle.
    - [ ] `ui/dashboard.py` `tabs[1]` bloğuna `_dispatch_viewer(uploaded_file)` mantığını yaz.
    - [ ] Audio/video MIME tipi seçimi için `mimetypes` modülü ile dinamik `format` belirleme.
    - [ ] PDF render'ı için spinner: `with st.spinner(texts.get("loading_preview", "Yükleniyor...")): ...`
    - [ ] `display_text_document` içindeki "Belge İçeriği", "Bu metin formatı desteklenmiyor." string'lerini i18n'e taşı (Ali ile koordinasyon).

### 🔵 Issue #14: Sidebar i18n Tamamlama ve Settings Expander İçeriği
*   **Sorumlu:** **Samet Demir**
*   **Özet:** `ui/dashboard.py`'deki tüm hardcoded Türkçe sidebar etiketlerini (`🌐 Dil / Language`, `📊 Navigasyon`, `📁 Dosya Yükleme`, `⏱️ Dosya Geçmişi`, `⚙️ Ayarlar`, "Henüz dosya yüklenmedi") `assets/languages.json`'dan çekecek şekilde refaktör etmek; Ayarlar expander'ına işlevsel öğeler eklemek.
*   **User Story:** _"İngilizce kullanıcı olarak, sidebar'daki tüm metinlerin de İngilizceye çevrilmesini; Ayarlar bölümünün gerçek seçenekler (varsayılan kalite, otomatik temizleme süresi vb.) sunmasını istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] Sidebar'daki **hiçbir kullanıcıya görünür string hardcoded değil**; tümü `texts.get()` ile çağrılır.
    - [ ] Yeni i18n anahtarları (TR + EN): `sidebar_language`, `sidebar_navigation`, `sidebar_upload`, `sidebar_history`, `sidebar_settings`, `history_empty`, `history_files_count`, `settings_theme`, `settings_about`, `settings_default_quality`, `settings_clear_history`.
    - [ ] Ayarlar expander'ında: (a) varsayılan görsel kalite slider'ı (`st.slider`, 1-100, default 100, `st.session_state.default_quality`), (b) "Geçmişi Temizle" butonu (`st.button` → `file_history = []`), (c) versiyon bilgisi.
    - [ ] Tema seçici hâlâ `disabled=True` olabilir ama tooltip ile "Açık tema Sprint 5'te gelecek" notu göster.
    - [ ] Dil değiştirildiğinde sidebar'daki tüm metinler anında güncellenir (`st.rerun()` zaten mevcut).
*   **Görevler:**
    - [ ] `assets/languages.json` yeni anahtarları ekle (Ali ile koordineli).
    - [ ] `ui/dashboard.py` `render_sidebar()` içindeki tüm `st.markdown("**...**")` çağrılarını `texts.get()` ile değiştir.
    - [ ] `_add_to_file_history` davranışı korunur; "Geçmişi Temizle" butonu yalnızca `file_history` doluysa gösterilir.
    - [ ] `settings_default_quality` slider'ı `Issue #11` Convert sekmesindeki `convert_image` çağrısı için varsayılan değer olarak okunur (Galip Efe ile koordinasyon).

### 🟢 Issue #15: Eksik Bağımlılık + Smoke Test + Yeni i18n Paritesi
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** `requirements.txt`'ye Said'in raporladığı `docx2pdf` sürümünü eklemek; `main.py` ve tüm `core/` modüllerinin import edilebildiğini doğrulayan smoke test'leri yazmak; Sprint 3'te eklenen yeni i18n anahtarlarının TR/EN paritesini doğrulamak.
*   **User Story:** _"Bir QA olarak, yeni geliştirici makinesinde `pip install -r requirements.txt && pytest` komutu hatasız çalıştığında projenin tüm modüllerinin yüklenebildiğini ve dil dosyasının tutarlı olduğunu garanti etmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `requirements.txt` içine `docx2pdf~=<sürüm>` eklenir, `~=` operatörü kuralı bozulmaz.
    - [ ] `tests/test_smoke.py` oluşturulur ve aşağıdaki testleri içerir: `test_main_imports`, `test_core_modules_import`, `test_ui_modules_import`, `test_config_class_attrs`.
    - [ ] `tests/test_languages.py::test_required_runtime_keys_exist` listesine Sprint 3'te eklenen kritik anahtarlar (`btn_convert`, `sidebar_language`, vb.) eklenir.
    - [ ] `python -m pytest tests -v` lokalde **0 fail** verir.
    - [ ] Sprint sonu manuel smoke checklist (Word olmayan ortamda DOCX→PDF beklenen `False`, FFmpeg olmayan ortamda audio dönüşüm `False`) `WEEKLY_PROGRESS_ALI.md`'ye işlenir.
*   **Görevler:**
    - [ ] `requirements.txt` güncelle.
    - [ ] `tests/test_smoke.py` yaz.
    - [ ] Sprint 3 i18n paritesini PR review'da doğrula.
    - [ ] Bu sprint sonunda manuel test raporunu `docs/WEEKLY_PROGRESS_ALI.md` altına yeni hafta bloğu olarak ekle.

---

# 🤖 4. Hafta (Sprint 4) Görev Listesi (Issues)

> **Sprint Hedefi:** `core/ai_engine.py` stub'ını gerçek **Gemini API** ile değiştirmek; AI sekmesinde özet, soru-cevap, anahtar kelime ve sadeleştirme akışlarını çalışır hale getirmek.
> **Definition of Done:** Geçerli `GEMINI_API_KEY` olan kullanıcı PDF/DOCX/TXT yükleyip AI sekmesinden özet alabilmeli, doküman içerikli soru sorabilmeli, anahtar kelime listesi görebilmeli. API key yokken kullanıcıya net hata mesajı gösterilmeli.

### 🔴 Issue #16: Gemini API Entegrasyonu ve `AIEngine` Tam Implementasyonu
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** `core/ai_engine.py` içindeki placeholder metotları gerçek Gemini API çağrılarıyla değiştirmek; özet, Q&A, anahtar kelime çıkarma ve sadeleştirme metotlarını eklemek; API key yokluğu / quota / network hatalarını graceful handle etmek.
*   **User Story:** _"Bir kullanıcı olarak, yüklediğim metin tabanlı dosyanın AI tarafından özetlenmesini, içeriği hakkında doğal dilde soru sorabilmeyi ve anahtar kelimelerini görmeyi istiyorum."_
*   **AC (Acceptance Criteria):**
    - [x] `AIEngine.summarize(text: str, length: str = "medium") -> str` gerçek Gemini çağrısı yapar; `length ∈ {"short", "medium", "long"}`.
    - [x] `AIEngine.answer_question(context: str, question: str) -> str` doğrudan context-feeding (RAG değil) ile çalışır.
    - [x] `AIEngine.extract_keywords(text: str, top_k: int = 10) -> list[str]` çalışır.
    - [x] `AIEngine.simplify(text: str, level: str = "intermediate") -> str` çalışır (`basic | intermediate | advanced`).
    - [x] `Config.GEMINI_API_KEY` `None` veya boşsa metotlar `RuntimeError` fırlatmaz; `i18n["error_api_key_missing"]` döner.
    - [x] Network/quota/API hataları `try/except`'le yakalanır, logging.error + kullanıcı dostu string döner.
    - [x] System prompt projeye özel hazırlanır (Türkçe/İngilizce çıktı dil yönetimi dahil).
    - [x] Tek bir `_call_gemini(prompt: str, system: str | None = None) -> str` private helper tüm metotlar tarafından kullanılır (DRY).
*   **Görevler:**
    - [ ] `requirements.txt`'ye `google-generativeai~=<sürüm>` ekle (Ali ile koordineli).
    - [x] `_call_gemini` helper'ını yaz; model: `gemini-1.5-flash` (cost-efficient).
    - [x] 4 public metodu implement et + docstring + tip ipuçları.
    - [x] System prompt'ları modül seviyesinde sabit olarak tanımla (`_SYSTEM_PROMPTS: dict[str, str]`).
    - [x] `tests/test_ai_engine.py` taslağı: `monkeypatch` ile `_call_gemini` mock'u → public metotların doğru parametreyi geçirdiğini test et.

### 🟠 Issue #17: Toplu Dönüşüm + PDF Sayfa Çıkarma + PDF Birleştirme
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** `core/converter.py`'ye batch (toplu) dönüşüm jenerik metodu, PDF sayfalarını PNG/JPG olarak export eden metot ve birden fazla PDF'i tek dosyada birleştiren metot eklemek.
*   **User Story:** _"Bir kullanıcı olarak, 10 görsele aynı anda WEBP'e çevirme, bir PDF'in her sayfasını ayrı PNG olarak alma ve birden çok PDF'i tek dosyada birleştirme imkânı istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `FileConverter.batch_convert(input_paths: list[str], output_dir: str, target_format: str, **kwargs) -> dict[str, bool]` çalışır; her dosya için sonucu döner.
    - [ ] `FileConverter.pdf_to_images(input_path: str, output_dir: str, image_format: str = "png", dpi: int = 150) -> list[str]` PyMuPDF ile her sayfayı kaydeder ve dosya yollarını döner.
    - [ ] `FileConverter.merge_pdfs(input_paths: list[str], output_path: str) -> bool` PyPDF2 veya PyMuPDF ile birleştirir.
    - [ ] Hatalar mevcut konvansiyona uygun: `bool` döner / boş liste döner; `logging.error` ile loglanır.
    - [ ] `tests/test_converter.py` içine her yeni metot için en az 1 success + 1 failure unit testi.
*   **Görevler:**
    - [ ] `pdf_to_images` ve `merge_pdfs` için PyPDF2 mı yoksa PyMuPDF mı kullanılacağını seç (perf + bağımlılık trade-off).
    - [ ] `batch_convert` içinde `convert_image / convert_csv_to_xlsx` gibi mevcut metotları dispatch et.
    - [ ] `__init__` ya da modül seviyesi `_CONVERSION_REGISTRY: dict[tuple[str, str], Callable]` ile dispatch tablosu oluştur (opsiyonel ama önerilir).
    - [ ] PR açıklamasında PDF birleştirme için seçilen kütüphaneyi gerekçeli yaz.

### 🟡 Issue #18: AI Sekmesi UI — Özet / Q&A / Anahtar Kelime Akışları
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** `Dashboard.render_main_area()` AI sekmesinde, yüklü metin tabanlı dosyadan içerik çıkararak `AIEngine` metotlarını tetikleyen interaktif paneli kurmak. Metin çıkarma `FileViewer`'ın yardımcı fonksiyonları + `core/converter.py` `convert_docx_to_txt` türevleriyle yapılır.
*   **User Story:** _"Bir kullanıcı olarak, AI sekmesinde dosya tipi destekleniyorsa 3 buton (Özetle / Soru Sor / Anahtar Kelime) görmek; sonuçları sayfada okuyabilir + kopyalayabilir formda almak istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] AI sekmesi yalnızca `.pdf / .docx / .txt / .csv` (text-only) dosyalar için aktiftir; aksi halde `st.info` ile bilgi gösterir.
    - [ ] Yüklü dosyadan ham metin çıkaran helper `_extract_text(file_path: str) -> str` `core/viewer.py`'ye eklenir (PDF için PyMuPDF ile `page.get_text()`, DOCX için `python-docx`, TXT için doğrudan okuma).
    - [ ] Üç ana eylem: `st.button("Özetle")`, `st.text_input + st.button("Soru Sor")`, `st.button("Anahtar Kelime Çıkar")`.
    - [ ] `summarize` butonu için uzunluk seçici (`st.radio: ["short", "medium", "long"]`).
    - [ ] Cevaplar `st.markdown` veya `st.text_area` ile gösterilir; uzun cevap için `st.expander` kullanılabilir.
    - [ ] Tüm uzun çağrılar `st.spinner` ile sarılır.
    - [ ] Hata durumlarında `i18n["error_api_key_missing"]` veya `i18n["error_ai_request_failed"]` ile `st.error`.
*   **Görevler:**
    - [ ] `core/viewer.py`'ye `_extract_text` (veya public `extract_text`) ekle.
    - [ ] `ui/dashboard.py` `tabs[2]` bloğunu yeniden yaz.
    - [ ] `assets/languages.json` yeni anahtarlar: `ai_summarize_btn`, `ai_ask_btn`, `ai_keywords_btn`, `ai_summary_length`, `ai_question_placeholder`, `error_ai_request_failed`, `error_api_key_missing`, `ai_unsupported_file_type`.
    - [ ] Çıktı kopyalama için `st.code` veya `st.text_area` kullanımını seç.

### 🔵 Issue #19: Loading State'ler, Toast Bildirimleri ve Tab İçeriği Cilalama
*   **Sorumlu:** **Samet Demir**
*   **Özet:** Tüm uzun süren operasyonlara (`convert_*`, `display_pdf`, AI çağrıları) tutarlı `st.spinner` + `st.toast` deneyimi getirmek; tab başlıklarını CSS ile daha belirgin hale getirmek; başarı/hata renklerini design token'lara bağlamak.
*   **User Story:** _"Bir kullanıcı olarak, herhangi bir işlem 1 saniyeden uzun sürdüğünde 'çalışıyor' geri bildirimini görmek; başarı durumunda kısa bir toast almak; hata mesajlarının ekranda kaybolmadan kalmasını istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] Tüm `FileConverter` ve `AIEngine` çağrıları `st.spinner(texts.get("loading_<context>"))` ile sarılır.
    - [ ] Başarı bildirimleri için merkezi helper: `notify_success(msg: str)` → hem `st.toast` hem `st.success`.
    - [ ] Hata bildirimleri kalıcı (`st.error` her zaman gösterilir).
    - [ ] `ui/styles.py`'ye yeni CSS: `[data-testid="stAlert"]` için brand renklere uygun başarı/hata varyantları.
    - [ ] Tab başlıklarına emoji + bold + alt çizgi gradient: zaten var olan stiller iyileştirilir, hover transition'ı 200ms'ye düşürülür.
    - [ ] Yeni i18n anahtarları: `loading_converting`, `loading_rendering`, `loading_ai_processing`, `notify_success_default`.
*   **Görevler:**
    - [ ] `ui/dashboard.py`'ye `notify_success` / `notify_error` helper'ları ekle (modül seviyesi fonksiyon olabilir).
    - [ ] Tüm tab handler'larını helper'ları kullanacak şekilde refaktör et.
    - [ ] CSS güncellemeleri.
    - [ ] Galip Efe / Said / Abdulkadir ile çakışmamak için Sprint sonunda merge sırası planla (Samet → diğerlerinin PR'ları sonrası).

### 🟢 Issue #20: AI ve Yeni Converter Metotları için Unit Testler
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** `AIEngine` ve `FileConverter`'ın yeni metotları (`batch_convert`, `pdf_to_images`, `merge_pdfs`) için unit testler yazmak; AI çağrıları mock'lanır, gerçek API çağrısı CI'da yapılmaz.
*   **User Story:** _"Bir QA olarak, AI metotlarının quota harcamadan testlerinin geçtiğini ve toplu dönüşüm metotlarının yan etki bırakmadığını otomatize etmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `tests/test_ai_engine.py` içinde her public AI metodu için en az 1 test (mock ile).
    - [ ] `tests/test_converter.py` (varsa genişletilir, yoksa oluşturulur) `batch_convert` için hem hepsi başarılı hem 1'i fail senaryosu.
    - [ ] `pdf_to_images` testinde tmp_path üzerinde çıkış dosyalarının gerçekten yaratıldığını assert eden test.
    - [ ] `merge_pdfs` testinde sayfa sayısının = sum(input pages) olduğu doğrulanır.
    - [ ] `pytest` koşum süresi tüm testler için < 20 saniye.
    - [ ] Sprint sonu rapor `WEEKLY_PROGRESS_ALI.md`'ye yeni hafta bloğu olarak işlenir.
*   **Görevler:**
    - [ ] `tests/test_ai_engine.py` oluştur (monkeypatch ile `AIEngine._call_gemini` mock).
    - [ ] `tests/test_converter.py` oluştur veya genişlet; küçük örnek PDF/CSV/PNG fixture'larını `tests/fixtures/` altına ekle.
    - [ ] `conftest.py` ile shared fixture (örn. `sample_pdf_path`) tanımı.
    - [ ] CI dokümantasyonu güncellemesi (gerekirse).

---

# 🎨 5. Hafta (Sprint 5) Görev Listesi (Issues)

> **Sprint Hedefi:** UI/UX cilalama (açık tema, animasyonlar, responsive iyileştirmeler), tüm zorunlu i18n anahtarlarının yerleşmesi, kapsamlı test coverage (>%70 hedefi).
> **Definition of Done:** Tema seçici çalışır; tüm kullanıcıya görünür string i18n'den gelir; `pytest --cov` raporu paylaşılır.

### 🔴 Issue #21: Tema Persistence ve Kullanıcı Tercihleri
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** Kullanıcının seçtiği tema (light/dark) ve dilin oturum sonrası da hatırlanması için `~/.universal-file-workstation/preferences.json` benzeri bir yerel persistence katmanı kurmak; `Config` üzerinden açılışta okumak.
*   **User Story:** _"Bir kullanıcı olarak, uygulamayı kapatıp tekrar açtığımda son kullandığım dil ve tema tercihimle açılmasını istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `config/settings.py` içine `Config.load_user_prefs()` ve `Config.save_user_prefs(prefs: dict)` static metotları eklenir.
    - [ ] Pencere yolu cross-platform: `Path.home() / ".universal-file-workstation" / "preferences.json"`.
    - [ ] `main.py::init_state()` ilk açılışta `prefs.json`'dan dil ve temayı okur.
    - [ ] Dil veya tema değişince otomatik kaydedilir (`Dashboard.render_sidebar()` içinde).
    - [ ] Dosya yoksa veya bozuksa varsayılana düşer ve `logging.warning` yazar.
    - [ ] `tests/test_settings.py` ile prefs okuma/yazma testleri.
*   **Görevler:**
    - [ ] `Config` üzerine `PREFS_PATH` constant ve helper metotlar.
    - [ ] `init_state()` güncellemesi.
    - [ ] Dashboard'da change-handler'a `Config.save_user_prefs(...)` ekle.
    - [ ] `.gitignore`'a `preferences.json` (kullanıcı home'unda olduğu için aslında gerekmez ama proje kökünde fallback varsa eklenmeli).

### 🟠 Issue #22: Görsel Kalite Önayarları + DOCX Sayfa Aralığı + RTF/ODT Genişletmesi
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** Görsel dönüşüm için kullanıcı dostu kalite preset'leri (`low/medium/high/lossless`); PDF→DOCX dönüşümünde sayfa aralığı parametresi; RTF/ODT input desteği için araştırma + uygulama.
*   **User Story:** _"Bir kullanıcı olarak, 'kalite: %75' yazmak yerine 'Yüksek/Orta/Düşük' seçmek; uzun bir PDF'in sadece 5-10 sayfa aralığını DOCX'e çevirmek; RTF/ODT dosyalarını da dönüştürmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `FileConverter.QUALITY_PRESETS: dict[str, int] = {"low": 50, "medium": 75, "high": 90, "lossless": 100}` modül seviyesinde sabit.
    - [ ] `convert_image` parametresi `quality: int | str = 100`; string verilirse preset'ten okur.
    - [ ] `convert_pdf_to_docx(input, output, start: int = 0, end: int | None = None)` parametreleri eklenir.
    - [ ] RTF/ODT için en az read (DOCX'e çevirme) desteği — `pypandoc` veya `striprtf` opsiyonu değerlendirilir.
    - [ ] Mevcut testler kırılmaz; yeni unit testler eklenir.
*   **Görevler:**
    - [ ] Preset constant'ı + parametre güncellemesi.
    - [ ] PDF→DOCX page range parametre yayılımı (UI'a kadar).
    - [ ] RTF/ODT için kütüphane seçimi + PR açıklamasında gerekçe.
    - [ ] `requirements.txt`'ye yeni paket ekleme (Ali koordinasyonu).

### 🟡 Issue #23: Açık Tema, Responsive Layout ve Animasyonlar
*   **Sorumlu:** **Samet Demir**
*   **Özet:** `ui/styles.py`'ye **light theme** varyantı eklemek (CSS değişkenlerini override eden ikinci bir blok); küçük ekranlarda sidebar collapse davranışı iyileştirmesi; tab geçişlerine fade-in animasyonu.
*   **User Story:** _"Bir kullanıcı olarak, gündüz açık temada, gece koyu temada çalışmak; küçük laptop ekranımda sidebar'ın okunabilir kalmasını istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `apply_custom_css(theme: str = "dark")` parametre alır; `theme="light"` için `:root` değişkenleri override eden ikinci CSS bloğu enjekte edilir.
    - [ ] Açık tema için palet: `--bg-base: #f7f9fc`, `--text-primary: #0b1220` vb. tutarlı tasarımla.
    - [ ] Sidebar 768px altında otomatik collapse'a uygun; içerik en az 320px width'te bozulmadan render olur.
    - [ ] Tab geçişlerine `transition: opacity 200ms ease` ile fade-in.
    - [ ] Buton hover lift efekti açık temada da iyi görünür (gölge rengi tema-aware).
    - [ ] Galip Efe'nin `Config.load_user_prefs()` ile entegre — `theme` `prefs.json`'dan okunur.
*   **Görevler:**
    - [ ] `apply_custom_css` parametre güncellemesi.
    - [ ] Light theme CSS değişken bloğu.
    - [ ] Tab fade-in transition CSS.
    - [ ] Manuel responsive testi 320 / 768 / 1280 / 1920 px breakpoint'lerinde.
    - [ ] `i18n` anahtarı: `settings_theme_light`, `settings_theme_dark`.

### 🔵 Issue #24: Görüntüleme Modülü Performans İyileştirmeleri (Lazy PDF Render + Pagination)
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** Büyük PDF'lerde (>50 sayfa) `display_pdf`'in tüm sayfayı tek seferde render etmesini engellemek; sayfa sayfa lazy render + `st.number_input` ile pagination eklemek; tablo görüntüleyicide arama/filtre özelliği.
*   **User Story:** _"Bir kullanıcı olarak, 200 sayfalık bir PDF yüklediğimde 5 dakika beklemek istemem; sadece görüntülemek istediğim sayfa aralığını seçmek istiyorum. Tabloda da sütunda arayabilmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `FileViewer.render_pdf` `start: int = 0, end: int | None = None` parametreleri alır.
    - [ ] `display_pdf` UI'da pagination (önceki/sonraki + sayfa numarası input + toplam sayfa göstergesi).
    - [ ] 100+ sayfa PDF için ilk render < 3 saniye (sadece görünür sayfa).
    - [ ] `display_table` `st.text_input` ile arama; DataFrame `df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]` ile filtrelenir.
    - [ ] Boş sonuç için `i18n["table_no_match"]` ile bilgi mesajı.
*   **Görevler:**
    - [ ] `render_pdf` parametreleri.
    - [ ] Pagination UI bileşeni.
    - [ ] Tablo arama input'u ve filtre mantığı.
    - [ ] Performans karşılaştırma notu PR açıklamasında (önce/sonra).

### 🟢 Issue #25: Coverage Raporu, E2E Senaryolar ve Belge Hijyeni
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** `pytest-cov` entegrasyonu, kapsamlı end-to-end senaryolar (her tab × her dosya tipi matrisi), README "Test" bölümünün güncellenmesi.
*   **User Story:** _"Bir QA olarak, hangi modülün hangi oranda test edildiğini sayısal görmek; her sprint sonu coverage raporunu ekibe paylaşmak istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `requirements.txt`'ye `pytest-cov~=<sürüm>` eklenir.
    - [ ] `pytest --cov=core --cov=ui --cov=config --cov-report=term-missing` komutu çalışır.
    - [ ] Coverage hedefi: `core/` ≥ %75, `config/` ≥ %90, `ui/` ≥ %40 (UI test zor, esnek).
    - [ ] E2E manuel test matrisi (`docs/E2E_TEST_MATRIX.md`) oluşturulur: her dosya tipi × her sekme.
    - [ ] README "Running Tests" bölümü coverage komutuyla güncellenir.
    - [ ] Sprint 5 raporu `WEEKLY_PROGRESS_ALI.md`'ye eklenir.
*   **Görevler:**
    - [ ] `requirements.txt` ve test komutları.
    - [ ] Coverage gap'lerini doldurmak için ek unit testler.
    - [ ] `docs/E2E_TEST_MATRIX.md` yaz.
    - [ ] README güncellemesi.

---

# 📦 6. Hafta (Sprint 6) Görev Listesi (Issues)

> **Sprint Hedefi:** Uygulamayı son kullanıcıya **PyInstaller ile `.exe`** olarak teslim etmek; FFmpeg bundling, app icon, son regresyon turu, v0.1.0 GitHub release.
> **Definition of Done:** Python kurulu olmayan temiz bir Windows makinesinde `.exe` çift tıklanır, açılır, tüm temel akışlar çalışır. GitHub Releases sayfasında binary + changelog + screenshot yayınlanır.

### 🔴 Issue #26: PyInstaller Spec ve `main.py` Üretim Modu Hardening
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** PyInstaller `.spec` dosyası yazmak; Streamlit'in özel ihtiyaçlarını (assets klasörü, runtime hooks) çözmek; `.exe` çift tıklayınca tarayıcı otomatik açılmasını sağlayacak launcher script.
*   **User Story:** _"Bir kullanıcı olarak, uygulamayı GitHub Releases'tan indirip Python kurmadan, terminal komutu yazmadan çift tıklayarak çalıştırmak istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `build/universal-file-workstation.spec` dosyası repo'ya eklenir.
    - [ ] `assets/`, `config/`, `core/`, `ui/` klasörleri `.exe` içine bundle edilir (`datas` parametresi).
    - [ ] Launcher script (`launcher.py` veya `main.py`'a eklenen `__main__` bloğu) Streamlit server'ı subprocess olarak başlatır + tarayıcı açar.
    - [ ] `.exe` boyutu < 250 MB (PRD hedefi 200 MB, esneklik tanınır).
    - [ ] Windows Defender false-positive'i için `pyinstaller --noconfirm --uac-admin` veya code signing notu dokümante edilir.
    - [ ] `docs/BUILD.md` adımlı build talimatı içerir.
*   **Görevler:**
    - [ ] `pyinstaller` ve `streamlit` runtime hook araştırması.
    - [ ] `.spec` dosyasını yaz; `hiddenimports` listesi (streamlit, pydub vb. için).
    - [ ] Launcher script.
    - [ ] App icon (`.ico`) hazırla (Samet ile koordinasyon).
    - [ ] Test build'i temiz Win10/11 VM'de.

### 🟠 Issue #27: FFmpeg Bundling ve Path Resolver
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** FFmpeg binary'sini `assets/bin/` altına bundle etmek; `core/player.py`'nin önce bundle'lanmış FFmpeg'i, yoksa sistem PATH'ini kullanmasını sağlamak.
*   **User Story:** _"Bir kullanıcı olarak, FFmpeg'i ayrıca indirip kurmak zorunda kalmadan ses dönüşümü yapabilmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `assets/bin/` altına Windows FFmpeg static build (LGPL) yerleştirilir.
    - [ ] `AudioConverter.__init__` önce `assets/bin/ffmpeg.exe`'yi kontrol eder, yoksa `shutil.which("ffmpeg")` fallback.
    - [ ] `pydub.AudioSegment.converter` global değişkeni doğru path'e set edilir.
    - [ ] `.gitignore`'a `assets/bin/` eklenir; binary git'e commit edilmez ama build script'i indirir.
    - [ ] `scripts/download_ffmpeg.py` script'i build aşamasında otomatik indirir.
    - [ ] Linux/macOS için aynı stratejinin notu `docs/BUILD.md`'de belgelenir (Sprint 6 scope: yalnızca Windows).
*   **Görevler:**
    - [ ] FFmpeg LGPL static build URL kararlaştır (gyan.dev veya BtbN).
    - [ ] `download_ffmpeg.py` yaz.
    - [ ] `AudioConverter` path resolver güncellemesi.
    - [ ] PyInstaller `.spec`'e `assets/bin/ffmpeg.exe` `binaries` olarak eklenir (Galip Efe ile koordinasyon).

### 🟡 Issue #28: Onboarding Akışı + Boş Durum Tasarımları + Hata Sayfaları
*   **Sorumlu:** **Samet Demir**
*   **Özet:** İlk açılışta gösterilen "Welcome / Onboarding" overlay'i; tüm sekmelerin "boş durum" (empty state) görselleri ve micro-illustration'ları; 500 / network error için kullanıcı dostu hata sayfası bileşeni.
*   **User Story:** _"İlk kez açan kullanıcı olarak, ne yapmam gerektiğini 30 saniyede anlamak; bir hata olduğunda 'Bir şey ters gitti' yerine ne yapmam gerektiğini söyleyen bir mesaj almak istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] İlk açılışta (`prefs.json`'da `onboarding_seen=False` ise) modal/expander ile 3 adımlı tanıtım gösterilir.
    - [ ] "Anladım" butonu `onboarding_seen=True` olarak kaydeder.
    - [ ] Her tab boş durumunda: ikon + başlık + alt yazı + CTA buton ("Dosya Yükle").
    - [ ] App icon (.ico + .png 512x512) hazırlanır (Galip Efe için).
    - [ ] `i18n` yeni anahtarlar: `onboarding_step_1/2/3`, `onboarding_dismiss`, `empty_state_convert`, `empty_state_view`, `empty_state_ai`.
*   **Görevler:**
    - [ ] Onboarding component (modal yerine `st.expander` + `st.session_state.onboarding_seen` ile).
    - [ ] Empty state bileşenleri (re-usable function).
    - [ ] App icon tasarımı.
    - [ ] CSS: empty state'ler için merkezi konum + soft glow.

### 🔵 Issue #29: Dosya Önizleme Cache + Görüntüle Modülü Final Cilalama
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** `FileViewer.render_pdf` çıktısını `st.cache_data` ile cache'lemek; tablo görünümünde sütun tipi metaverilerini gösteren küçük bir info satırı; resim önizlemede zoom/fit kontrolleri.
*   **User Story:** _"Aynı PDF'i ikinci kez açtığımda anında yüklenmesini; bir tabloya bakarken hangi sütunun int/float/str olduğunu görmek; görseli zoom-in/zoom-out yapabilmek istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `render_pdf` ve `read_table` fonksiyonları `@st.cache_data(ttl=3600)` ile dekore edilir (mümkünse modül seviyesi static helper olarak).
    - [ ] Aynı dosya 2. kez yüklendiğinde render süresi < 100ms.
    - [ ] `display_table` üstüne kısa bir "X satır × Y sütun · dtypes: int(2), float(1), object(3)" özet metni.
    - [ ] `display_image` zoom için Streamlit'in built-in `st.image` `width` parametresi + slider veya 3 preset (Fit / 100% / 200%).
    - [ ] Cache hit/miss telemetri için debug log eklenir.
*   **Görevler:**
    - [ ] Cache decorator implementasyonu — Streamlit cache'in self method ile uyumsuzluğu nedeniyle modül seviyesi private fonksiyonlara taşıma.
    - [ ] Tablo metadata satırı.
    - [ ] Resim zoom UI.
    - [ ] Performance benchmark notu PR'da.

### 🟢 Issue #30: Final Regresyon, Release Hazırlığı ve v0.1.0 Yayını
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** Tüm sprint'lerin birleşik regresyon turu; CHANGELOG.md yazımı; ekran görüntüleri; GitHub Release sayfası hazırlığı; lisans / üçüncü parti notice dosyaları.
*   **User Story:** _"Bir QA olarak, son kullanıcıya teslim öncesi tüm özelliklerin son bir kez yan yana test edildiğinden ve release notlarının kullanıcı dostu yazıldığından emin olmak istiyorum."_
*   **AC (Acceptance Criteria):**
    - [ ] `docs/CHANGELOG.md` Keep-a-Changelog formatında oluşturulur; Sprint 1-6 kazanımları kullanıcı diliyle özetlenir.
    - [ ] `docs/E2E_TEST_MATRIX.md` tam tur tamamlanır; sonuç tablosu repo'ya commit edilir.
    - [ ] En az 5 ekran görüntüsü `docs/screenshots/` altına eklenir (her tab + sidebar + onboarding).
    - [ ] README "Installation" bölümüne `.exe` indirme linki + system requirements eklenir.
    - [ ] `THIRD_PARTY_LICENSES.md` (FFmpeg LGPL dahil) hazırlanır.
    - [ ] GitHub Release `v0.1.0` etiketi atılır; `.exe`, kaynak kod ve checksums yüklenir.
    - [ ] Pre-release smoke test: temiz Win10 VM + temiz Win11 VM.
*   **Görevler:**
    - [ ] CHANGELOG yaz.
    - [ ] E2E matrix son tur.
    - [ ] Screenshot çekimi.
    - [ ] Üçüncü parti lisans notları derleme.
    - [ ] GitHub Release sayfası taslağı + ekibe review.

---

# 📊 Kapasite ve Risk Notları

| Risk | Etki | Hafifletme |
|:---|:---|:---|
| Gemini API key bağımlılığı | AI sekmesi key olmayan kullanıcıda çalışmaz | Sprint 4'te graceful degradation + clear error message |
| `docx2pdf` Windows + MS Word zorunluluğu | macOS/Linux kullanıcılarda DOCX→PDF kapalı | UI'da OS/Word kontrolü + alternatif öner (`libreoffice`) |
| PyInstaller Streamlit uyumu | `.exe` build'inde runtime hook karmaşası | Sprint 6 başında 1 günlük spike; gerekirse `nicegui`/`pywebview` fallback değerlendirilir |
| FFmpeg LGPL bundling lisans uyumu | Yasal | `THIRD_PARTY_LICENSES.md` ve LGPL koşulları belgelenir |
| Sprint 6'da regresyon süresi | Release gecikmesi | Sprint 5 sonu coverage ≥ %70 → regresyon yükü azalır |

# 👥 Sprint 3-6 Yük Dağılımı

| Üye | Sprint 3 | Sprint 4 | Sprint 5 | Sprint 6 | Notlar |
|:---|:---:|:---:|:---:|:---:|:---|
| Galip Efe Öncü | Issue #11 | Issue #16 | Issue #21 | Issue #26 | Architectural / cross-cutting |
| Said Hamza Turan | Issue #12 | Issue #17 | Issue #22 | Issue #27 | Backend converters & audio |
| Abdulkadir Sar | Issue #13 | Issue #18 | Issue #24 | Issue #29 | Viewer & UI helpers |
| Samet Demir | Issue #14 | Issue #19 | Issue #23 | Issue #28 | UI/UX & theme |
| Muhammed Ali Avcı | Issue #15 | Issue #20 | Issue #25 | Issue #30 | QA, i18n parite, release |

> Her sprint sonunda retrospektif: tamamlanmayan görevler bir sonraki sprint'in **ilk** önceliği olur, yeni görev eklenmeden devralınır.
