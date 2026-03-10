# 📄 Project Details — File Converter & Analyzer

> Çok amaçlı bir masaüstü/web uygulaması: dosya dönüştürme, dahili görüntüleme ve yapay zekâ destekli içerik analizi.

---

## 🔍 Proje Tanımı

Bu proje; farklı dosya türlerini **dönüştürebilen**, uygulama içinde **görüntüleyebilen/çalıştırabilen** ve **yapay zekâ destekli içerik analizi** yapabilen çok amaçlı bir masaüstü veya web uygulamasıdır.

**UI Kütüphanesi:** [Streamlit](https://streamlit.io)

---

## 🧩 Modüller

### 1. Dosya Dönüştürme Modülü

Uygulama aşağıdaki kategorilerde dosya dönüştürme işlemleri gerçekleştirir:

#### 1.1 Metin ve Belge Dosyaları

| Kaynak Format | Hedef Format |
|---|---|
| PDF | DOCX, TXT, PNG, JPG |
| DOCX | PDF, TXT |
| CSV | XLSX |
| XLSX | CSV |

> **Amaç:** Metin ve tablo içeren dosyaları kendi aralarında dönüştürebilmek.

#### 1.2 Görsel Dosyaları

| Dönüşüm |
|---|
| PNG ↔ JPG |
| PNG / JPG ↔ WEBP |
| Görsel formatları arası kalite ayarlı dönüşüm |

#### 1.3 Ses Dosyaları

| Dönüşüm |
|---|
| MP3 ↔ WAV |
| MP3 ↔ OGG |
| Formatlar arası dönüştürme |

---

### 2. Dosya Görüntüleme ve Çalıştırma Modülü

Kullanıcı, uygulama içinde dosyaları açıp görüntüleyebilecektir:

| Dosya Türü | Görüntüleyici |
|---|---|
| PDF | Dahili PDF görüntüleyici |
| DOCX | Metin görüntüleyici |
| PNG / JPG | Görsel görüntüleyici |
| MP3 | Dahili ses oynatıcı |
| CSV / XLSX | Tablo görüntüleyici |

> **Amaç:** Kullanıcı, başka bir programa ihtiyaç duymadan dosyayı doğrudan uygulama içinde inceleyebilmeli.

---

### 3. Yapay Zekâ Destekli Analiz Modülü

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

| Özellik | Açıklama |
|---|---|
| 🌗 Tema | Karanlık / Açık tema desteği |
| 🌍 Çoklu Dil | Türkçe ve İngilizce dil desteği |
| 🕓 Dosya Geçmişi | Son işlem yapılan dosyalar listelenir |
| 🖱️ Sürükle-Bırak | Dosya yükleme kolaylığı |
| ⚙️ Ayarlar | Kalite ve çıktı formatı seçimi |

---

## 📌 Notlar

- Proje **Streamlit** kullanılarak geliştirilecektir.
- Dosya yapısı modüler ve genişletilebilir biçimde tasarlanacaktır.