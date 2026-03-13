"""
config/settings.py — Uygulama Yapılandırma ve Sabitler
Sahibi: Galip Efe Öncü (Proje Mimarı)

Senin Görevin:
Uygulamanın genel ayarlarını, API anahtarlarını, desteklenen dosya türlerini ve dil (i18n) tercihlerini merkezi bir yerden yönetmek.

Çıktı: "Uygulamanın her yerinden erişilebilen tutarlı ayarlar nesnesi."
"""

class Config:
    APP_NAME = "Universal File Workstation"
    DEFAULT_LANGUAGE = "tr"  # tr / en
    
    # TODO: Galip Efe Öncü — API anahtarlarını .env dosyasından çekme mantığını kur.
    # TODO: Galip Efe Öncü — Desteklenen dosya uzantılarını listele.
    
    API_KEY = "SECRET" # Örnek yer tutucu
