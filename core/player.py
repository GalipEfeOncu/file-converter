"""
core/player.py — Ses Dönüştürme Algoritmaları
Sahibi: Said Hamza (Mantık & Algoritma Mühendisi)
"""

import logging
import shutil
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class AudioConverter:
    import shutil
    import logging


class AudioConverter:
    def __init__(self):
        self.ffmpeg_available = shutil.which("ffmpeg") is not None

        if not self.ffmpeg_available:
            logging.warning("Uyarı: Sistemde FFmpeg bulunamadı.")
        else:
            logging.info("Sistem Kontrolü: FFmpeg başarıyla bulundu.")

    def __init__(self):
        self.ffmpeg_available = self.is_ffmpeg_installed()
        if not self.ffmpeg_available:
            logging.warning("KRİTİK UYARI: Sistemde 'ffmpeg' bulunamadı! Ses dönüşüm özellikleri çalışmayacaktır.")

    def is_ffmpeg_installed(self) -> bool:
        return shutil.which("ffmpeg") is not None

    def convert_audio(self, input_path: str, output_path: str, target_format: str) -> bool:
        if not self.ffmpeg_available:
            logging.error("Hata: İşlem iptal edildi. ffmpeg yüklü değil.")
            return False

        try:
            audio = AudioSegment.from_file(input_path)

            audio.export(output_path, format=target_format.lower())

            logging.info(f"Başarılı: Ses Dönüşümü -> {output_path} ({target_format.upper()})")
            return True

        except FileNotFoundError:
            logging.error(f"Hata: Girdi ses dosyası bulunamadı ({input_path})")
            return False
        except CouldntDecodeError:
            logging.error("Hata: Dosya çözülemedi. Dosya bozuk veya desteklenmeyen bir format olabilir.")
            return False
        except Exception as e:
            logging.error(f"Beklenmeyen Hata (Ses Dönüşümü): {e}")
            return False

    def convert_mp3_to_ogg(self, input_path: str, output_path: str) -> bool:
        return self.convert_audio(input_path, output_path, target_format="ogg")

    def convert_ogg_to_mp3(self, input_path: str, output_path: str) -> bool:
        return self.convert_audio(input_path, output_path, target_format="mp3")
