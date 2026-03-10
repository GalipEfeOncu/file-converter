# =============================================================================
# core/player.py — Ses Format Dönüştürme İşleyicisi
# =============================================================================
#
# SORUMLULUK: Mantık & Algoritma Mühendisi
#
# Bu dosya ses dosyalarının format dönüşümünü yönetir. Görevleri:
#
#   1. SES DÖNÜŞÜMÜ (pydub tabanlı):
#      - MP3 → WAV : AudioSegment.from_mp3().export(format="wav")
#      - MP3 → OGG : AudioSegment.from_mp3().export(format="ogg")
#      - WAV → MP3 : AudioSegment.from_wav().export(format="mp3")
#      - OGG → MP3 : AudioSegment.from_ogg().export(format="mp3")
#
#   2. SES METAVERİSİ:
#      - Dönüştürülen dosyanın süresini, bit hızını ve kanal sayısını döndürür (kullanıcıya bilgi olarak gösterilir).
#
#   3. HATA YAKALAMA:
#      - ffmpeg kurulu değilse kullanıcıya net kurulum talimatı sunar.
#      - Bozuk/desteklenmeyen dosyalarda açıklayıcı hata mesajı üretir.
#
#   4. FONKSİYON İMZASI STANDARDI:
#      convert_audio(input_path: str, output_path: str, fmt: str) -> dict
#      -> {"success": bool, "output": str, "duration_sec": float,
#          "error": str | None}
#
# BAĞIMLILIKLAR: pydub  (sistem gereksinimi: ffmpeg)
#
# NOT: ffmpeg, sistemde PATH'e eklenmiş olmalıdır.
#      Windows: winget install ffmpeg
#      macOS  : brew install ffmpeg
#
# =============================================================================
