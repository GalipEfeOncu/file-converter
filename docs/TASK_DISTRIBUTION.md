# Modern File Converter & Reader
## Ekip Görev Dağılımı ve Proje Mimarisi

> Bu belge, her ekip üyesinin sorumluluklarını ve modül sahipliklerini tanımlar. Her geliştirici yalnızca kendi alanında çalışacak; diğer modüllerle koordinasyon, net arayüzler üzerinden sağlanacaktır.
>
> 💡 Yeni başlayan geliştirici/model misin? Önce `docs/AGENT_GUIDE.md` (tek dosyada tam proje rehberi) sonra bu dosyayı oku.
>
> **Son Güncelleme:** 2026-04-19

---

## 🏛️ Görev 1 — Proje Mimarı & Yapay Zeka

**Sorumlu Kişi:** _Galip Efe Öncü_  
**Modüller:** `main.py`, `core/ai_engine.py`, `config/settings.py`

### Sorumluluklar
- `main.py` dosyasını yönetmek; Streamlit uygulama akışını (`st.set_page_config`, sayfa yönlendirmesi, oturum durumu) kurmak.
- Diğer takım arkadaşlarının yazdığı modülleri (`converter`, `viewer`, `player`) `main.py` içinde kusursuzca import etmek ve birbirine bağlamak.
- OpenAI/Gemini API ile belge özetleme ve soru-cevap mantığını `ai_engine.py` içinde geliştirmek.
- Streamlit `session_state` kullanarak uygulama genelindeki durum yönetimini (seçili dosya, aktif mod vb.) sağlamak.

---

## ⚙️ Görev 2 — Mantık & Algoritma Mühendisi

**Sorumlu Kişi:** _Said Hamza Turan_  
**Modüller:** `core/converter.py`, `core/player.py`

### Sorumluluklar
- Dosya dönüştürme algoritmalarını kurmak ve sağlamlaştırmak (Örn: PDF → DOCX, CSV → Excel) → `converter.py`
- Ses formatı dönüştürme (MP3/WAV/OGG) için `pydub` tabanlı işleyici mantığını geliştirmek → `player.py`
- Hata yakalama (Exception Handling) mekanizmalarını oluşturmak ve dönüştürme sırasındaki çökmeleri engellemek.
- Streamlit'ten çağrılabilecek şekilde temiz fonksiyon imzaları (`input_path`, `output_path` → `bool/str`) tasarlamak.

---

## 📄 Görev 3 — Dosya Görüntüleme Uzmanı

**Sorumlu Kişi:** _Abdulkadir Sar_  
**Modül:** `core/viewer.py`

### Sorumluluklar
- PDF sayfalarını **PyMuPDF (fitz)** ile resme çevirip Streamlit'te `st.image()` ile gösterilecek formata hazırlamak.
- **Pandas** yardımıyla Excel (`.xlsx`) ve CSV tablolarını okuyup `st.dataframe()` ile arayüzde temiz şekilde yansıtmak.
- Word (`.docx`) ve düz metin (`.txt`) dosyalarını binary-safe (UTF-8) olarak okuyup `st.text_area()` veya `st.markdown()` ile göstermek.

---

## 🎨 Görev 4 — Arayüz Tasarımcısı

**Sorumlu Kişi:** _Samet Demir_
**Modüller:** `ui/dashboard.py`, `ui/styles.py`

### Sorumluluklar
- **Streamlit** bileşenlerini (`st.columns`, `st.sidebar`, `st.tabs`, `st.expander` vb.) kullanarak modern bir sayfa düzeni oluşturmak → `dashboard.py`
- `ui/styles.py` dosyasında CSS enjeksiyonu (`st.markdown` + `unsafe_allow_html=True`) yöntemiyle özel tema, renk paleti ve tipografi tanımlamak.
- Karanlık tema uyumlu, genişleyebilir (responsive) bir sidebar ve içerik alanı tasarlamak.
- Yalnızca görsel düzeni teslim etmek; iş mantığı ve callback'ler Mimarın sorumluluğundadır.

---

## 🧪 Görev 5 — Kalite Güvence & Test Uzmanı

**Sorumlu Kişi:** _Muhammed Ali Avcı_  
**Modüller:** `assets/languages.json`, `requirements.txt`, `tests/`

### Sorumluluklar
- Sistemin Türkçe/İngilizce dil desteğini `languages.json` üzerinden hazırlamak ve dil iskeletini kurmak.
- Projenin `README.md` dosyasını, haftalık ilerleme raporlarını ve GitHub dokümantasyonunu yazmak/güncel tutmak.
- Her hafta diğer 4 kişinin kodlarını farklı senaryo ve zorlu dosyalarla test etmek ve bulguları raporlamak.  
  *(Örn: "Yüksek hacimli PDF dosyalarının işlenmesi sırasında bellek optimizasyonu kontrolü.")*
- `requirements.txt` bağımlılık listesini temiz, versiyonlanmış ve uyumlu tutmak.
- `pytest` ile `tests/` klasöründeki birim testleri çalıştırıp sonuçları paylaşmak.

---

## 🗂️ Modül Sahipliği Özet Tablosu

**1. Detaylı Modül Dağılımı:**

| Modül | Görev | Sorumlu |
|---|---|---|
| `main.py` | Streamlit giriş noktası & durum yönetimi | Mimar |
| `core/ai_engine.py` | Yapay zeka özetleme & soru-cevap | Mimar |
| `config/settings.py` | Uygulama geneli yapılandırma | Mimar |
| `core/converter.py` | Dosya format dönüştürme | Mantık Mühendisi |
| `core/player.py` | Ses formatı dönüştürme | Mantık Mühendisi |
| `core/viewer.py` | Dosya render & görüntüleme | Görüntüleme Uzmanı |
| `ui/dashboard.py` | Streamlit sayfa düzeni | Arayüz Tasarımcısı |
| `ui/styles.py` | CSS tema & renk sistemi | Arayüz Tasarımcısı |
| `assets/languages.json` | i18n dil stringleri | QA Mühendisi |
| `requirements.txt` | Bağımlılık yönetimi | QA Mühendisi |
| `tests/` | Birim & entegrasyon testleri | QA Mühendisi |

---

## 👨‍💻 Kişi ve Rol Bazlı Dosya Sorumlulukları (Kolay Görünüm)

Kimlerin hangi dosyalarda kodlama yapacağını kolayca takip etmek için özet liste:

| Rol | Sorumlu Kişi | Doğrudan Müdahale Edeceği Dosyalar (`.py` vb.) |
|---|---|---|
| **Proje Mimarı** | Galip Efe Öncü | `main.py`<br>`core/ai_engine.py`<br>`config/settings.py` |
| **Mantık Mühendisi** | Said Hamza Turan | `core/converter.py`<br>`core/player.py` |
| **Görüntüleme Uzmanı** | Abdulkadir Sar | `core/viewer.py` |
| **Arayüz Tasarımcısı** | Samet Demir | `ui/dashboard.py`<br>`ui/styles.py` |
| **QA & Test Uzmanı** | Muhammed Ali Avcı | `assets/languages.json`<br>`requirements.txt`<br>`tests/` klasörü |

---

## 🖥️ Uygulamayı Çalıştırma

```bash
# Sanal ortamı aktifleştir
venv\Scripts\activate

# Streamlit uygulamasını başlat
streamlit run main.py
```
