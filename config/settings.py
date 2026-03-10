# =============================================================================
# config/settings.py — Uygulama Geneli Yapılandırma ve Sabitler
# =============================================================================
#
# SORUMLULUK: Mimar (Galip Efe Öncü)
#
# Bu dosya, uygulama boyunca kullanılan tüm sabit parametreleri, dosya yolu
# ayarlarını ve izin verilen limitleri tanımlar. Görevleri:
#
#   1. DESTEKLENEN UZANTILAR:
#      - ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt", ".csv", ".png", ... ]
#      - Uygulamanın kabul edeceği dosya türlerinin listesini tutmak.
#
#   2. DOSYA BOYUTU LİMİTLERİ:
#      - MAX_FILE_SIZE_MB = 10  (Ücretsiz / Standart kullanım limiti vb.)
#
#   3. DIZIN YOLLARI (PATHS):
#      - TEMP_DIR = "temp/"  (Geçici yüklenen dosyalar)
#      - OUTPUT_DIR = "exports/" (Dönüştürülmüş çıktıların kaydedileceği yer)
#      - Otomatik olarak bu klasörlerin var olup olmadığını kontrol eden bir
#        başlatma (init) fonksiyonu içerebilir.
#
#   4. AI MODEL AYARLARI:
#      - DEFAULT_MODEL = "gpt-4o"
#      - TEMPERATURE = 0.5 (Üretilen metnin yaratıcılık derecesi)
#
# KULLANIM:
#   from config.settings import ALLOWED_EXTENSIONS, TEMP_DIR
#
# =============================================================================
