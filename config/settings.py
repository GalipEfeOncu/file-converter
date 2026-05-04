"""
config/settings.py — Uygulama Yapılandırma ve Sabitler
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Uygulamanın genel ayarlarını, API anahtarlarını, desteklenen dosya türlerini ve dil (i18n) tercihlerini merkezi bir yerden yönetmek.

Çıktı: "Uygulamanın her yerinden erişilebilen tutarlı ayarlar nesnesi."
"""

import os
import json
import logging
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını okur. Bu sayede API anahtarları gibi gizli bilgiler güvenli bir şekilde saklanır.


class Config:
    APP_NAME = "Universal File Workstation"
    DEFAULT_LANGUAGE = "en"  # Default language: en / tr

    # ---------------------------------------------------------------------------
    # AI Provider Configuration (loaded from .env)
    # ---------------------------------------------------------------------------
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")
    # Active provider: "groq" | "deepseek"  — overridable at runtime via session_state
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "groq").lower()



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

    PREFS_PATH = Path.home() / ".universal-file-workstation" / "preferences.json"

    @staticmethod
    def load_user_prefs() -> dict:
        """Kullanıcı tercihlerini ~/.universal-file-workstation/preferences.json'dan okur."""
        if not Config.PREFS_PATH.exists():
            return {}
        try:
            with open(Config.PREFS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Kullanıcı tercihleri okunamadı: {e}")
            return {}

    @staticmethod
    def save_user_prefs(prefs: dict):
        """Kullanıcı tercihlerini belirtilen konuma kaydeder."""
        try:
            Config.PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(Config.PREFS_PATH, "w", encoding="utf-8") as f:
                json.dump(prefs, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.warning(f"Kullanıcı tercihlerini kaydedilemedi: {e}")

    @staticmethod
    def switch_theme(theme: str):
        """
        Switches theme by copying the correct config file and restarting.
        theme: "dark" | "light"
        """
        streamlit_dir = Path(".streamlit")
        target = streamlit_dir / "config.toml"
        
        if theme == "dark":
            # Write dark config
            target.write_text("""[theme]
base = "dark"
backgroundColor = "#0f1117"
secondaryBackgroundColor = "#1a1d27"
textColor = "#e8eaf0"
primaryColor = "#5b6af0"
font = "sans serif"
""")
        else:
            # Write light config
            target.write_text("""[theme]
base = "light"
backgroundColor = "#f5f6fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#0d0f1a"
primaryColor = "#5b6af0"
font = "sans serif"
""")
        
        prefs = Config.load_user_prefs()
        prefs["theme"] = theme
        Config.save_user_prefs(prefs)
