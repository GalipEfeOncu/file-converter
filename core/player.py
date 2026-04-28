import os
import shutil
import logging
from pydub import AudioSegment

class AudioConverter:
    def __init__(self):
        self.ffmpeg_available = shutil.which("ffmpeg") is not None
        if not self.ffmpeg_available:
            logging.error("FFmpeg bulunamadı! Ses dönüşümleri çalışmayacak.")

    def convert_audio(self, input_path, output_path, output_format):
        if not self.ffmpeg_available:
            logging.error("Hata: FFmpeg kurulu değil.")
            return False
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=output_format)
            return True
        except Exception as e:
            logging.error(f"Dönüşüm hatası: {e}")
            return False

    def convert_mp3_to_wav(self, input_path, output_path):
        return self.convert_audio(input_path, output_path, "wav")

    def convert_wav_to_mp3(self, input_path, output_path):
        return self.convert_audio(input_path, output_path, "mp3")