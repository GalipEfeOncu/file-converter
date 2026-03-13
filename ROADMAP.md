# 📅 Proje Yol Haritası (Roadmap)

Bu belge, **Universal File Workstation** projesinin 6 haftalık geliştirme sürecini tanımlar. Aşağıdaki listeleri GitHub üzerinde Issue açarken doğrudan kopyalayıp kullanabilirsiniz.

---

## 🏗️ Genel Takvim Özeti
*   **1. Hafta:** Altyapı, Arayüz İskeleti ve Temel Fonksiyonlar
*   **2. Hafta:** Dosya İşleme Motorları (PDF, DOCX, CSV)
*   **3. Hafta:** Dosya Görüntüleme ve Medya Oynatıcı Entegrasyonu
*   **4. Hafta:** Yapay Zeka (AI) Analiz Modülü ve API Entegrasyonu
*   **5. Hafta:** UI/UX Cilalama, Tema Desteği ve Hata Ayıklama
*   **6. Hafta:** Final Testleri, Dokümantasyon ve Yayınlama (.exe)

---

## 🚀 1. HAFTA: GitHub Issue Listesi

### 🏛️ Issue 1 — Proje Mimarı (Galip Efe Öncü)

**Issue #1.1**
- **Başlık:** Proje İskeletinin Kurulması ve Session State Yönetimi
- **İçerik:**
  - `main.py` dosyasının temel Streamlit yapısının oluşturulması.
  - Uygulama genelinde kullanılacak `session_state` kontrol mekanizmasının (yüklenen dosya takibi, aktif sayfa/mod bilgisi) kurgulanması.

**Issue #1.2**
- **Başlık:** Yapılandırma Sistemi ve Çevre Değişkenleri Entegrasyonu
- **İçerik:**
  - `config/settings.py` dosyasının tamamlanması.
  - `.env` dosyasından API anahtarlarını güvenli bir şekilde çekecek `python-dotenv` entegrasyonunun yapılması.
  - QA ile koordineli olarak i18n dil desteği altyapısının devreye alınması.

---

### ⚙️ Issue 2 — Mantık & Algoritma Mühendisi (Said Hamza Turan)

**Issue #2.1**
- **Başlık:** Temel Dönüştürme Algoritmaları Araştırması ve Altyapısı
- **İçerik:**
  - `core/converter.py` içinde PDF-to-Text ve CSV-to-XLSX dönüşümleri için kütüphane seçimi (pdf2docx, pandas vb.).
  - Dönüştürme fonksiyonlarının girdi-çıktı imzalarının ve hata yakalama (try-except) yapısının kurulması.

**Issue #2.2**
- **Başlık:** Ses İşleme ve FFmpeg Bağımlılık Kontrolü
- **İçerik:**
  - `core/player.py` içinde sistemde `ffmpeg` yüklü olup olmadığını kontrol eden bir doğrulama fonksiyonunun yazılması.
  - Temel ses dönüşüm (MP3/WAV) iskeletinin oluşturulması.

---

### 📄 Issue 3 — Dosya Görüntüleme Uzmanı (Abdulkadir Sar)

**Issue #3.1**
- **Başlık:** PDF Rendering ve Visual Preview Altyapısı
- **İçerik:**
  - `core/viewer.py` içinde `PyMuPDF` (fitz) kullanarak PDF dosyalarını imaja çevirme fonksiyonunun yazılması.
  - PDF sayfalarının Streamlit üzerinde `st.image` ile gösterilmesi için PoC (Proof of Concept) oluşturulması.

**Issue #3.2**
- **Başlık:** Tablo Veri Görüntüleme (CSV/Excel) Entegrasyonu
- **İçerik:**
  - Pandas kullanarak CSV ve Excel dosyalarının okunarak `st.dataframe` üzerinden temiz bir şekilde sunulması.
  - Veri tipi uyumsuzluklarını önlemek için temel bir validator yazılması.

---

### 🎨 Issue 4 — Arayüz Tasarımcısı (Samet Demir)

**Issue #4.1**
- **Başlık:** Ana Dashboard Düzeni ve Navigasyon Yapısı
- **İçerik:**
  - `ui/dashboard.py` içinde `st.sidebar` ve ana içerik alanının yerleşiminin yapılması.
  - Üç ana sekmenin (Dönüştür, Görüntüle, AI) `st.tabs` kullanılarak oluşturulması.

**Issue #4.2**
- **Başlık:** Tasarım Sistemi ve Görsel Kimlik (CSS)
- **İçerik:**
  - `ui/styles.py` içinde projenin kurumsal renk paleti ve tipografi standartlarının CSS olarak tanımlanması.
  - Streamlit'in standart dışı alanlarını özelleştirecek CSS enjeksiyonlarının başlatılması.

---

### 🧪 Issue 5 — Kalite Güvence & Test Uzmanı (Muhammed Ali Avcı)

**Issue #5.1:**
- **Başlık:** Dil Paketi (i18n) ve JSON Veri Yapısı
- **İçerik:**
  - `assets/languages.json` dosyasının hem Türkçe hem İngilizce olacak şekilde tüm anahtarlarının tanımlanması.
  - Uygulama içindeki metinlerin dinamik olarak bu dosyadan çekilmesi için test yapılması.

**Issue #5.2:**
- **Başlık:** Test Otomasyonu Kurulumu ve Smoke Testler
- **İçerik:**
  - `pytest` çalışma ortamının yapılandırılması.
  - Uygulamanın temel modüllerinin import edilebilirliğini ve `main.py`'ın çökmeden başladığını doğrulayan ilk test senaryolarının yazılması.
