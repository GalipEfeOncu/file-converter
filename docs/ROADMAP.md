# 🗺 Universal File Workstation: 6 Haftalık Geliştirme Yol Haritası

---

## 📅 Proje Planı Tanıtımı
Bu döküman, projenin 6 haftalık hızlandırılmış geliştirme planını ve üyelerin haftalık odak noktalarını içerir.

| Hafta | Odak Noktası | Ana Hedef |
| :--- | :--- | :--- |
| **Hafta 1** | **Temel Altyapı** | Altyapı, Arayüz İskeleti ve Temel Fonksiyonların kurulması. |
| **Hafta 2** | **Dosya İşleme** | Dosya İşleme Motorları (PDF, DOCX, CSV vb.) geliştirilmesi. |
| **Hafta 3** | **Görüntüleme & Medya** | Dosya Görüntüleme ve Medya Oynatıcı Entegrasyonu. |
| **Hafta 4** | **Yapay Zeka** | Yapay Zeka (AI) Analiz Modülü ve API Entegrasyonu. |
| **Hafta 5** | **UI/UX & Hata Ayıklama** | UI/UX Cilalama, Tema Desteği ve Hata Ayıklama. |
| **Hafta 6** | **Final & Yayınlama** | Final Testleri, Dokümantasyon ve Yayınlama (.exe olarak). |

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
    - [ ] `core/player.py` içinde sistemde `ffmpeg` yüklü olup olmadığını denetleyen doğrulama fonksiyonunu yaz.
    - [x] Temel ses dönüşüm (MP3/WAV) iskeletini oluştur.

### 🟡 Issue #3: PDF Rendering ve Tablo Veri Görüntüleme
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** Belge ve elektronik tablo dosyalarının Streamlit arayüzünde temiz ve görsel bir şekilde sunulması.
*   **Görevler:**
    - [x] `core/viewer.py` içinde `PyMuPDF` (fitz) kullanarak PDF dosyalarını imaja çevirme fonksiyonunu yaz.
    - [ ] PDF sayfalarının Streamlit üzerinde `st.image` ile gösterilmesi için PoC (Proof of Concept) oluştur.
    - [ ] Pandas kullanarak CSV ve Excel dosyalarının okunup `st.dataframe` üzerinden temiz sunulmasını sağla.
    - [x] Veri tipi uyumsuzluklarını önlemek için temel bir validator yaz.

### 🔵 Issue #4: Ana Dashboard ve Görsel Tasarım Sistemi
*   **Sorumlu:** **Samet Demir**
*   **Özet:** Uygulamanın navigasyon düzenini kurmak ve görsel bütünlüğü sağlamak için CSS enjeksiyonlarını başlatmak.
*   **Görevler:**
    - [ ] `ui/dashboard.py` içinde `st.sidebar` ve ana içerik alanının yerleşimini yap.
    - [ ] Üç ana sekmeyi (Dönüştür, Görüntüle, AI) `st.tabs` kullanarak oluştur.
    - [x] `ui/styles.py` içinde projenin kurumsal renk paleti ve tipografi standartlarını CSS olarak tanımla.
    - [x] Streamlit'in standart dışı alanlarını özelleştirecek CSS enjeksiyonlarını başlat.

### 🟢 Issue #5: Kalite Güvence ve Test Otomasyonu
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** Çoklu dil desteğinin testleri ve uygulamanın sistem test otomasyonunu (pytest) yapılandırmak.
*   **Görevler:**
    - [x] `assets/languages.json` dosyasını hem Türkçe hem İngilizce olacak şekilde tanımla.
    - [x] Uygulama içindeki metinlerin dinamik olarak bu dosyadan çekilmesi süreçlerini test et.
    - [x] `pytest` çalışma ortamını yapılandır.
    - [ ] Temel modüllerin import testlerini ve `main.py` çalışabilirliğini doğrulayan Smoke Test senaryolarını yaz.

---

# 🚀 2. Hafta (Sprint 2) Görev Listesi (Issues)

