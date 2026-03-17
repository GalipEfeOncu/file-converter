"""
config/settings.py — Uygulama Yapılandırma ve Sabitler
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Uygulamanın genel ayarlarını, API anahtarlarını, desteklenen dosya türlerini ve dil (i18n) tercihlerini merkezi bir yerden yönetmek.

Çıktı: "Uygulamanın her yerinden erişilebilen tutarlı ayarlar nesnesi."
"""

import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını okur. Bu sayede API anahtarları gibi gizli bilgiler güvenli bir şekilde saklanır.


class Config:
    APP_NAME = "Universal File Workstation"
    DEFAULT_LANGUAGE = "tr"  # Default dil. tr / en

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # os.getenv() ile .env dosyasından API anahtarını çeker.

    # fmt: off
    SUPPORTED_EXTENSIONS = [
        # Dokümanlar
        ".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".epub",
        # Tablo ve Veri
        ".csv", ".xlsx", ".xls", ".json", ".xml", ".yaml",
        # Resim (Görsel Analiz için)
        ".jpg", ".jpeg", ".png", ".webp", ".svg", ".bmp",
        # Ses (Ses İşleme Modülü için)
        ".mp3", ".wav", ".ogg", ".flac", ".m4a",
        # Video (Görüntüleme Paneli için)
        ".mp4", ".mov", ".webm",
        # Kod (AI Analiz için Çok Önemli)
        ".py", ".ipynb", ".js", ".html", ".css", ".java", ".cpp", ".sql"
    ]
    # fmt: on

    VERSION = "0.1.0-alpha"
