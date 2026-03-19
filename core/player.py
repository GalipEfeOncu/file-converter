"""
core/player.py — Ses Dönüştürme Algoritmaları
Sahibi: Said Hamza Turan (Mantık & Algoritma Mühendisi)
"""

import logging
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

class AudioConverter:

    def convert_audio(self, input_path: str, output_path: str, target_format: str) -> bool:
        """
        Desteklenen ses formatları (MP3, WAV, OGG vb.) arasında güvenli dönüşüm yapar.

        """
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