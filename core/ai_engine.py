# =============================================================================
# core/ai_engine.py — Yapay Zekâ Destekli İçerik Analiz Motoru
# =============================================================================
#
# SORUMLULUK: Mimar (Galip Efe Öncü)
#
# Bu dosya, desteklenen dosya türlerinin içeriğini okuyup OpenAI/Gemini API üzerinden analiz eden AI motorunu barındırır. Görevleri:
#
#   1. METİN OKUMA:
#      - PDF  : PyPDF2 ile tüm sayfalardan ham metin çıkarma
#      - DOCX : python-docx ile paragrafları birleştirme
#      - TXT  : UTF-8 dosya okuma
#      - CSV  : pandas ile ilk N satırı metne dönüştürme (önizleme analizi)
#
#   2. AI ANALİZ FONKSİYONLARI:
#      - summarize(text)          → Belgeyi kısa ve anlaşılır şekilde özetler.
#      - generate_questions(text) → İçerikten çalışma soruları üretir.
#      - extract_keywords(text)   → Anahtar kavramları listeler.
#      - suggest_title(text)      → Belge için başlık önerir.
#      - simplify(text, level)    → Metni belirtilen seviyede (basit/orta/
#                                   akademik) yeniden yazar.
#
#   3. API YÖNETİMİ:
#      - python-dotenv ile .env dosyasındaki API anahtarını güvenli okur.
#      - Seçili modeli (gpt-4o / gemini-pro) config/settings.py'den alır.
#      - Rate limit ve ağ hatalarını yakalar, kullanıcıya anlaşılır
#        hata mesajı iletir.
#
#   4. FONKSİYON İMZASI STANDARDI:
#      Her AI fonksiyonu şu imzayı izleyecek:
#        analyze_X(text: str, **kwargs) -> dict
#        -> {"success": bool, "result": str, "error": str | None}
#
# BAĞIMLILIKLAR: openai, python-dotenv, PyPDF2, python-docx, pandas
#
# =============================================================================
