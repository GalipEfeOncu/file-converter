"""
tests/test_ai_engine.py — AIEngine modülü birim testleri
Ekleme: Issue #6 — Galip Efe Öncü
Güncelleme: Issue #16 — Galip Efe Öncü

AIEngine'in tüm public metotlarını (summarize, answer_question,
extract_keywords, simplify) monkeypatch ile mock'lanmış _call_groq
üzerinden test eder. Gerçek API çağrısı yapılmaz.
"""

import pytest
from core.ai_engine import AIEngine, _SYSTEM_PROMPTS


# ---------------------------------------------------------------------------
# Fixture: AIEngine instance (API key olmadan fallback modda)
# ---------------------------------------------------------------------------
@pytest.fixture
def engine():
    """API key olmadan AIEngine oluşturur (fallback mod)."""
    return AIEngine()


# ---------------------------------------------------------------------------
# 1. Temel örnek testler (geriye uyumluluk)
# ---------------------------------------------------------------------------
class TestAIEngineBasic:
    """AIEngine sınıfının temel davranış testleri."""

    def test_instantiation(self, engine):
        """AIEngine sınıfı hatasız oluşturulabilmeli."""
        assert engine is not None

    def test_summarize_returns_string(self, engine):
        """summarize metodu string döndürmeli."""
        result = engine.summarize("Bu bir test metnidir. Python programlama dili hakkında.")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_answer_question_returns_string(self, engine):
        """answer_question metodu string döndürmeli."""
        result = engine.answer_question(
            "Python bir programlama dilidir.",
            "Python nedir?"
        )
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# 2. Boş/geçersiz girdi testleri
# ---------------------------------------------------------------------------
class TestEmptyInputs:
    """Boş girdi durumlarında hata fırlatmadan bilgilendirici mesaj döner."""

    def test_summarize_empty_text(self, engine):
        """Boş metin ile summarize çağrıldığında bilgilendirici mesaj döndürmeli."""
        result = engine.summarize("")
        assert isinstance(result, str)
        assert "metin" in result.lower() or len(result) > 0

    def test_summarize_whitespace_only(self, engine):
        """Sadece boşluk ile summarize çağrıldığında bilgilendirici mesaj döndürmeli."""
        result = engine.summarize("   \n\t  ")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_answer_question_empty_context(self, engine):
        """Boş bağlam ile answer_question çağrıldığında hata fırlatmamalı."""
        result = engine.answer_question("", "Test sorusu")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_answer_question_empty_question(self, engine):
        """Boş soru ile answer_question çağrıldığında hata fırlatmamalı."""
        result = engine.answer_question("Bağlam metni", "")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_extract_keywords_empty_text(self, engine):
        """Boş metin ile extract_keywords çağrıldığında boş liste döndürmeli."""
        result = engine.extract_keywords("")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_simplify_empty_text(self, engine):
        """Boş metin ile simplify çağrıldığında bilgilendirici mesaj döndürmeli."""
        result = engine.simplify("")
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# 3. Monkeypatch ile _call_groq mock testleri
# ---------------------------------------------------------------------------
class TestSummarizeWithMock:
    """summarize metodu _call_groq'ye doğru parametreleri geçirdiğini test eder."""

    def test_summarize_medium_calls_correct_prompt(self, engine, monkeypatch):
        """summarize(length='medium') doğru system prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["prompt"] = prompt
            called_with["system"] = system
            return "Mocked summary"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.summarize("Test metni", length="medium")

        assert result == "Mocked summary"
        assert called_with["prompt"] == "Test metni"
        assert called_with["system"] == _SYSTEM_PROMPTS["summarize"]

    def test_summarize_short_calls_correct_prompt(self, engine, monkeypatch):
        """summarize(length='short') kısa özet system prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Kısa özet"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.summarize("Test metni", length="short")

        assert called_with["system"] == _SYSTEM_PROMPTS["summarize_short"]

    def test_summarize_long_calls_correct_prompt(self, engine, monkeypatch):
        """summarize(length='long') uzun özet system prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Uzun özet"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.summarize("Test metni", length="long")

        assert called_with["system"] == _SYSTEM_PROMPTS["summarize_long"]

    def test_summarize_invalid_length_falls_back(self, engine, monkeypatch):
        """Geçersiz length değeri 'medium' varsayılanına düşer."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Fallback özet"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.summarize("Test metni", length="invalid_value")

        assert called_with["system"] == _SYSTEM_PROMPTS["summarize"]


