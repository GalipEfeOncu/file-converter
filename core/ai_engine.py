"""
core/ai_engine.py — Yapay Zeka Destekli Analiz Modülü
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Yüklenen metin tabanlı dosyaları (PDF, DOCX, TXT) Gemini API kullanarak analiz etmek;
özet çıkarma, soru-cevap, anahtar kelime çıkarma ve metin sadeleştirme yapmak.

Çıktı: "Ham metni işleyip anlamlı içgörülere ve özetlere dönüştüren AI servisi."
"""

import logging
import streamlit as st

from config.settings import Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ---------------------------------------------------------------------------
# System Prompt Sabitleri
# ---------------------------------------------------------------------------
_SYSTEM_PROMPTS: dict[str, str] = {
    "summarize": (
        "Sen bir belge özetleme asistanısın. Kullanıcının verdiği metni "
        "kısa, öz ve anlaşılır şekilde özetle. Özette ana fikirleri ve "
        "kritik detayları koru. Çıktı dilini girdi metninin diline göre "
        "otomatik seç (Türkçe metin → Türkçe özet, İngilizce metin → "
        "İngilizce özet)."
    ),
    "summarize_short": (
        "Sen bir belge özetleme asistanısın. Verilen metni EN FAZLA 2-3 "
        "cümleyle özetle. Yalnızca en önemli ana fikri koru. Çıktı dilini "
        "girdi metninin diline göre otomatik seç."
    ),
    "summarize_long": (
        "Sen bir belge özetleme asistanısın. Verilen metni detaylı şekilde "
        "özetle; tüm önemli noktaları, argümanları ve destekleyici detayları "
        "koru. Çıktı dilini girdi metninin diline göre otomatik seç."
    ),
    "qa": (
        "Sen bir soru-cevap asistanısın. Kullanıcının sağladığı bağlam "
        "metnini kullanarak soruyu yanıtla. Yalnızca bağlamda bulunan "
        "bilgilere dayalı cevap ver. Bağlamda yanıt bulamıyorsan bunu "
        "açıkça belirt. Cevap dilini sorunun diline göre seç."
    ),
    "keywords": (
        "Sen bir anahtar kelime çıkarma asistanısın. Verilen metinden "
        "en önemli ve temsil edici anahtar kelimeleri çıkar. Her anahtar "
        "kelimeyi yeni satıra yaz. Yalnızca anahtar kelimeleri döndür, "
        "ek açıklama ekleme. Çıktı dilini metnin diline göre seç."
    ),
    "simplify": (
        "Sen bir metin sadeleştirme asistanısın. Verilen metni daha "
        "anlaşılır, sade ve kolay okunur hale getir. Teknik terimleri "
        "günlük dil karşılıklarıyla açıkla. Anlamı koruyarak cümleleri "
        "kısalt ve basitleştir. Çıktı dilini metnin diline göre seç."
    ),
    "simplify_basic": (
        "Sen bir metin sadeleştirme asistanısın. Verilen metni çok basit, "
        "herkesin anlayabileceği bir dile çevir. Teknik terimleri tamamen "
        "günlük kelimelere dönüştür. Kısa cümleler kullan. "
        "Çıktı dilini metnin diline göre seç."
    ),
    "simplify_advanced": (
        "Sen bir metin sadeleştirme asistanısın. Verilen metnin akışını "
        "ve okunabilirliğini iyileştir; ancak teknik doğruluğu ve "
        "terminolojiyi koru. Akademik veya profesyonel seviyede yaz. "
        "Çıktı dilini metnin diline göre seç."
    ),
}

# ---------------------------------------------------------------------------
# Uzunluk → system prompt eşleme
# ---------------------------------------------------------------------------
_SUMMARY_LENGTH_MAP: dict[str, str] = {
    "short": "summarize_short",
    "medium": "summarize",
    "long": "summarize_long",
}

_SIMPLIFY_LEVEL_MAP: dict[str, str] = {
    "basic": "simplify_basic",
    "intermediate": "simplify",
    "advanced": "simplify_advanced",
}


