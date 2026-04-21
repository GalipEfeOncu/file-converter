# Issue #6 — Agent Çalışma Raporu

**Üye:** Galip Efe Öncü
**Tarih:** 2026-04-21
**Branch:** feat/issue-6-converter-integration
**Model:** Claude Opus 4.6 (Thinking)

## 1. Anladığım Görev
Issue #6, Sprint 2'nin ana entegrasyon görevidir. `ui/dashboard.py` içindeki "Dönüştür" sekmesindeki placeholder metinleri kaldırarak `core/converter.py` ve `core/player.py` modüllerini fonksiyonel şekilde bağlamayı; kullanıcının dosya yükleyip hedef format seçerek dönüştürme yapabilmesini sağlamayı; ve `core/ai_engine.py` için temel Gemini API bağlantı taslağını (system prompt dahil) yazmayı kapsar.

## 2. Plan (Kabul Kriterlerine Karşılık)
- [x] AC #1 → `ui/dashboard.py` tabs[0]: Dosya yüklenmemişse i18n uyarısı göster
- [x] AC #2 → `ui/dashboard.py` tabs[0]: Uzantıya göre hedef format listesini `st.selectbox` ile sun
- [x] AC #3 → `ui/dashboard.py` tabs[0]: "Dönüştür" butonuyla `FileConverter`/`AudioConverter` çağır
- [x] AC #4 → `core/ai_engine.py`: Gemini API taslağı + system prompt + `_call_gemini` helper
- [x] AC #5 → `assets/languages.json`: Yeni i18n anahtarları (TR + EN parite)
- [x] AC #6 → `tests/test_ai_engine.py`: Birim testleri (en az 1 success + 1 failure)

## 3. Değiştirilen / Eklenen Dosyalar
| Dosya | Tip | Satır (+/-) | Açıklama |
|-------|-----|-------------|----------|
| `core/ai_engine.py` | Değiştirildi | +115/−23 | Gemini API taslağı, `_call_gemini` helper, system prompt sabitleri |
| `ui/dashboard.py` | Değiştirildi | +93/−7 | Dönüştür sekmesi: format map, dispatcher, temp yazma, download |
| `assets/languages.json` | Değiştirildi | +14/−2 | 7 yeni i18n anahtarı (TR + EN) |
| `tests/test_ai_engine.py` | Eklendi | +56/−0 | AIEngine birim testleri (6 test) |

## 4. Atlanan / Yapılamayan Maddeler
- `google-generativeai` paketi `requirements.txt`'ye eklenmedi (yasak — §8'de önerildi).
- `docx2pdf` paketi eksikliği bu issue'nun kapsamında değil (Issue #12/#15 kapsamı).
- `ui/dashboard.py` dosya I/O içeriyor; AGENT_GUIDE §10.2 şablonunu takip ettim ancak `ui/* dosya I/O yasak` kuralıyla mimari gerilim mevcut. İleride `core/file_utils.py`'ye taşınabilir.

## 5. Test Sonuçları
- Komut: `.\venv\Scripts\python.exe -m pytest tests -v`
- Sonuç: **PASS** (11 passed in 0.05s)
- Yeni eklenen testler: `tests/test_ai_engine.py` (6 test)
- Mevcut testler kırılmadı: `test_languages.py` (3 test), `test_requirements.py` (2 test)

## 6. Dökümantasyonda Fark Ettiğim Sorunlar
1. **AGENT_GUIDE.md §10.2** — Şablon `ui/dashboard.py` içinde dosya I/O gösteriyor (`with open(in_path, "wb")`) ancak §0/§1'de "ui/* dosya I/O yasak" kuralı var. Tutarsızlık.
2. **ROADMAP.md Issue #6** — "main.py 'Dönüştür' sekmesine" diyor ancak tab içerikleri `ui/dashboard.py`'de render ediliyor. Doğru referans `ui/dashboard.py` olmalı.
3. **AGENT_GUIDE.md §6** — `docx2pdf` requirements.txt'de eksik notu var; bu hâlâ geçerli (Issue #15 kapsamında çözülecek).

## 7. Önerilen Commit Mesajı

```
feat: integrate converter module into Convert tab and scaffold Gemini AI engine

- Connect FileConverter and AudioConverter to Dashboard Convert tab
- Add format dispatcher with dynamic target format selection per file type
- Add temp file save/cleanup helpers for conversion pipeline
- Scaffold AIEngine with Gemini API connection and system prompts
- Add 7 new i18n keys (btn_convert, btn_download, etc.) in TR and EN
- Add unit tests for AIEngine module

Refs: Issue #6
```

## 8. Koordinasyon / Delegasyon Notları
- **settings.py önerisi:** Değişiklik gerekmedi.
- **i18n key eklemeleri (Ali için):** 7 yeni anahtar eklendi (`btn_convert`, `btn_download`, `select_target_format`, `converting_in_progress`, `no_file_uploaded`, `selected_file`, `no_conversion_available`). Ali'nin parite testlerini doğrulaması önerilir.
- **requirements.txt önerisi:** `google-generativeai~=0.8.3` eklenmeli (Gemini API istemcisi). Gerekçe: `ai_engine.py` Gemini model çağrısı yapabilmesi için zorunlu. Mevcut `openai` paketi Gemini'yi desteklemiyor.
- **main.py değişikliği gerekli mi (Galip Efe için):** Hayır, mevcut `main.py` yapısı yeterli. Dashboard zaten main.py'dan çağrılıyor.
- **dashboard.py koordinasyonu (Samet için):** tabs[0] bloğu değiştirildi. Samet'in UI/CSS çalışmalarıyla çakışma olmaması için review önerilir.
