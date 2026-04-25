# Issue #16 — Agent Çalışma Raporu

**Üye:** Galip Efe Öncü
**Tarih:** 2026-04-21
**Branch:** feat/issue-16-gemini-ai-engine
**Model:** Claude Opus 4.6 (Thinking)

## 1. Anladığım Görev
`core/ai_engine.py` içindeki mevcut iki metotlu (summarize, answer_question) stub implementasyonu gerçek Gemini API çağrılarıyla değiştirmek. Yeni metotlar eklemek: `extract_keywords(text, top_k)` ve `simplify(text, level)`. Tüm metotların `_call_gemini` private helper üzerinden çalışmasını sağlamak (DRY). `summarize` metoduna `length` parametresi eklemek. API anahtarı yokluğu, network/quota hatalarını graceful handle etmek. Projeye özel system prompt'lar tanımlamak.

## 2. Plan (Kabul Kriterlerine Karşılık)
- [x] AC #1 → `AIEngine.summarize(text, length="medium")` gerçek Gemini çağrısı — `core/ai_engine.py`'ye `length` parametresi + 3 system prompt varyantı (short/medium/long) eklendi
- [x] AC #2 → `AIEngine.answer_question(context, question)` context-feeding ile çalışır — mevcut implementasyon korundu ve doğrulandı
- [x] AC #3 → `AIEngine.extract_keywords(text, top_k=10)` eklendi — Gemini yanıtını parse edip `list[str]` döndürür, madde işaretlerini temizler
- [x] AC #4 → `AIEngine.simplify(text, level="intermediate")` eklendi — 3 seviye (basic/intermediate/advanced) system prompt varyantı
- [x] AC #5 → `GEMINI_API_KEY` None/boşsa metotlar `RuntimeError` fırlatmaz; bilgilendirici string döner (extract_keywords boş liste döner)
- [x] AC #6 → Network/quota/API hataları `try/except`'le yakalanır, `logging.error` + kullanıcı dostu string döner
- [x] AC #7 → 8 adet projeye özel system prompt tanımlandı, TR/EN çıktı dil yönetimi dahil
- [x] AC #8 → `_call_gemini(prompt, system)` private helper tüm metotlarca kullanılır (DRY)

## 3. Değiştirilen / Eklenen Dosyalar
| Dosya | Tip | Satır (+/-) | Açıklama |
|-------|-----|-------------|----------|
| `core/ai_engine.py` | Değiştirildi | +108 / -30 | 4 public metot (summarize, answer_question, extract_keywords, simplify), 8 system prompt sabiti, length/level parametreleri |
| `assets/languages.json` | Değiştirildi | +4 / -2 | `error_api_key_missing` ve `error_ai_request_failed` anahtarları (hem tr hem en) |
| `tests/test_ai_engine.py` | Değiştirildi | +199 / -53 | 25 test (monkeypatch mock ile), 6 test sınıfı: Basic, EmptyInputs, Summarize, AnswerQuestion, ExtractKeywords, Simplify, SystemPrompts |

## 4. Atlanan / Yapılamayan Maddeler
- **`requirements.txt` değişikliği:** `google-generativeai~=0.8.3` eklenmeli ancak bu dosyanın sahibi Ali (QA). Ali ile koordinasyon §8'de belirtildi. Mevcut `openai~=1.70.0` bağımlılığı aktif olarak kullanılmıyor; `google-generativeai` ile değiştirilmesi önerilir.
- **AI sekmesi UI bağlantısı:** Issue #18 (Abdulkadir Sar) kapsamındadır; `AIEngine` metotları UI'dan çağrılmaya hazırdır.