class TestAnswerQuestionWithMock:
    """answer_question metodu doğru parametreleri geçirdiğini test eder."""

    def test_answer_question_passes_correct_prompt(self, engine, monkeypatch):
        """answer_question bağlam ve soruyu doğru formatta geçirmeli."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["prompt"] = prompt
            called_with["system"] = system
            return "Mocked answer"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.answer_question("Bağlam metni", "Test sorusu?")

        assert result == "Mocked answer"
        assert "Bağlam metni" in called_with["prompt"]
        assert "Test sorusu?" in called_with["prompt"]
        assert called_with["system"] == _SYSTEM_PROMPTS["qa"]


class TestExtractKeywordsWithMock:
    """extract_keywords metodu doğru çalıştığını test eder."""

    def test_extract_keywords_parses_response(self, engine, monkeypatch):
        """extract_keywords Groq yanıtını satırlara ayırıp listeye çevirmeli."""
        def mock_call(self_inner, prompt, system=None):
            return "Python\nYapay Zeka\nMakine Öğrenimi\nDerin Öğrenme\nVeri Bilimi"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.extract_keywords("Uzun bir test metni burada")

        assert isinstance(result, list)
        assert len(result) == 5
        assert "Python" in result
        assert "Yapay Zeka" in result

    def test_extract_keywords_respects_top_k(self, engine, monkeypatch):
        """extract_keywords top_k sınırına uymalı."""
        def mock_call(self_inner, prompt, system=None):
            return "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK\nL"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.extract_keywords("Metin", top_k=3)

        assert len(result) == 3

    def test_extract_keywords_api_failure_returns_empty(self, engine, monkeypatch):
        """API bağlantı hatası durumunda boş liste döndürmeli."""
        def mock_call(self_inner, prompt, system=None):
            return "API bağlantısı kurulamadı. Lütfen GROQ_API_KEY..."

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.extract_keywords("Metin")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_extract_keywords_uses_correct_system_prompt(self, engine, monkeypatch):
        """extract_keywords doğru system prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "keyword1\nkeyword2"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.extract_keywords("Test metni")

        assert called_with["system"] == _SYSTEM_PROMPTS["keywords"]

    def test_extract_keywords_cleans_bullet_points(self, engine, monkeypatch):
        """extract_keywords madde işaretlerini temizlemeli."""
        def mock_call(self_inner, prompt, system=None):
            return "• Python\n- Yapay Zeka\n* Veri\n1. Analiz\n2. Model"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.extract_keywords("Test metni")

        assert "Python" in result
        assert "Yapay Zeka" in result
        assert "Veri" in result
        assert "Analiz" in result
        assert "Model" in result


class TestSimplifyWithMock:
    """simplify metodu doğru parametreleri geçirdiğini test eder."""

    def test_simplify_intermediate_default(self, engine, monkeypatch):
        """simplify(level='intermediate') varsayılan system prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Sadeleştirilmiş metin"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        result = engine.simplify("Karmaşık metin")

        assert result == "Sadeleştirilmiş metin"
        assert called_with["system"] == _SYSTEM_PROMPTS["simplify"]

    def test_simplify_basic_level(self, engine, monkeypatch):
        """simplify(level='basic') basit sadeleştirme prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Basit metin"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.simplify("Karmaşık metin", level="basic")

        assert called_with["system"] == _SYSTEM_PROMPTS["simplify_basic"]

    def test_simplify_advanced_level(self, engine, monkeypatch):
        """simplify(level='advanced') gelişmiş sadeleştirme prompt'u kullanmalı."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Profesyonel metin"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.simplify("Karmaşık metin", level="advanced")

        assert called_with["system"] == _SYSTEM_PROMPTS["simplify_advanced"]

    def test_simplify_invalid_level_falls_back(self, engine, monkeypatch):
        """Geçersiz level değeri 'intermediate' varsayılanına düşer."""
        called_with = {}

        def mock_call(self_inner, prompt, system=None):
            called_with["system"] = system
            return "Fallback metin"

        monkeypatch.setattr(AIEngine, "_call_groq", mock_call)
        engine.simplify("Karmaşık metin", level="nonexistent")

        assert called_with["system"] == _SYSTEM_PROMPTS["simplify"]


# ---------------------------------------------------------------------------
# 4. System prompt sabitlerinin tutarlılık kontrolü
# ---------------------------------------------------------------------------
class TestSystemPrompts:
    """System prompt sabitleri doğru tanımlanmış olmalı."""

    def test_all_required_prompts_exist(self):
        """Tüm gerekli system prompt anahtarları tanımlı olmalı."""
        required = {
            "summarize", "summarize_short", "summarize_long",
            "qa", "keywords",
            "simplify", "simplify_basic", "simplify_advanced",
        }
        assert required.issubset(set(_SYSTEM_PROMPTS.keys()))

    def test_prompts_are_non_empty_strings(self):
        """Tüm system prompt'lar boş olmayan string olmalı."""
        for key, value in _SYSTEM_PROMPTS.items():
            assert isinstance(value, str), f"{key} string değil"
            assert len(value.strip()) > 0, f"{key} boş"