### 🔴 Issue #6: Arayüz ve Dönüştürücü Modüllerinin Entegrasyonu
*   **Sorumlu:** **Galip Efe Öncü**
*   **Özet:** `main.py` içerisindeki dönüştürme (Convert) ve görüntüleme (View) sekmelerinin altyapısını Said ve Abdulkadir'in modülleriyle bağlamak.
*   **Görevler:**
    - [ ] `main.py` "Dönüştür" sekmesine `core/converter.py` modülünü import edip bağla.
    - [ ] Streamlit arayüzünden seçilen dosya hedefine göre `converter.py` fonksiyonlarını tetikleyen buton ve durum yönetimini ekle.
    - [ ] `ai_engine.py` için temel Gemini API bağlantı taslağını yaz ve System Prompt oluşturarak test altyapısını kur.

### 🟠 Issue #7: Gelişmiş Dönüştürme Motorları (Resim & Belge)
*   **Sorumlu:** **Said Hamza Turan**
*   **Özet:** Proje detaylarındaki eksik görsel ve diğer metin formatı dönüşümlerini (PNG/JPG/WEBP, DOCX->PDF) kodlamak.
*   **Görevler:**
    - [ ] `core/converter.py` içine Pillow (PIL) kullanarak PNG <-> JPG <-> WEBP dönüşüm imkanlarını ekle.
    - [ ] DOCX dosyalarından PDF ve TXT formatına dönüştürme fonksiyonlarını yaz.
    - [ ] Arayüzde kalite seçeneği (görseller için %50, %80 vb.) alınabilecek şekilde fonksiyon imzalarına argüman (`quality: int`) ekle.
    - [ ] `player.py` dosyasındaki eksik kalan MP3 <-> OGG eklentilerini tamamla.

### 🟡 Issue #8: Arayüz Görüntüleme Bileşenlerinin (UI) Bağlanması
*   **Sorumlu:** **Abdulkadir Sar**
*   **Özet:** `viewer.py` arka planında oluşturulan render çıktılarının Streamlit arayüzünde kullanıcıya sunulması.
*   **Görevler:**
    - [ ] Dönüştürülen veya yüklenen PDF sayfalarını `st.image` ile art arda gösterecek bir loop kur.
    - [ ] Excel/CSV verilerini `pd.DataFrame` üzerinden okuduktan sonra `st.dataframe` veya `st.data_editor` ile arayüze bas.
    - [ ] `st.audio` ve `st.video` kullanarak medya oynatma araçlarının arayüzdeki entegrasyonu için kod taslaklarını hazırla.
    - [ ] DOCX veya TXT içeriğini okuyup UTF-8 olarak decodelayan ve `st.markdown` veya `st.text_area` ile gösteren fonksiyonu yaz.

### 🔵 Issue #9: Gelişmiş Dashboard ve Dosya Yükleme Paneli
*   **Sorumlu:** **Samet Demir**
*   **Özet:** Geçiçi `st.radio` navigasyonunu kaldırıp modern bir dashboard sidebar kalıbına geçmek.
*   **Görevler:**
    - [ ] `ui/dashboard.py` içindeki `render_sidebar()` fonksiyonunu yaz, "Dosya Geçmişi" veya dil seçimi konseptini oraya ekle.
    - [ ] `ui/dashboard.py` içindeki `render_main_area()` kısmında `st.tabs` kullanarak (Dönüştür, Görüntüle, AI) sekmelerini asıl yerine oturt.
    - [ ] Ana ekrandaki dosya yükleyici (`st.file_uploader`) kısmına CSS ekleyerek daha estetik bir sürükle-bırak kutusu görünümü ver (Drag&Drop hissi).
    - [ ] Galip Efe ile eş zamanlı çalışarak tasarımlarının `main.py` içerisine import edilmesini sağla.

### 🟢 Issue #10: Modül Entegrasyon Testleri ve Kalite Güvencesi
*   **Sorumlu:** **Muhammed Ali Avcı**
*   **Özet:** Yeni dönüştürücüler için gelişmiş testler ve projenin resmi sistem testinin başlatılması.
*   **Görevler:**
    - [x] `pytest.ini` ve test konfigürasyonlarını kurarak resmi test altyapısına geçiş yap.
    - [ ] DOCX -> PDF ve Görsel (JPG/PNG/WEBP) dönüştürme modülleri için birim (unit) testleri yaz.
    - [x] İngilizce/Türkçe string hatalarını veya çevirisi unutulan kelimeleri `languages.json` dosyasına ekle.
    - [x] Uygulamanın büyük dosyalarda (>50MB) çöküp çökmediğini görmek için manuel duman testleri (smoke test) yürüt.