## 5. Test Sonuçları
- Komut: `python -m pytest tests -v`
- Sonuç: **PASS** (39 passed, 0 failed, 1 warning)
- Yeni eklenen testler:
  - `TestAIEngineBasic::test_instantiation`
  - `TestAIEngineBasic::test_summarize_returns_string`
  - `TestAIEngineBasic::test_answer_question_returns_string`
  - `TestEmptyInputs::test_summarize_empty_text`
  - `TestEmptyInputs::test_summarize_whitespace_only`
  - `TestEmptyInputs::test_answer_question_empty_context`
  - `TestEmptyInputs::test_answer_question_empty_question`
  - `TestEmptyInputs::test_extract_keywords_empty_text`
  - `TestEmptyInputs::test_simplify_empty_text`
  - `TestSummarizeWithMock::test_summarize_medium_calls_correct_prompt`
  - `TestSummarizeWithMock::test_summarize_short_calls_correct_prompt`
  - `TestSummarizeWithMock::test_summarize_long_calls_correct_prompt`
  - `TestSummarizeWithMock::test_summarize_invalid_length_falls_back`
  - `TestAnswerQuestionWithMock::test_answer_question_passes_correct_prompt`
  - `TestExtractKeywordsWithMock::test_extract_keywords_parses_response`
  - `TestExtractKeywordsWithMock::test_extract_keywords_respects_top_k`
  - `TestExtractKeywordsWithMock::test_extract_keywords_api_failure_returns_empty`
  - `TestExtractKeywordsWithMock::test_extract_keywords_uses_correct_system_prompt`
  - `TestExtractKeywordsWithMock::test_extract_keywords_cleans_bullet_points`
  - `TestSimplifyWithMock::test_simplify_intermediate_default`
  - `TestSimplifyWithMock::test_simplify_basic_level`
  - `TestSimplifyWithMock::test_simplify_advanced_level`
  - `TestSimplifyWithMock::test_simplify_invalid_level_falls_back`
  - `TestSystemPrompts::test_all_required_prompts_exist`
  - `TestSystemPrompts::test_prompts_are_non_empty_strings`

## 6. Dökümantasyonda Fark Ettiğim Sorunlar
- **AGENT_GUIDE.md §2.5:** `AIEngine` API sözleşmesi artık güncel değil. Yeni imzalar:
  - `summarize(text: str, length: str = "medium") -> str` (length parametresi yeni)
  - `extract_keywords(text: str, top_k: int = 10) -> list[str]` (yeni metot)
  - `simplify(text: str, level: str = "intermediate") -> str` (yeni metot)
- **AGENT_GUIDE.md §6:** `requirements.txt` tablosunda `openai~=1.70.0` listeleniyor ancak proje Gemini kullanıyor. `google-generativeai~=0.8.3` olarak güncellenmeli.
- **ROADMAP.md Issue #16 Görev maddesi:** `requirements.txt`'ye `google-generativeai~=<sürüm>` eklenmesi görevde belirtilmiş, ancak dosya sahibi Ali olduğu için koordinasyon gerekiyor.

## 7. Önerilen Commit Mesajı - (commit ingilizce olacak)

```
feat: implement full Gemini API integration for AIEngine

- Add `extract_keywords(text, top_k)` and `simplify(text, level)` public methods
- Add `length` parameter to `summarize()` with short/medium/long variants
- Define 8 task-specific system prompts as module-level constants
- Handle API key missing, network, and quota errors gracefully (no exceptions)
- Add `error_api_key_missing` and `error_ai_request_failed` i18n keys (tr+en)
- Rewrite test suite with 25 monkeypatch-based mock tests (0 API calls)

Refs: Issue #16
```

## 8. Koordinasyon / Delegasyon Notları
- **settings.py önerisi:** Değişiklik gerekmiyor. `Config.GEMINI_API_KEY` mevcut ve doğru çalışıyor.
- **i18n key eklemeleri (Ali için):** `error_api_key_missing` ve `error_ai_request_failed` anahtarları `assets/languages.json`'a hem `tr` hem `en` olarak eklendi. Ali'nin sprint review'da parite testini doğrulaması bekleniyor.
- **requirements.txt önerisi:** `google-generativeai~=0.8.3` eklenmeli. Mevcut `openai~=1.70.0` bağımlılığı artık kullanılmıyor (`ai_engine.py` Gemini kullanıyor); kaldırılması veya değiştirilmesi önerilir. Sahibi Ali — PR'da etiketlenecek.
- **main.py değişikliği gerekli mi (Galip Efe için):** Bu issue kapsamında hayır. AI sekmesi UI bağlantısı Issue #18 (Abdulkadir) kapsamındadır. `AIEngine` metotları UI'dan çağrılmaya hazırdır.
