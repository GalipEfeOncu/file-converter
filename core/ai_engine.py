"""
core/ai_engine.py — Yapay Zeka Destekli Analiz Modülü
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Yüklenen metin tabanlı dosyaları (PDF, DOCX, TXT) Gemini API kullanarak analiz etmek;
özet çıkarma, soru-cevap ve içerik analizi yapmak.

Çıktı: "Ham metni işleyip anlamlı içgörülere ve özetlere dönüştüren AI servisi."
"""

import logging

from config.settings import Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ---------------------------------------------------------------------------
# System Prompt Sabitleri
# ---------------------------------------------------------------------------
_SYSTEM_PROMPTS = {
    "summarize": (
        "Sen bir belge özetleme asistanısın. Kullanıcının verdiği metni "
        "kısa, öz ve anlaşılır şekilde özetle. Özette ana fikirleri ve "
        "kritik detayları koru. Çıktı dilini girdi metninin diline göre "
        "otomatik seç (Türkçe metin → Türkçe özet, İngilizce metin → "
        "İngilizce özet)."
    ),
    "qa": (
        "Sen bir soru-cevap asistanısın. Kullanıcının sağladığı bağlam "
        "metnini kullanarak soruyu yanıtla. Yalnızca bağlamda bulunan "
        "bilgilere dayalı cevap ver. Bağlamda yanıt bulamıyorsan bunu "
        "açıkça belirt. Cevap dilini sorunun diline göre seç."
    ),
}


class AIEngine:
    """Belgeler üzerinde yapay zeka analizi gerçekleştirir.

    Gemini API üzerinden özet çıkarma ve soru-cevap işlevleri sunar.
    API anahtarı yapılandırılmamışsa tüm metotlar bilgilendirici
    bir geri-dönüş (fallback) stringi döndürür; hata fırlatmaz.
    """

    def __init__(self):
        self._model = None
        self._init_client()

    def _init_client(self):
        """Gemini API istemcisini başlatır. Eksik key veya paket durumunda
        graceful fallback sağlar."""
        if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "key_buraya_yazilacak":
            logging.warning("Gemini API anahtarı yapılandırılmamış.")
            return

        try:
            import google.generativeai as genai

            genai.configure(api_key=Config.GEMINI_API_KEY)
            self._model = genai.GenerativeModel("gemini-1.5-flash")
            logging.info("Başarılı: Gemini API bağlantısı kuruldu.")
        except ImportError:
            logging.error(
                "Hata: google-generativeai paketi yüklü değil. "
                "Kurulum: pip install google-generativeai~=0.8.3"
            )
        except Exception as e:
            logging.error(f"Hata: Gemini API başlatılamadı: {e}")

    # ------------------------------------------------------------------
    # Private helper — tüm public metotlar bu fonksiyonu kullanır (DRY)
    # ------------------------------------------------------------------
    def _call_gemini(self, prompt: str, system: str | None = None) -> str:
        """Gemini modeline istek gönderir.

        Args:
            prompt: Kullanıcı/görev promptu.
            system: Opsiyonel system prompt (metot bazında).

        Returns:
            Model yanıtı veya hata durumunda bilgilendirici string.
        """
        if self._model is None:
            return (
                "API bağlantısı kurulamadı. Lütfen GEMINI_API_KEY "
                "değerini .env dosyasında ayarlayın ve google-generativeai "
                "paketinin kurulu olduğundan emin olun."
            )

        try:
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            response = self._model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logging.error(f"Hata: Gemini API çağrısı başarısız: {e}")
            return f"AI isteği başarısız oldu. Detay: {e}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def summarize(self, text: str) -> str:
        """Metni özetler.

        Args:
            text: Özetlenecek ham metin.

        Returns:
            Özet stringi veya hata/fallback mesajı.
        """
        if not text or not text.strip():
            return "Özetlenecek metin bulunamadı."
        return self._call_gemini(text, system=_SYSTEM_PROMPTS["summarize"])

    def answer_question(self, context: str, question: str) -> str:
        """Verilen bağlam üzerinde soruyu yanıtlar.

        Args:
            context: Kaynak metin (bağlam).
            question: Kullanıcının sorusu.

        Returns:
            Yanıt stringi veya hata/fallback mesajı.
        """
        if not context or not context.strip():
            return "Soru-cevap için bağlam metni bulunamadı."
        if not question or not question.strip():
            return "Lütfen bir soru girin."

        prompt = f"Bağlam:\n{context}\n\nSoru: {question}"
        return self._call_gemini(prompt, system=_SYSTEM_PROMPTS["qa"])