class AIEngine:
    """Belgeler üzerinde yapay zeka analizi gerçekleştirir.

    Groq API üzerinden özet çıkarma, soru-cevap, anahtar kelime çıkarma
    ve metin sadeleştirme işlevleri sunar. API anahtarı yapılandırılmamışsa
    tüm metotlar bilgilendirici bir geri-dönüş (fallback) stringi döndürür;
    hata fırlatmaz.
    """

    def __init__(self):
        self._model = None
        self._client = None
        self._model_name = None
        self._init_client()

    def _init_client(self):
        """Groq API istemcisini başlatır. Eksik key veya paket durumunda
        graceful fallback sağlar."""
        logging.info("Groq API istemcisi başlatılıyor...")

        try:
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception as e:
                logging.warning(f"st.secrets ile okunamadı, dosyadan okunuyor... Hata: {e}")
                # Fallback: manuel okuma (Streamlit context hataları için)
                import re
                with open(".streamlit/secrets.toml", "r") as f:
                    match = re.search(r'GROQ_API_KEY\s*=\s*"([^"]+)"', f.read())
                    if match:
                        api_key = match.group(1)
                    else:
                        raise ValueError("GROQ_API_KEY bulunamadı.")
            
            if not api_key or api_key == "buraya_groq_api_key":
                logging.warning("Handshake FAILED: Groq API anahtarı yapılandırılmamış (secrets.toml dosyasını kontrol edin).")
                return
        except Exception as e:
            logging.warning(f"Handshake FAILED: Groq API key okunamadı: {e}")
            return

        try:
            from groq import Groq

            self._client = Groq(api_key=api_key)
            self._model_name = "llama-3.3-70b-versatile"
            self._model = True  # başarı bayrağı
            logging.info(f"Handshake SUCCESS: Groq API bağlantısı kuruldu (Model: {self._model_name}).")
        except ImportError:
            logging.error(
                "Handshake FAILED: groq paketi yüklü değil. "
                "Kurulum: pip install groq"
            )
        except Exception as e:
            logging.error(f"Handshake CRITICAL ERROR: Groq API başlatılamadı: {str(e)}")

    # ------------------------------------------------------------------
    # Private helper — tüm public metotlar bu fonksiyonu kullanır (DRY)
    # ------------------------------------------------------------------
    def _call_groq(self, prompt: str, system: str | None = None) -> str:
        """Groq modeline istek gönderir.

        Args:
            prompt: Kullanıcı/görev promptu.
            system: Opsiyonel system prompt (metot bazında).

        Returns:
            Model yanıtı veya hata durumunda bilgilendirici string.
        """
        if self._model is None:
            logging.warning("AI çağrısı reddedildi: Model başlatılmamış.")
            return (
                "API bağlantısı kurulamadı. Lütfen GROQ_API_KEY "
                "değerini .streamlit/secrets.toml dosyasında ayarlayın ve groq "
                "paketinin kurulu olduğundan emin olun."
            )

        try:
            logging.info("Groq API isteği gönderiliyor...")
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = self._client.chat.completions.create(
                model=self._model_name,
                messages=messages
            )
            logging.info("Groq API yanıtı başarıyla alındı.")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Hata: Groq API çağrısı başarısız: {str(e)}")
            return f"AI isteği başarısız oldu. Detay: {e}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def summarize(self, text: str, length: str = "medium") -> str:
        """Metni özetler.

        Args:
            text: Özetlenecek ham metin.
            length: Özet uzunluğu — "short", "medium" veya "long".

        Returns:
            Özet stringi veya hata/fallback mesajı.
        """
        if not text or not text.strip():
            return "Özetlenecek metin bulunamadı."

        prompt_key = _SUMMARY_LENGTH_MAP.get(length, "summarize")
        system = _SYSTEM_PROMPTS[prompt_key]
        return self._call_groq(text, system=system)

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
        return self._call_groq(prompt, system=_SYSTEM_PROMPTS["qa"])

    def extract_keywords(self, text: str, top_k: int = 10) -> list[str]:
        """Metinden anahtar kelimeleri çıkarır.

        Args:
            text: Analiz edilecek ham metin.
            top_k: Döndürülecek maksimum anahtar kelime sayısı.

        Returns:
            Anahtar kelime listesi. Hata durumunda boş liste.
        """
        if not text or not text.strip():
            logging.error("Hata: Anahtar kelime çıkarma için metin bulunamadı.")
            return []

        prompt = (
            f"Aşağıdaki metinden en önemli {top_k} anahtar kelimeyi çıkar. "
            f"Her anahtar kelimeyi yeni satıra yaz. "
            f"Yalnızca anahtar kelimeleri döndür:\n\n{text}"
        )
        raw = self._call_groq(prompt, system=_SYSTEM_PROMPTS["keywords"])

        # API bağlantı hatası durumunda boş liste döndür
        if raw.startswith("API bağlantısı kurulamadı") or raw.startswith("AI isteği başarısız"):
            logging.error(f"Hata: Anahtar kelime çıkarma başarısız: {raw}")
            return []

        # Yanıtı satırlara ayır, temizle ve top_k ile sınırla
        keywords = [
            line.strip().lstrip("•-–—*0123456789. ")
            for line in raw.strip().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        return keywords[:top_k]

    def simplify(self, text: str, level: str = "intermediate") -> str:
        """Metni sadeleştirir / basitleştirir.

        Args:
            text: Sadeleştirilecek ham metin.
            level: Sadeleştirme seviyesi — "basic", "intermediate" veya "advanced".

        Returns:
            Sadeleştirilmiş metin veya hata/fallback mesajı.
        """
        if not text or not text.strip():
            return "Sadeleştirilecek metin bulunamadı."

        prompt_key = _SIMPLIFY_LEVEL_MAP.get(level, "simplify")
        system = _SYSTEM_PROMPTS[prompt_key]
        return self._call_groq(text, system=system)
