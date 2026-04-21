"""
tests/test_ai_engine.py — AIEngine modülü birim testleri
Ekleme: Issue #6 — Galip Efe Öncü

AIEngine'in API anahtarı olmadan (fallback modda) doğru çalıştığını,
hata fırlatmadığını ve string döndürdüğünü doğrular.
"""

from core.ai_engine import AIEngine


def test_ai_engine_instantiation():
    """AIEngine sınıfı hatasız oluşturulabilmeli."""
    engine = AIEngine()
    assert engine is not None


def test_summarize_returns_string():
    """summarize metodu string döndürmeli."""
    engine = AIEngine()
    result = engine.summarize("Bu bir test metnidir. Python programlama dili hakkında.")
    assert isinstance(result, str)
    assert len(result) > 0


def test_answer_question_returns_string():
    """answer_question metodu string döndürmeli."""
    engine = AIEngine()
    result = engine.answer_question(
        "Python bir programlama dilidir.",
        "Python nedir?"
    )
    assert isinstance(result, str)
    assert len(result) > 0


def test_summarize_with_empty_text():
    """Boş metin ile summarize çağrıldığında hata fırlatmamalı ve bilgilendirici mesaj döndürmeli."""
    engine = AIEngine()
    result = engine.summarize("")
    assert isinstance(result, str)
    assert len(result) > 0


def test_answer_question_with_empty_context():
    """Boş bağlam ile answer_question çağrıldığında hata fırlatmamalı."""
    engine = AIEngine()
    result = engine.answer_question("", "Test sorusu")
    assert isinstance(result, str)
    assert len(result) > 0


def test_answer_question_with_empty_question():
    """Boş soru ile answer_question çağrıldığında hata fırlatmamalı."""
    engine = AIEngine()
    result = engine.answer_question("Bağlam metni", "")
    assert isinstance(result, str)
    assert len(result) > 0
